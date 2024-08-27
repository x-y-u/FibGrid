"""
    coding: utf-8
    Project: graphSAGE-pytorch
    File: line_encode.py
    Author: xieyu
    Date: 2024/5/27 20:59
    IDE: PyCharm
"""

import numpy as np
import time
from joblib import Parallel, delayed

from scipy.interpolate import splprep, splev


def line_to_psf(index, line):
    k = 3
    f1 = line[0]
    f2 = line[-1]

    tract = line.T
    n_vertex = tract.shape[1]

    p0 = tract[:, :-1]
    p1 = tract[:, 1:]
    disp = p1 - p0

    L2 = np.sqrt(np.sum(disp ** 2, axis=0))

    arc_length = np.sum(L2)

    cum_len = np.cumsum(L2) / arc_length
    para = np.zeros(n_vertex)
    para[1:] = cum_len

    n_vertex = len(para)
    para_even = np.hstack((-para[::-1][1:], para))

    tract_even = np.hstack((tract[:, ::-1][:, 1:], tract))

    para_even = np.tile(para_even, (k + 1, 1)).T
    pi_factors = np.tile(np.arange(k + 1), (2 * n_vertex - 1, 1)) * np.pi
    Y = np.cos(para_even * pi_factors) * np.sqrt(2)

    # # 设置正则化参数
    # alpha = 1e-5
    #
    # # 正则化项
    # I = np.eye(Y.shape[1])

    beta = np.linalg.pinv(Y.T @ Y) @ Y.T @ tract_even.T

    return index, beta, f1, f2


def lines_to_psdf_multi_cpu(lines, number_of_jobs=1):
    result_betas = np.zeros((len(lines), 15))
    betas = np.zeros((len(lines), 4, 3))
    # time_start = time.time()
    results = Parallel(n_jobs=number_of_jobs, verbose=0)(
        delayed(line_to_psf)(
            index,
            line)
        for index, line in zip(range(0, len(lines)), lines))
    # print(time.time() - time_start)
    for result in results:
        index, beta, f1, f2 = result
        betas[index] = beta
        result_betas[index, 6:9] = f1
        result_betas[index, 9:12] = f2
        result_betas[index, 12:15] = f1-f2
    # print(time.time() - time_start)
    vecs = np.sqrt(np.sum(betas[:, 1:, :] ** 2, axis=-1))
    result_betas[:, 3:6] = vecs
    result_betas[:, 0:3] = betas[:, 0, :]
    # print(time.time() - time_start)
    return result_betas


