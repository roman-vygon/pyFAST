# Generated with SMOP  0.41
from libsmop import *
import re


# parse_test_yuv_name.m


def parse_test_yuv_name(input_filename=None):
    param_re = re.compile(r'(?P<name>\w+)_(?P<width>\d+)x(?P<height>\d+)')
    # parse_test_yuv_name.m:4
    param_re_2 = re.compile('(?P<name>\w+)_(?P<height>\d+)p')
    # parse_test_yuv_name.m:5
    tokenNames = struct()
    m = param_re.search(input_filename)
    tokenNames.name = m.group('name')
    tokenNames.width = m.group('width')
    tokenNames.height = m.group('height')

    # parse_test_yuv_name.m:7
    if isempty(tokenNames.width):
        # 'filename_720p'.
        tokenNames = struct()
        m = param_re_2.search(input_filename)
        tokenNames.name = m.group('name')
        tokenNames.height = m.group('height')
        # parse_test_yuv_name.m:10
        imgHeight = int(tokenNames.height)
        # parse_test_yuv_name.m:11
        imgWidth = (imgHeight * 1280) / 720
    # parse_test_yuv_name.m:12
    else:
        imgWidth = int(tokenNames.width)
        # parse_test_yuv_name.m:14
        imgHeight = int(tokenNames.height)
    # parse_test_yuv_name.m:15

    seq_name = tokenNames.name
    # parse_test_yuv_name.m:17
    return seq_name, imgWidth, imgHeight
