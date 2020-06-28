# Generated with SMOP  0.41
from libsmop import *
import glob
import ntpath

from utils.matlab_call_hevc_tools.parse_test_yuv_name import parse_test_yuv_name
# get_file_info_in_video_test_set.m


def get_file_info_in_video_test_set(test_dir=None, seq_name=None):
    dir_ent = glob.glob(os.path.join(test_dir, seq_name + '*.yuv'))

    if isempty(dir_ent):
        error('Could not find the file for the sequence!')

    seq_filename = ntpath.basename(dir_ent[0])
    print(seq_filename)
    _, img_width, img_height = parse_test_yuv_name(seq_filename)
    return seq_filename, img_width, img_height
