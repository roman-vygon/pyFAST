# Generated with SMOP  0.41
from libsmop import *


def make_encoding_param(**kwargs):
    filepath = '.'
    # make_encoding_param.m:3
    tool_folder_path = os.path.join('.', 'utils', 'matlab_call_hevc_tools')
    # make_encoding_param.m:4
    # ------------------------------------------------------------------------
    # Default parameters
    # ------------------------------------------------------------------------
    params = struct()
    params.hm_main_dir = os.path.join(tool_folder_path, 'hm')
    params.hm_bin_dir = os.path.join(params.hm_main_dir, 'bin')

    params.cfg_dir = os.path.join(params.hm_main_dir, 'cfg')
    params.cfg_sequence_dir = os.path.join(params.cfg_dir, 'per-sequence')

    params.width = []
    params.height = []

    params.QP = []

    params.test_yuv_dir = os.path.join('.', 'data')

    params.main_cfg_setting = 'encoder_lowdelay_P_main'
    params.num_frames = []
    # ------------------------------------------------------------------------
    # Parse the new parameters
    # ------------------------------------------------------------------------
    for key in kwargs:
        setattr(params, key, kwargs[key])
    return params
