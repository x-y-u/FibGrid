"""
    coding: utf-8
    Project: FibGrid_data_trans
    File: samples_trans.py
    Author: xieyu
    Date: 2024/6/4 15:45
    IDE: PyCharm
"""

import h5py
import numpy as np
from dipy.data.fetcher import get_file_formats

import nibabel as nib

from data_preprocess.utils.dataset_specific_utils import *

from data_preprocess.utils.line_encode import lines_to_psdf_multi_cpu

import os
from dipy.io.streamline import load_tractogram
from tqdm import tqdm

from data_preprocess.utils.trans_data import Bundle_psdf_trans2_3D

channels = np.array([31, 31, 31, 15, 15, 15, 31, 31, 31, 31, 31, 31])

dataset_type = 2
bundle_names = get_bundle_names(dataset_type)
num_classes = len(bundle_names)
if dataset_type == 1:
    dataset_base_path = "/data/xieyu/atlas/ORG_AnatomicalTracts/"
    dataset_out_base_path = "/data/xieyu/unet3D_ORG_AnatomicalTracts/datasets/"
elif dataset_type == 2:
    # dataset_base_path = "/data/xieyu/atlas/Tracts39/"
    # dataset_out_base_path = "/data/xieyu/unet3D_Tracts39/datasets/"
    dataset_base_path = "/data/xieyu/atlas/Tracts39_test/"
    dataset_out_base_path = "/data/xieyu/unet3D_Tracts39/datasets_test/"
else:
    dataset_base_path = "/data/xieyu/tract_seg_data/BTC_data/"
    dataset_out_base_path = "/data/xieyu/unet3D_seg/BTC_data/"

dir_names = [name for name in os.listdir(dataset_base_path)]

references = nib.load("template0.nii.gz")

for dir_name in tqdm(dir_names):
    # bundle_base_path = os.path.join(dataset_base_path, f"{dir_name}/TOM_trackings")
    bundle_base_path = os.path.join(dataset_base_path, dir_name)
    if not os.path.isdir(bundle_base_path):
        continue
    sample_out_path = os.path.join(dataset_out_base_path, dir_name)
    if not os.path.exists(sample_out_path):
        os.mkdir(sample_out_path)
    if os.path.exists(os.path.join(sample_out_path, "f_img.nii")):
        continue
    betas = []
    indices = [0]
    for bundle_name in bundle_names:
        bundle_path = os.path.join(bundle_base_path, f"{bundle_name}.tck")
        cur_lines = load_tractogram(bundle_path, references, bbox_valid_check=False).streamlines
        cur_betas = lines_to_psdf_multi_cpu(cur_lines, 1)
        betas.extend(cur_betas)
        indices.append(len(betas))
    labels = np.zeros(len(betas))
    betas = np.array(betas)
    for i in range(num_classes):
        labels[indices[i]:indices[i + 1]] = i

    labels_path = os.path.join(sample_out_path, "labels.h5")
    with h5py.File(labels_path, 'w') as hf:
        hf['labels'] = labels

    bundle_trans = Bundle_psdf_trans2_3D(channels)

    # p, s, d, f = bundle_trans.trans_bundle(betas, sample_out_path, is_save_mask=True,
    #                                        labels=labels, num_classes=num_classes)
  
    p, s, d, f = bundle_trans.trans_bundle(betas, sample_out_path)

    betas_out_path = os.path.join(sample_out_path, "betas.h5")

    with h5py.File(betas_out_path, 'w') as hf:
        hf['positions'] = p
        hf['shapes'] = s
        hf['directions'] = d
        hf['regions'] = f






