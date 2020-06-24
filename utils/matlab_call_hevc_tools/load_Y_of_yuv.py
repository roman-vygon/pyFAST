# Generated with SMOP  0.41
from libsmop import *


# load_Y_of_yuv.m


def load_Y_of_yuv(filename=None, img_width=None, img_height=None, N_frames=None):
    final_Y = cell(1, N_frames)
    # load_Y_of_yuv.m:3
    for f_idx in arange(1, N_frames).reshape(-1):
        __, __, yuv_img = loadFileYuv(filename, img_width, img_height, f_idx, nargout=3)
        # load_Y_of_yuv.m:5
        final_Y[f_idx] = yuv_img(arange(), arange(), 1)
    # load_Y_of_yuv.m:6

    return final_Y
