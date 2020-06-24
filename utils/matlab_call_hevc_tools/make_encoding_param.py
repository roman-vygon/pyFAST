# Generated with SMOP  0.41
from libsmop import *
# make_encoding_param.m

    
@function
def make_encoding_param(varargin=None,*args,**kwargs):
    varargin = make_encoding_param.varargin
    nargin = make_encoding_param.nargin

    filepath=mfilename('fullpath')
# make_encoding_param.m:3
    tool_folder_path,__,__=fileparts(filepath,nargout=3)
# make_encoding_param.m:4
    # ------------------------------------------------------------------------
# Default parameters
# ------------------------------------------------------------------------
    params.hm_main_dir = copy(fullfile(tool_folder_path,'hm'))
# make_encoding_param.m:9
    params.hm_bin_dir = copy(fullfile(params.hm_main_dir,'bin'))
# make_encoding_param.m:10
    params.cfg_dir = copy(fullfile(params.hm_main_dir,'cfg'))
# make_encoding_param.m:11
    params.cfg_sequence_dir = copy(fullfile(params.cfg_dir,'per-sequence'))
# make_encoding_param.m:12
    params.width = copy([])
# make_encoding_param.m:13
    params.height = copy([])
# make_encoding_param.m:14
    params.QP = copy([])
# make_encoding_param.m:15
    params.test_yuv_dir = copy(fullfile(cd,'data'))
# make_encoding_param.m:17
    params.main_cfg_setting = copy('encoder_lowdelay_P_main')
# make_encoding_param.m:19
    params.num_frames = copy([])
# make_encoding_param.m:21
    # ------------------------------------------------------------------------
# Parse the new parameters
# ------------------------------------------------------------------------
    for i in arange(1,length(varargin),2).reshape(-1):
        setattr(params,varargin[i],varargin[i + 1])
# make_encoding_param.m:27
    