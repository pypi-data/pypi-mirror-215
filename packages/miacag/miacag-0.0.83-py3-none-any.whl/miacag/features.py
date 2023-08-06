import torch
from miacag.dataloader.get_dataloader import get_dataloader_test
from miacag.configs.options import TestOptions
from miacag.metrics.metrics_utils import init_metrics, normalize_metrics
from miacag.model_utils.get_loss_func import get_loss_func
from miacag.model_utils.predict_utils import Predictor
from miacag.configs.config import load_config
from miacag.trainer import get_device
from miacag.models.BuildModel import ModelBuilder
import os
from miacag.model_utils.train_utils import set_random_seeds
from miacag.tester import read_log_file, convert_string_to_tuple
import shutil
from miacag.models.modules import get_loss_names_groups
from miacag.models.get_encoder import get_encoder
from sklearn.decomposition import PCA
from miacag.utils.script_utils import mkFolder
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import monai
import numpy as np

def compute_pca(dino_params, patch_feat):
    patch_feat = patch_feat.reshape(dino_params['patch_h'] * dino_params['patch_w'], dino_params['feat_dim'])
    pca = PCA(n_components=3)
    pca.fit(patch_feat)
    pca_features = pca.transform(patch_feat)
    return pca_features, pca

def plot_pca(pca_features, dino_params, config, output_directory, frame_idx):
   # pca_folder = os.path.join(output_directory, 'pca')
   # mkFolder(pca_folder)
    pca_features[:, 0] = (pca_features[:, 0] - pca_features[:, 0].min()) / (pca_features[:, 0].max() - pca_features[:, 0].min())
    # create figure
    plt.figure(figsize=(32, 32))
    plt.imshow(pca_features[:, 0].reshape(dino_params['patch_h'], dino_params['patch_w']))
    plt.show()
    plt.savefig(os.path.join(output_directory, 'pca1' + str(frame_idx) + '.png'))
    plt.close()
    
def plot_pca_rgb(pca_features, dino_params, config, output_directory, patch_feat, pca, frame_idx):
    features = patch_feat.reshape(dino_params['patch_h'] * dino_params['patch_w'], dino_params['feat_dim'])
    # segment using the first component
   # pca_dir = os.path.join(output_directory, 'pca')
  #  mkFolder(pca_dir)
    pca_features_bg = pca_features[:, 0] < 10
    pca_features_fg = ~pca_features_bg

    pca_background = pca_features_bg.reshape(
                dino_params['patch_h'], dino_params['patch_w'])
    pca_background = np.flip(np.rot90(np.rot90(np.rot90(pca_background))), 1)
    plt.figure(figsize=(32, 32))
    plt.imshow(
        pca_features_bg.reshape(
                dino_params['patch_h'], dino_params['patch_w']))
    plt.show()
    plt.savefig(os.path.join(output_directory, 'pca_background' + str(frame_idx) + '.png'))
    plt.close()

    # PCA for only foreground patches
    pca.fit(features.numpy()[pca_features_fg]) # NOTE: I forgot to add it in my original answer
    pca_features_rem = pca.transform(features.numpy()[pca_features_fg])
    for i in range(3):
        # pca_features_rem[:, i] = (pca_features_rem[:, i] - pca_features_rem[:, i].min()) / (pca_features_rem[:, i].max() - pca_features_rem[:, i].min())
        # transform using mean and std, I personally found this transformation gives a better visualization
        pca_features_rem[:, i] = (pca_features_rem[:, i] - pca_features_rem[:, i].mean()) / (pca_features_rem[:, i].std() ** 2) + 0.5

    pca_features_rgb = pca_features.copy()
    pca_features_rgb[pca_features_bg] = 0
    pca_features_rgb[pca_features_fg] = pca_features_rem

    pca_features_rgb = pca_features_rgb.reshape(1, dino_params['patch_h'], dino_params['patch_w'], 3)
   # for i in range(0, 1):
    #    plt.subplot(2, 2, i+1)
    pca_rgb = pca_features_rgb[0,..., ::-1]
    pca_rgb = np.flip(np.rot90(np.rot90(np.rot90(pca_rgb))), 1)

    plt.figure(figsize=(32, 32))
    plt.imshow(pca_rgb)
    plt.savefig(os.path.join(output_directory, 'features' + str(frame_idx) + '.png'))
    plt.show()
    plt.close()
    return pca_rgb


def show_features_grayscale_image(image, features, output_directory, frame_idx):
    image = np.flip(np.rot90(np.rot90(np.rot90(image))), 1)
    features = np.flip(np.rot90(np.rot90(np.rot90(features))), 1)

    plt.figure(figsize=(32, 32))
    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap='gray')
    plt.subplot(1, 2, 2)
    plt.imshow(features)

    plt.savefig(os.path.join(output_directory, 'input_vs_feats' + str(frame_idx) + '.png'))
    plt.show()
    plt.close()
    
def show_grayscale_image(image, output_directory, frame_idx):
    image = np.flip(np.rot90(np.rot90(np.rot90(image))), 1)
    plt.figure(figsize=(32, 32))
    plt.imshow(image, cmap='gray')
    plt.savefig(os.path.join(output_directory, 'input' + str(frame_idx) + '.png'))
    plt.show()
    plt.close()

def get_patch_features(config, model, test_loader, dino_params, output_directory):
    output_directory = os.path.join(output_directory, 'features')
    mkFolder(output_directory)
    with torch.no_grad():
        for i, sample in enumerate(test_loader.val_loader):
            data_path = sample['DcmPathFlatten_meta_dict']['filename_or_obj'][0]
            data_array = monai.transforms.LoadImage()(data_path)[0].numpy()
            if i== 1:
                print('done forwarining samples:', i)

                break
            for frame_idx in range(0, sample['inputs'].shape[-1]):
                data_array_frame = data_array[:, :, frame_idx]
                dcm_folder = sample['DcmPathFlatten_meta_dict']['filename_or_obj'][0][len(config['DataSetPath']):]
                output_directory_idx = os.path.join(output_directory, dcm_folder)
                mkFolder(output_directory_idx)
                show_grayscale_image(data_array_frame, output_directory_idx, frame_idx)
                  #  input2d_2 = np.flip(np.rot90(np.rot90(np.rot90(input2d_2))), 1)

                frame = sample['inputs'][:,:,:,:,frame_idx]
                out_features = model.forward_features(frame)
                patch_feat = out_features['x_norm_patchtokens']
                pca_features, pca = compute_pca(dino_params, patch_feat)

                pca_rgb = plot_pca_rgb(pca_features, dino_params, config, output_directory_idx, patch_feat, pca, frame_idx)

                plot_pca(pca_features, dino_params, config, output_directory_idx, frame_idx)
                show_features_grayscale_image(data_array_frame, pca_rgb, output_directory_idx, frame_idx)                             
               # print('forwarining')
                
                

def get_dino_model(config, device, model_path):
    model, features = get_encoder(config, device)
    loaded_model = torch.load(
                    model_path,
                    map_location=device)

    model.load_state_dict(loaded_model)


    if config['model']['backbone'] =='dinov2_vits14':
        dino_params = dict({"patch_h": 37,
                        "patch_w": 37,
                        "feat_dim": features})
    else:
        ValueError('Not implemented')
    return model, dino_params

def feature_forward_dino(config, model_path, output_directory):
    config['loaders']['mode'] = 'prediction'

    config['loaders']['val_method']["samples"] = 1
    config['loaders']['batchSize'] = 1
    config['loaders']['val_method']["samples"] = 1


    config['loaders']['val_method']['saliency'] == 'True'

    device = get_device(config)

    if config["cpu"] == "False":
        torch.cuda.set_device(device)
        torch.backends.cudnn.benchmark = True
    config['datasetFingerprintFile'] = None
    #config['loss']['groups_names'], config['loss']['groups_counts'], \
    # config['loss']['group_idx'], config['groups_weights'] \
    #     = get_loss_names_groups(config)
    config['use_DDP'] = 'True'

    model, dino_params = get_dino_model(config, device, model_path)
    config['task_type'] = 'classification'
    test_loader = get_dataloader_test(config)


    get_patch_features(config, model, test_loader, dino_params, output_directory)
    # # Get loss func
    # criterion = get_loss_func(config)

    # pipeline = Predictor(model, criterion, config, device, test_loader)
    # pipeline.get_predictor_pipeline()


if __name__ == '__main__':
    config = vars(TestOptions().parse())
    config = read_log_file(config)
    if config['use_DDP'] == 'True':
        torch.distributed.init_process_group(
            backend="nccl" if config["cpu"] == "False" else "Gloo",
            init_method="env://")
    pred(config)
