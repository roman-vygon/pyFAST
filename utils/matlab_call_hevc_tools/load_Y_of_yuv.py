# Generated with SMOP  0.41
from libsmop import *
from utils.matlab_call_hevc_tools.loadFileYuv import loadFileYuv


def load_Y_of_yuv(filename=None, img_width=None, img_height=None, N_frames=None):
    final_Y = cell(1, N_frames)
    for f_idx in arange(1, N_frames).reshape(-1):
        _, _, yuv_img = loadFileYuv(filename, img_width, img_height, f_idx)
        final_Y[f_idx] = yuv_img[:, :, 1]

    return final_Y
