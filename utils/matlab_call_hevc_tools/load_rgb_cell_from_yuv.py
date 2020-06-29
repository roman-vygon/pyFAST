# Generated with SMOP  0.41
from libsmop import *
from utils.matlab_call_hevc_tools.loadFileYuv import loadFileYuv

# load_rgb_cell_from_yuv.m


def load_rgb_cell_from_yuv(yuv_path=None, img_width=None, img_height=None, num_frames=None):
    rgb_cell = []
    for i in range(num_frames):
        rgb_cell[i] = loadFrameYuv(yuv_path, img_width, img_height, i)

    return rgb_cell
