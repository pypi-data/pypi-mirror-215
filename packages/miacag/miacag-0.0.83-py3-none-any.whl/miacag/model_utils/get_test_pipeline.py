from miacag.model_utils.eval_utils import val_one_epoch
from miacag.model_utils.eval_utils import eval_one_step
import os
import json
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from miacag.preprocessing.pre_process import appendDataframes
import os
from miacag.preprocessing.pre_process import mkFolder
import psycopg2
from psycopg2.extras import execute_batch
from miacag.utils.sql_utils import update_cols
import torch
import shutil
import time


class TestPipeline():
    def get_test_pipeline(self, model, criterion, config, test_loader,
                          device, init_metrics,
                          normalize_metrics,
                          running_metric_test, running_loss_test):

        if config['task_type'] in ["classification", "regression", "mil_classification"]:
            self.get_test_classification_pipeline(model, criterion,
                                                  config, test_loader,
                                                  device, init_metrics,
                                                  normalize_metrics,
                                                  running_metric_test,
                                                  running_loss_test)
        elif config['loaders']['task_type'] == "image2image":
            self.get_test_segmentation_pipeline(model, criterion,
                                                config, test_loader,
                                                device, init_metrics,
                                                normalize_metrics,
                                                running_metric_test,
                                                running_loss_test)
        else:
            raise ValueError("Task type is not implemented")

    def get_test_classification_pipeline(self, model, criterion,
                                         config, test_loader,
                                         device, init_metrics,
                                         normalize_metrics,
                                         running_metric_test,
                                         running_loss_test):
        start = time.time()
        print('starting inference:')
        metrics, df_results = val_one_epoch(
            model, criterion, config,
            test_loader.val_loader, device,
            running_metric_val=running_metric_test,
            running_loss_val=running_loss_test,
            saliency_maps=False)
        stop = time.time()
        print('time for testing:', stop-start)
        for count, label in enumerate(config['labels_names']):
            csv_files = self.saveCsvFiles(label, df_results, config, count)
        torch.distributed.barrier()
        if torch.distributed.get_rank() == 0:
            for count, label in enumerate(config['labels_names']):
                test_loader.val_df = self.buildPandasResults(
                    label,
                    test_loader.val_df,
                    csv_files,
                    count,
                    config)
                self.insert_data_to_db(test_loader, label, config)
                if config['loss']['name'] == 'CE':
                    acc = {
                        'accuracy ensemble_' + label: accuracy_score(
                            test_loader.val_df[label].astype('float').astype('int'),
                            test_loader.val_df[
                                label + '_predictions'].astype(
                                    'float').astype('int'))}
                    print('accuracy_correct', acc)
                    metrics.update(acc)
                print('metrics (mean of all preds)', metrics)
                
                log_name = config["table_name"] + '_' + label + '_log.txt'
                with open(
                    os.path.join(config['output_directory'], log_name),
                        'w') as file:
                    file.write(json.dumps({**metrics, **config},
                            sort_keys=True, indent=4,
                            separators=(',', ': ')))
            shutil.rmtree(csv_files)
            cachDir = os.path.join(
                            config['model']['pretrain_model'],
                            'persistent_cache')
            if os.path.exists(cachDir):
                shutil.rmtree(cachDir)

    def get_test_segmentation_pipeline(self, model, criterion,
                                       config, test_loader,
                                       device, init_metrics,
                                       normalize_metrics,
                                       running_metric_test, running_loss_test):
        from models.image2image_utils.utils_3D.test_utils_img2img_monai \
                import slidingWindowTest
        testModule = slidingWindowTest(model, criterion, config,
                                       test_loader, device,
                                       running_metric_val=running_metric_test,
                                       running_loss_val=running_loss_test,
                                       saliency_maps=False)
        testModule()

    def get_output_pr_class(self, outputs, class_idx):
        outs = []
        for row in outputs[0]:
            for idx, value in enumerate(row):
                if idx == class_idx:
                    outs.append(value.item())
        return outs

    def buildPandasResults(self, label_name, val_df, csv_files, count, config):
        filename = os.path.join(csv_files, label_name)
        df_pred = self.appendDataframes(filename)
        df_pred['rowid'] = df_pred['rowid'].astype(float).astype(int)
        col_names = [
            i for i in df_pred.columns.to_list() if i.startswith(
                label_name + '_confidence')]
        df_pred[label_name+'_confidences'] = df_pred[col_names].values.tolist()

        if label_name + '_predictions' in val_df.columns:
            val_df = val_df.drop(columns=[label_name + '_predictions'])
        if label_name + '_confidences' in val_df.columns:
            val_df = val_df.drop(columns=[label_name + '_confidences'])
        #val_df = pd.concat([val_df, df_pred], axis=1)
        val_df = val_df.merge(
            df_pred, left_on='rowid', right_on='rowid', how='right')
        val_df[label_name + '_confidences'] = \
            val_df[label_name + '_confidences'].apply(pd.to_numeric)
        val_df_conf = pd.DataFrame()
        val_df_conf[label_name + '_confidences'] = val_df.groupby(
            'rowid')[label_name + '_confidences'].apply(np.mean)
        if config['loss']['name'][count].startswith('CE'):
            val_df_conf[label_name + '_predictions'] = \
                val_df_conf[label_name + '_confidences'].apply(np.argmax)
        elif config['loss']['name'][count] in ['MSE', '_L1', 'L1smooth', 'NNL']:
            val_df_conf[label_name + '_predictions'] = \
                val_df_conf[label_name + '_confidences'].astype(float)
        elif config['loss']['name'][count] == 'BCE_multilabel':
            val_df_conf[label_name + '_predictions'] = \
                val_df_conf[label_name + '_confidences'].apply(
                    np.round).astype(int)
        else:
            raise ValueError(
                'not implemented loss: ', config['loss']['name'][count])
        val_df = val_df.merge(
            val_df_conf,
            left_on='rowid',
            right_on='rowid',
            how='inner').drop_duplicates('rowid')
        val_df[label_name + '_confidences'] = \
            val_df[label_name + '_confidences_y']
        val_df = val_df.drop(
            columns=[label_name + '_confidences_y',
                     label_name + '_confidences_x'])
        return val_df

    def insert_data_to_db(self, test_loader, label_name, config):
        confidences = self.array_to_tuple(
            test_loader.val_df[label_name + '_confidences'].to_list())
        test_loader.val_df[label_name + '_confidences'] = confidences
        records = test_loader.val_df.to_dict('records')
        update_cols(
                    records, config,
                    [label_name + '_predictions', label_name + '_confidences'])

    def resetDataPaths(self, test_loader, config):
        test_loader.val_df['DcmPathFlatten'] = \
            test_loader.val_df['DcmPathFlatten'].apply(
                lambda x:  "".join(
                    x.rsplit(config['DataSetPath'])).strip(os.sep))
        return test_loader

    def array_to_tuple(self, confidences):
        conf_list_tuple = []
        for conf in confidences:
            li = [np.format_float_positional(i, precision=4)
                  for i in tuple(conf)]
            li = [str(i) + ":" + li[i] for i in range(len(li))]
            li = tuple(li)
            li = self.tuple2key(li)
            conf_list_tuple.append([li])
        return conf_list_tuple

    def tuple2key(self, t, delimiter=u';'):
        return delimiter.join(t)

    def saveCsvFiles(self, label_name, df, config, count):
        if config['loss']['name'][count].startswith('CE'):
            confidences = label_name + '_confidence'
           # confidences = confidences[count]
            confidence_col = [
                label_name + '_confidence_' +
                str(i) for i in range(0, config['model']['num_classes'][count])]
        else:
            confidences = label_name + '_confidence'
         #   df[confidences] = np.expand_dims(df[confidences], 1)
            confidence_col = [
                label_name + '_confidence_' +
                str(i) for i in range(0, 1)]
        csv_files = os.path.join(config['output_directory'], 'csv_files_pred')
        mkFolder(csv_files)
        label_name_csv_files = os.path.join(csv_files, label_name)
        mkFolder(label_name_csv_files)
        array = np.concatenate(
            (np.expand_dims(df[confidences].to_numpy(), 1),
             np.expand_dims(df["rowid"].to_numpy(), 1)), axis=1)
      
        cols = confidence_col + ['rowid']
        if config['loss']['name'][count].startswith('CE'):
            # convert array with rows with liusts to liste
            liste = []
            for i in range(0, config['model']['num_classes'][count]):
                liste.append(array[i, 0] + [array[i,1]])
            array = liste
        df = pd.DataFrame(
            array,
            columns=cols)
        df.to_csv(
            os.path.join(label_name_csv_files, str(torch.distributed.get_rank()))+'.csv')
        return csv_files
      #  df.to_csv()
    
    def appendDataframes(self, csv_files_dir):
        paths = os.listdir(csv_files_dir)
        paths = [os.path.join(csv_files_dir, p) for p in paths]
        li = []
        for filename in paths:
            df = pd.read_csv(filename, index_col=None,
                             header=0, dtype=str)
            li.append(df)
        return pd.concat(li, axis=0, ignore_index=True)