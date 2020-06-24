# Generated with SMOP  0.41
from libsmop import *


# get_file_info_in_video_test_set.m


def get_file_info_in_video_test_set(test_dir=None, seq_name=None):
    dir_ent = dir(fullfile(test_dir, concat([seq_name, '*.yuv'])))
    # get_file_info_in_video_test_set.m:4
    if isempty(dir_ent):
        error('Could not find the file for the sequence!')

    seq_filename = dir_ent(1).name
    # get_file_info_in_video_test_set.m:8
    __, img_width, img_height = parse_test_yuv_name(seq_filename, nargout=3)
    # get_file_info_in_video_test_set.m:9
    return seq_filename, img_width, img_height
