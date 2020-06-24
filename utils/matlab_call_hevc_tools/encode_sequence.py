# Generated with SMOP  0.41
from libsmop import *


# encode_sequence.m


@function
def encode_sequence(seq_name=None, enc_params=None):
    if logical_not(exist('enc_params', 'var')):
        enc_params = make_encoding_param()
    # encode_sequence.m:4

    # Find the exact file name
    dir_ent = dir(fullfile(enc_params.test_yuv_dir, concat([seq_name, '*.yuv'])))
    # encode_sequence.m:8
    if isempty(dir_ent):
        error('Could not find the file for the sequence!')

    yuv_filename = dir_ent(1).name
    # encode_sequence.m:12
    __, img_width, img_height = parse_test_yuv_name(yuv_filename, nargout=3)
    # encode_sequence.m:13
    # Input arguments
    enc_app = fullfile(enc_params.hm_bin_dir, 'TAppEncoderStatic')
    # encode_sequence.m:16
    cfg_main = fullfile(enc_params.cfg_dir, concat([enc_params.main_cfg_setting, '.cfg']))
    # encode_sequence.m:17
    cfg_sequence = fullfile(enc_params.cfg_sequence_dir, concat([seq_name, '.cfg']))
    # encode_sequence.m:19
    input_yuv = fullfile(enc_params.test_yuv_dir, yuv_filename)
    # encode_sequence.m:20
    # Output arguments
    yuv_recon_dir = fullfile(cd, 'enc_files')
    # encode_sequence.m:23
    if logical_not(exist(yuv_recon_dir, 'dir')):
        mkdir(yuv_recon_dir)

    enc_alias = sprintf('%s_%d', seq_name, enc_params.num_frames)
    # encode_sequence.m:28
    yuv_recon_name = fullfile(yuv_recon_dir, concat([enc_alias, '.yuv']))
    # encode_sequence.m:29
    binary_name = fullfile(yuv_recon_dir, concat([enc_alias, '.str']))
    # encode_sequence.m:30
    # Other arguments
    other_arguments = []
    # encode_sequence.m:33
    if logical_not(isempty(enc_params.num_frames)):
        other_arguments = concat([other_arguments, sprintf('--FramesToBeEncoded=%d', enc_params.num_frames)])
    # encode_sequence.m:35

    enc_command = sprintf('%s -c %s -c %s -i %s -o %s -b %s %s', enc_app, cfg_main, cfg_sequence, input_yuv,
                          yuv_recon_name, binary_name, other_arguments)
    # encode_sequence.m:38
    # Evaluate the command!
    system(enc_command)
    # Information about the encoding!
    enc_info = struct('yuv_recon_name', cellarray([yuv_recon_name]), 'binary_name', cellarray([binary_name]),
                      'img_width', cellarray([img_width]), 'img_height', cellarray([img_height]), 'dst_dir',
                      cellarray([yuv_recon_dir]), 'seq_alias', cellarray([enc_alias]))
    # encode_sequence.m:46
    return enc_info