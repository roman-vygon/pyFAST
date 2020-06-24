# Generated with SMOP  0.41
from libsmop import *
# encode_sequence_from_cell.m

    
@function
def encode_sequence_from_cell(image_cells=None,seq_name=None,enc_params=None,enc_dir=None,*args,**kwargs):
    varargin = encode_sequence_from_cell.varargin
    nargin = encode_sequence_from_cell.nargin

    if logical_not(isfield(enc_params,'QP')):
        enc_params.QP = copy(27)
# encode_sequence_from_cell.m:5
    
    # image_cells:RGB data
    
    img_height=size(image_cells[1],1)
# encode_sequence_from_cell.m:9
    img_width=size(image_cells[1],2)
# encode_sequence_from_cell.m:10
    num_frames=length(image_cells)
# encode_sequence_from_cell.m:11
    yuv_name=sprintf('%s_%dx%d_%d',seq_name,img_width,img_height,num_frames)
# encode_sequence_from_cell.m:13
    yuv_filename=sprintf('%s.yuv',yuv_name)
# encode_sequence_from_cell.m:15
    if logical_not(exist('enc_dir','var')) or isempty(enc_dir):
        enc_dir=fullfile(cd,'..','temp_data',yuv_name)
# encode_sequence_from_cell.m:18
    
    if logical_not(exist(enc_dir,'dir')):
        mkdir(enc_dir)
    
    saveFileYuv(rgbcell2mov(image_cells),fullfile(enc_dir,yuv_filename),1)
    # Input arguments
    if ismac:
        enc_app=fullfile(enc_params.hm_bin_dir,'TAppEncoder')
# encode_sequence_from_cell.m:29
    else:
        if isunix:
            enc_app=fullfile(enc_params.hm_bin_dir,'TAppEncoderStatic')
# encode_sequence_from_cell.m:31
        else:
            if ispc:
                enc_app=fullfile(enc_params.hm_bin_dir,'TAppEncoder.exe')
# encode_sequence_from_cell.m:33
            else:
                error('The code can only run on Windows, Linux, Mac')
    
    cfg_main=fullfile(enc_params.cfg_dir,concat([enc_params.main_cfg_setting,'.cfg']))
# encode_sequence_from_cell.m:38
    cfg_sequence=fullfile(enc_params.cfg_sequence_dir,concat([seq_name,'.cfg']))
# encode_sequence_from_cell.m:40
    input_yuv=fullfile(enc_dir,yuv_filename)
# encode_sequence_from_cell.m:41
    # Output arguments
    yuv_recon_name=fullfile(enc_dir,concat([yuv_name,'_recon.yuv']))
# encode_sequence_from_cell.m:44
    binary_name=fullfile(enc_dir,concat([yuv_name,'.str']))
# encode_sequence_from_cell.m:45
    # Number of Frames
    other_arguments=sprintf('--FramesToBeEncoded=%d',num_frames)
# encode_sequence_from_cell.m:48
    # Image Width
    other_arguments=concat([other_arguments,sprintf(' --SourceWidth=%d --QP=%d',img_width,enc_params.QP)])
# encode_sequence_from_cell.m:51
    # Image Height
    other_arguments=concat([other_arguments,sprintf(' --SourceHeight=%d',img_height)])
# encode_sequence_from_cell.m:55
    enc_command=sprintf('%s -c %s -c %s -i %s -o %s -b %s %s',enc_app,cfg_main,cfg_sequence,input_yuv,yuv_recon_name,binary_name,other_arguments)
# encode_sequence_from_cell.m:58
    # Evaluate the command!
    system(enc_command)
    # Information about the encoding!
    enc_info=struct('yuv_recon_name',cellarray([yuv_recon_name]),'binary_name',cellarray([binary_name]),'img_width',cellarray([img_width]),'img_height',cellarray([img_height]),'dst_dir',cellarray([enc_dir]),'seq_alias',cellarray([yuv_name]))
# encode_sequence_from_cell.m:66
    return enc_info
    
if __name__ == '__main__':
    pass
    