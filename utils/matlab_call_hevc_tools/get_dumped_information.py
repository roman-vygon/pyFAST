# Generated with SMOP  0.41
from libsmop import *
# get_dumped_information.m

    
@function
def get_dumped_information(enc_params=None,enc_info=None,*args,**kwargs):
    varargin = get_dumped_information.varargin
    nargin = get_dumped_information.nargin

    # Decode the sequence and get the dumped information
    
    if ismac:
        env_cmd='env PRINT_COEFF=1 PRINT_INTRA=1 PRINT_MV=1 SAVE_PREFILT=1'
# get_dumped_information.m:5
        enc_app=fullfile(enc_params.hm_bin_dir,'TAppDecoder')
# get_dumped_information.m:6
    else:
        if isunix:
            env_cmd='env PRINT_COEFF=1 PRINT_INTRA=1 PRINT_MV=1 SAVE_PREFILT=1'
# get_dumped_information.m:8
            enc_app=fullfile(enc_params.hm_bin_dir,'TAppDecoderStatic')
# get_dumped_information.m:9
        else:
            if ispc:
                env_cmd=concat(['set PRINT_COEFF=1 & set PRINT_INTRA=1',' & set PRINT_MV=1 & set SAVE_PREFILT=1 &'])
# get_dumped_information.m:11
                enc_app=fullfile(enc_params.hm_bin_dir,'TAppDecoder.exe')
# get_dumped_information.m:13
            else:
                error('The code can only run on Windows, Linux, Mac')
    
    binary_file=enc_info.binary_name
# get_dumped_information.m:18
    yuv_recon_file=enc_info.yuv_recon_name
# get_dumped_information.m:19
    dump_txt_name=fullfile(enc_info.dst_dir,concat([enc_info.seq_alias,'_dump.txt']))
# get_dumped_information.m:20
    dump_cmd=sprintf('%s %s -b %s -o %s > %s',env_cmd,enc_app,binary_file,yuv_recon_file,dump_txt_name)
# get_dumped_information.m:22
    system(dump_cmd)
    dec_info=struct('dump_txt_name',cellarray([dump_txt_name]))
# get_dumped_information.m:25
    dec_info.enc_info = copy(enc_info)
# get_dumped_information.m:26
    return dec_info
    
if __name__ == '__main__':
    pass
    