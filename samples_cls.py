"""
    coding: utf-8
    Project: FibGrid_data_trans
    File: samples_cls.py
    Author: xieyu
    Date: 2024/6/4 16:28
    IDE: PyCharm
"""
import os

import h5py
import numpy as np
import nibabel as nib
from tqdm import tqdm

from data_preprocess.utils.dataset_specific_utils import get_bundle_names

dataset_base_path = "/data/xieyu/unet3D_Tracts39/datasets_test/"

dir_names = [name for name in os.listdir(dataset_base_path)]

bundle_names = get_bundle_names(2)

for dir_name in tqdm(dir_names):
    print(dir_name)
    sample_base_path = os.path.join(dataset_base_path, dir_name)
    if not os.path.isdir(sample_base_path):
        continue
    p_seg_result_path = os.path.join(sample_base_path, "p_seg_result.nii")
    s_seg_result_path = os.path.join(sample_base_path, "s_seg_result.nii")
    d_seg_result_path = os.path.join(sample_base_path, "d_seg_result.nii")
    f_seg_result_path = os.path.join(sample_base_path, "f_seg_result.nii")

    predict_labels_out_path = os.path.join(sample_base_path, "predict_labels.h5")

    betas_path = os.path.join(sample_base_path, "betas.h5")

    p_seg_result = nib.load(p_seg_result_path).get_fdata()
    s_seg_result = nib.load(s_seg_result_path).get_fdata()
    d_seg_result = nib.load(d_seg_result_path).get_fdata()
    f_seg_result = nib.load(f_seg_result_path).get_fdata()

    with h5py.File(betas_path, 'r') as hf:
        p = np.array(hf["positions"]).astype(int)
        s = np.array(hf["shapes"]).astype(int)
        d = np.array(hf["directions"]).astype(int)
        f = np.array(hf["regions"]).astype(int)

    num_lines = p.shape[0]
    print(num_lines)

    predict_labels = np.zeros(num_lines, dtype=int)
    for i in range(num_lines):
        cur_p = p[i]
        cur_s = s[i]
        cur_d = d[i]
        cur_d_neg = d[i + num_lines]
        cur_f = f[i]
        cur_f_neg = f[i + num_lines]

        p1 = p_seg_result[tuple(cur_p)]
        p2 = s_seg_result[tuple(cur_s)]
        p3 = d_seg_result[tuple(cur_d)]
        p4 = d_seg_result[tuple(cur_d_neg)]
        p5 = f_seg_result[tuple(cur_f)]
        p6 = f_seg_result[tuple(cur_f_neg)]
        p_result = p1 * p2 * p3 * p4 * p5 * p6
        is_all_zero = np.all(p_result == 0)
        if is_all_zero:
            predict_labels[i] = 0
        else:
            cur_class = np.argmax(p_result)
            predict_labels[i] = cur_class + 1

    with h5py.File(predict_labels_out_path, 'w') as hf:
        hf['labels'] = predict_labels
    
    real_labels_path = os.path.join(sample_base_path, "labels.h5")
    with h5py.File(real_labels_path, 'r') as hf:
        real_labels = np.array(hf['labels']) + 1
    print(dir_name, np.average(real_labels == predict_labels))
    break



