import uuid
import os
import socket
from datetime import datetime, timedelta
import yaml
from miacag.preprocessing.split_train_val import splitter
from miacag.utils.sql_utils import copy_table, add_columns, \
    copyCol, changeDtypes

import pandas as pd
from miacag.postprocessing.append_results import appendDataFrame
import torch
from miacag.trainer import train
from miacag.tester import test
from miacag.configs.config import load_config, maybe_create_tensorboard_logdir
from miacag.configs.options import TrainOptions
import argparse
from miacag.preprocessing.labels_map import labelsMap
from miacag.preprocessing.utils.check_experiments import checkExpExists, \
    checkCsvExists
from miacag.plots.plotter import plot_results, plotRegression
import pandas as pd
from miacag.preprocessing.transform_thresholds import transformThreshold
from miacag.preprocessing.transform_missing_floats import transformMissingFloats
from miacag.utils.script_utils import create_empty_csv, mkFolder, maybe_remove, test_for_file, write_file
from miacag.postprocessing.aggregate_pr_group import Aggregator
from miacag.postprocessing.count_stenosis_pr_group \
    import CountSignificantStenoses

parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    '--cpu', type=str,
    help="if cpu 'True' else 'False'")
parser.add_argument(
            "--local_rank", type=int,
            help="Local rank: torch.distributed.launch.")
parser.add_argument(
            "--local-rank", type=int,
            help="Local rank: torch.distributed.launch.")
parser.add_argument(
            "--num_workers", type=int,
            help="Number of cpu workers for training")    
parser.add_argument(
    '--config_path', type=str,
    help="path to folder with config files")


def stenosis_identifier(cpu, num_workers, config_path, table_name_input=None):
    if table_name_input is None:
        print('world', os.environ['WORLD_SIZE'])
        print('rank', os.environ['RANK'])
        print('local rank', os.environ['LOCAL_RANK'])
        print('hostname', socket.gethostname())
        torch.distributed.init_process_group(
                backend="nccl" if cpu == "False" else "Gloo",
                init_method="env://",
                timeout=timedelta(seconds=1800000),
                world_size=int(os.environ['WORLD_SIZE']),
                rank=int(os.environ['RANK'])
                )
    config_path = [
        os.path.join(config_path, i) for i in os.listdir(config_path)]

    for i in range(0, len(config_path)):
        print('loading config:', config_path[i])
        with open(config_path[i]) as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
        mkFolder(config['output'])
        csv_exists, output_csv_test = checkCsvExists(config['output'])


        exp_exists = checkExpExists(config_path[i], config['output'])
        if exp_exists is False:

            config['master_port'] = os.environ['MASTER_PORT']
            config['num_workers'] = num_workers
            config['cpu'] = cpu
            tensorboard_comment = os.path.basename(config_path[i])[:-5]
            temp_file = os.path.join(config['output'], 'temp.txt')
            torch.distributed.barrier()
            if torch.distributed.get_rank() == 0:
                maybe_remove(temp_file)
                experiment_name = tensorboard_comment + '_' + \
                    "SEP_" + \
                    datetime.now().strftime('%b%d_%H-%M-%S')
                write_file(temp_file, experiment_name)
            torch.distributed.barrier()
            experiment_name = test_for_file(temp_file)[0]
            output_directory = os.path.join(
                        config['output'],
                        experiment_name)
            mkFolder(output_directory)
            output_config = os.path.join(output_directory,
                                         os.path.basename(config_path[i]))
            if table_name_input is None:
                output_table_name = \
                    experiment_name + "_" + config['table_name']
            else:
                output_table_name = table_name_input

            output_plots = os.path.join(output_directory, 'plots')
            mkFolder(output_plots)

            output_plots_train = os.path.join(output_plots, 'train')
            output_plots_val = os.path.join(output_plots, 'val')
            output_plots_test = os.path.join(output_plots, 'test')

            mkFolder(output_plots_train)
            mkFolder(output_plots_test)
            mkFolder(output_plots_val)

            # begin pipeline
            # 1. copy table
            os.system("mkdir -p {output_dir}".format(
                output_dir=output_directory))
            torch.distributed.barrier()
            if torch.distributed.get_rank() == 0:
                if table_name_input is None:
                    copy_table(sql_config={
                        'database': config['database'],
                        'username': config['username'],
                        'password': config['password'],
                        'host': config['host'],
                        'schema_name': config['schema_name'],
                        'table_name_input': config['table_name'],
                        'table_name_output': output_table_name})

                # # 2. copy config
                os.system(
                    "cp {config_path} {config_file_temp}".format(
                        config_path=config_path[i],
                        config_file_temp=output_config))
            # rename labels and add columns;
            trans_label = [i + '_transformed' for i in config['labels_names']]
            labels_names_original = config['labels_names']
            config['labels_names'] = trans_label
            # add placeholder for confidences
            conf = [i + '_confidences' for i in config['labels_names']]
            conf_agg = [i + '_confidences_aggregated' for i in config['labels_names']]
            # add placeholder for predictions
            pred = [i + '_predictions' for i in config['labels_names']]

            torch.distributed.barrier()
            if torch.distributed.get_rank() == 0:
                add_columns({
                    'database': config['database'],
                    'username': config['username'],
                    'password': config['password'],
                    'host': config['host'],
                    'schema_name': config['schema_name'],
                    'table_name': output_table_name,
                    'table_name_output': output_table_name},
                            trans_label,
                            ["float8"] * len(trans_label))
                # copy content of labels
                copyCol(
                    {'database': config["database"],
                        'username': config["username"],
                        'password': config['password'],
                        'host': config['host'],
                        'schema_name': config['schema_name'],
                        'table_name': output_table_name,
                        'query': config['query_transform']},
                    labels_names_original,
                    trans_label)

                add_columns({
                    'database': config['database'],
                    'username': config['username'],
                    'password': config['password'],
                    'host': config['host'],
                    'schema_name': config['schema_name'],
                    'table_name': output_table_name,
                    'table_name_output': output_table_name},
                            conf,
                            ["VARCHAR"] * len(conf))
                add_columns({
                    'database': config['database'],
                    'username': config['username'],
                    'password': config['password'],
                    'host': config['host'],
                    'schema_name': config['schema_name'],
                    'table_name': output_table_name,
                    'table_name_output': output_table_name},
                            pred,
                            ["float8"] * len(pred))

                add_columns({
                    'database': config['database'],
                    'username': config['username'],
                    'password': config['password'],
                    'host': config['host'],
                    'schema_name': config['schema_name'],
                    'table_name': output_table_name,
                    'table_name_output': output_table_name},
                            conf_agg,
                            ["float8"] * len(conf))
                

                add_columns({
                    'database': config['database'],
                    'username': config['username'],
                    'password': config['password'],
                    'host': config['host'],
                    'schema_name': config['schema_name'],
                    'table_name': output_table_name,
                    'table_name_output': output_table_name},
                            ["antalsignifikantestenoser_pred"],
                            ["float8"])

                # 3. split train and validation , and map labels
                trans = transformMissingFloats({
                    'labels_names': config['labels_names'],
                    'database': config['database'],
                    'username': config['username'],
                    'password': config['password'],
                    'host': config['host'],
                    'schema_name': config['schema_name'],
                    'table_name': output_table_name,
                    'query': config['query_transform'],
                    'TestSize': config['TestSize']})
                trans()

                trans_thres = transformThreshold({
                    'labels_names': config['labels_names'],
                    'database': config['database'],
                    'username': config['username'],
                    'password': config['password'],
                    'host': config['host'],
                    'schema_name': config['schema_name'],
                    'table_name': output_table_name,
                    'query': config['query_transform'],
                    'TestSize': config['TestSize']},
                    config)
                trans_thres()

                # change dtypes for label
                changeDtypes(
                    {'database': config["database"],
                        'username': config["username"],
                        'password': config['password'],
                        'host': config['host'],
                        'schema_name': config['schema_name'],
                        'table_name': output_table_name,
                        'query': config['query_transform']},
                    trans_label,
                    ["int8"] * len(trans_label))
                splitter_obj = splitter(
                    {
                        'labels_names': config['labels_names'],
                        'database': config['database'],
                        'username': config['username'],
                        'password': config['password'],
                        'host': config['host'],
                        'schema_name': config['schema_name'],
                        'table_name': output_table_name,
                        'query': config['query_split'],
                        'TestSize': config['TestSize']})
                splitter_obj()
                # ...and map data['labels'] test
            # 4. Train model
            torch.distributed.barrier()
            config['output'] = output_directory
            config['output_directory'] = output_directory
            config['table_name'] = output_table_name
            config['use_DDP'] = 'True'
            config['datasetFingerprintFile'] = None
            train(config)

            # 5 eval model

            config['model']['pretrain_model'] = output_directory
            test({**config, 'query': config["query_test"], 'TestSize': 1})


            torch.distributed.barrier()
            torch.cuda.empty_cache()
            torch.distributed.destroy_process_group()


            # plotting results
           # torch.distributed.barrier()
           # if torch.distributed.get_rank() == 0:
            # 6 plot results:
            # train
            plot_results({
                        'database': config['database'],
                        'username': config['username'],
                        'password': config['password'],
                        'host': config['host'],
                        'labels_names': config['labels_names'],
                        'table_name': output_table_name,
                        'schema_name': config['schema_name'],
                        'query': config['query_train_plot']},
                        config['labels_names'],
                        [i + "_predictions" for i in
                            config['labels_names']],
                        output_plots_train,
                        config['model']['num_classes'],
                        config,
                        [i + "_confidences" for i in
                            config['labels_names']]
                        )


            # val
            plot_results({
                        'database': config['database'],
                        'username': config['username'],
                        'password': config['password'],
                        'host': config['host'],
                        'schema_name': config['schema_name'],
                        'labels_names': config['labels_names'],
                        'table_name': output_table_name,
                        'query': config['query_val_plot']},
                        config['labels_names'],
                        [i + "_predictions" for i in
                            config['labels_names']],
                        output_plots_val,
                        config['model']['num_classes'],
                        config,
                        [i + "_confidences" for i in
                            config['labels_names']]
                        )

            # test
            plot_results({
                        'database': config['database'],
                        'username': config['username'],
                        'password': config['password'],
                        'host': config['host'],
                        'labels_names': config['labels_names'],
                        'schema_name': config['schema_name'],
                        'table_name': output_table_name,
                        'query': config['query_test_plot']},
                        config['labels_names'],
                        [i + "_predictions" for i in
                            config['labels_names']],
                        output_plots_test,
                        config['model']['num_classes'],
                        config,
                        [i + "_confidences" for i in
                            config['labels_names']]
                        )

            # append results 
            # csv_results = appendDataFrame(sql_config={
            #                     'labels_names': config['labels_names'],
            #                     'database': config['database'],
            #                     'username': config['username'],
            #                     'password': config['password'],
            #                     'host': config['host'],
            #                     'schema_name': config['schema_name'],
            #                     'table_name': output_table_name,
            #                     'query': config['query_test_plot']},
            #                 df_results=df_results,
            #                 experiment_name=experiment_name)
            print('config files processed', str(i+1))
            print('config files to process in toal:', len(config_path))
            # csv_results = pd.DataFrame(csv_results)
            # csv_results.to_csv(output_csv_test, index=False, header=True)

        if csv_exists:
            return None
        else:
            return output_table_name


if __name__ == '__main__':
    args = parser.parse_args()
    stenosis_identifier(args.cpu, args.num_workers, args.config_path)
