# Generated with SMOP  0.41
from libsmop import *
import numpy as np

# rgb2y_cell.m

def rgb2y_cell(rgb_cell=None):
    Y_cell = cell(size(rgb_cell))
    # rgb2y_cell.m:2
    img_height = size(rgb_cell[1], 1)
    # rgb2y_cell.m:4
    img_width = size(rgb_cell[1], 2)
    # rgb2y_cell.m:5
    for i in range(len(rgb_cell)):
        rgb_vec = np.reshape(rgb_cell[i], img_height*img_width), 3)
        # rgb2y_cell.m:8
        yuv_vec = convertRgbToYuv(rgb_vec)
        # rgb2y_cell.m:9
        Y_cell[i] = reshape(yuv_vec(arange(), 1), img_height, img_width)
    # rgb2y_cell.m:10

    return Y_cell
