# Generated with SMOP  0.41
from libsmop import *


# parse_test_yuv_name.m


def parse_test_yuv_name(input_filename=None):
    param_str = '(?<name>\w+)_(?<width>\d+)x(?<height>\d+)'
    # parse_test_yuv_name.m:4
    param_str_2 = '(?<name>\w+)_(?<height>\d+)p'
    # parse_test_yuv_name.m:5
    tokenNames = regexp(input_filename, param_str, 'names')
    # parse_test_yuv_name.m:7
    if isempty(tokenNames):
        # 'filename_720p'.
        tokenNames = regexp(input_filename, param_str_2, 'names')
        # parse_test_yuv_name.m:10
        imgHeight = str2num(tokenNames.height)
        # parse_test_yuv_name.m:11
        imgWidth = dot(imgHeight, 1280) / 720
    # parse_test_yuv_name.m:12
    else:
        imgWidth = str2num(tokenNames.width)
        # parse_test_yuv_name.m:14
        imgHeight = str2num(tokenNames.height)
    # parse_test_yuv_name.m:15

    seq_name = tokenNames.name
    # parse_test_yuv_name.m:17
    return seq_name, imgWidth, imgHeight
