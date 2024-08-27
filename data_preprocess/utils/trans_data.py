"""
    coding: utf-8
    Project: graphSAGE-pytorch
    File: trans_data.py
    Author: xieyu
    Date: 2024/5/27 21:44
    IDE: PyCharm
"""

import numpy as np

import os

import nibabel as nib


def generate_img(betas, shape, path):
    shape = shape + 1
    img = np.zeros((shape[0], shape[1], shape[2]))
    points = betas
    points = np.unique(points, axis=0).astype(int)
    for point in points:
        img[tuple(point)] += 1

    # 创建一个 NIfTI 图像对象
    nii_img = nib.Nifti1Image(img, affine=np.eye(4))

    # 保存为 NIfTI 文件
    nib.save(nii_img, path)


def save_mask(betas, labels, shape, num_classes, out_path):
    if betas.shape[0] != labels.shape[0]:
        labels = np.concatenate((labels, labels)).reshape(-1, 1)
    else:
        labels = labels.reshape(-1, 1)
    betas = np.hstack((betas, labels)).astype(int)
    betas = np.unique(betas, axis=0)
    shape = shape + 1
    mask = np.zeros((shape[0], shape[1], shape[2], num_classes))
    for beta in betas:
        mask[tuple(beta)] += 1

    # 创建一个 NIfTI 图像对象
    nii_mask = nib.Nifti1Image(mask, affine=np.eye(4))

    # 保存为 NIfTI 文件
    nib.save(nii_mask, out_path)


def single_feat_trans(feats, channels):
    min_values = np.min(feats, axis=0)
    max_values = np.max(feats, axis=0)
    origin_interval_len = (max_values - min_values) / channels
    interval_len = 1.1 * origin_interval_len
    min_values -= 0.05 * origin_interval_len
    max_values += 0.05 * origin_interval_len
    feats = ((feats - min_values) // interval_len)
    return feats


def betas_trans(betas, channels):

    p = betas[:, 0:3]
    s = betas[:, 3:6]
    d_neg = betas[:, 12:15].copy() * -1
    d = np.vstack((betas[:, 12:15], d_neg))/2
    d = np.vstack((p, p)) + d
    f = np.vstack((betas[:, 6:9], betas[:, 9:12]))

    p = single_feat_trans(p, channels[0:3])
    s = single_feat_trans(s, channels[3:6])
    d = single_feat_trans(d, channels[6:9])
    f = single_feat_trans(f, channels[9:12])

    return p, s, d, f


class Bundle_psdf_trans2_3D:
    def __init__(self, channels):
        self.channels = channels

    def trans_bundle(self, betas, out_base_path, is_save_mask=False, labels=None, num_classes=72):
        # betas = lines_to_psd_multi_cpu(lines, 4)
        # del lines
        # num_lines = betas.shape[0]
        p, s, d, f = betas_trans(betas, self.channels)

        if is_save_mask:
            save_mask(p, labels, self.channels[0:3], num_classes,
                      os.path.join(out_base_path, "p_mask.nii"))
            save_mask(s, labels, self.channels[3:6], num_classes,
                      os.path.join(out_base_path, "s_mask.nii"))
            save_mask(d, labels, self.channels[6:9], num_classes,
                      os.path.join(out_base_path, "d_mask.nii"))
            save_mask(f, labels, self.channels[9:12], num_classes,
                      os.path.join(out_base_path, "f_mask.nii"))

        img_p_out_path = os.path.join(out_base_path, "p_img.nii")
        img_s_out_path = os.path.join(out_base_path, "s_img.nii")
        img_d_out_path = os.path.join(out_base_path, "d_img.nii")
        img_f_out_path = os.path.join(out_base_path, "f_img.nii")

        generate_img(p, self.channels[0:3], img_p_out_path)
        generate_img(s, self.channels[3:6], img_s_out_path)
        generate_img(d, self.channels[6:9], img_d_out_path)
        generate_img(f, self.channels[9:12], img_f_out_path)

        # with h5py.File(os.path.join(out_base_path, "betas.h5"), 'w') as hf:
        #     hf['betas'] = betas
        return p, s, d, f

