# Generated with SMOP  0.41
from libsmop import *
# unit_test_downsample_encode.m

    # This script tests the pipeline to call the encoder, decoder of HEVC, and
# parse the dumped information to MATLAB.
    
    clc
    clear
    close_('all')
    # ------------------------------------------------------------------------
# Basic setup
# ------------------------------------------------------------------------
    seq_name='BQSquare'
# unit_test_downsample_encode.m:11
    num_frames=3
# unit_test_downsample_encode.m:12
    enc_params=make_encoding_param('num_frames',num_frames)
# unit_test_downsample_encode.m:13
    clip_dim=16
# unit_test_downsample_encode.m:14
    # ------------------------------------------------------------------------
# Read the sequence and downsample it!
# ------------------------------------------------------------------------
    yuv_filename,img_width,img_height=get_file_info_in_video_test_set(enc_params.test_yuv_dir,seq_name,nargout=3)
# unit_test_downsample_encode.m:19
    rgb_cell=load_rgb_cell_from_yuv(fullfile(enc_params.test_yuv_dir,yuv_filename),img_width,img_height,num_frames)
# unit_test_downsample_encode.m:21
    # ------------------------------------------------------------------------
# Downsample the image
# ------------------------------------------------------------------------
    rgb_half_cell=imdownsample_cell(rgb_cell,2,clip_dim)
# unit_test_downsample_encode.m:27
    # ------------------------------------------------------------------------
# Call the pipeline
# ------------------------------------------------------------------------
    enc_info=encode_sequence_from_cell(rgb_half_cell,seq_name,enc_params)
# unit_test_downsample_encode.m:32
    dec_info=get_dumped_information(enc_params,enc_info)
# unit_test_downsample_encode.m:33
    intra_recon,inter_mc,res_all,inter_mask,other_info=parse_all_saved_info(dec_info,nargout=5)
# unit_test_downsample_encode.m:34
    recon_together=combine_dumped_info(intra_recon,inter_mc,res_all,inter_mask)
# unit_test_downsample_encode.m:36
    # ------------------------------------------------------------------------
# Load the actual decoded video
# ------------------------------------------------------------------------
    ref_Y=load_Y_of_yuv(dec_info.enc_info.yuv_recon_name,dec_info.enc_info.img_width,dec_info.enc_info.img_height,num_frames)
# unit_test_downsample_encode.m:42
    # ------------------------------------------------------------------------
# Verify the results: Blockwise Comparison with CodecVisa
# ------------------------------------------------------------------------
# Variables to compare: Intra Recon vs Final, Residue vs True Residue,
# Inter prediction vs MC, motion vector
# Frames to compare: 1, 2, 3
    
    # Unfortunately, this has to be done interactively...
    
    frame_idx=3
# unit_test_downsample_encode.m:54
    cu_x=160
# unit_test_downsample_encode.m:55
    cu_y=40
# unit_test_downsample_encode.m:56
    w=8
# unit_test_downsample_encode.m:57
    h=8
# unit_test_downsample_encode.m:58
    # is_intra = '?';
    intra_final=intra_recon[frame_idx]
# unit_test_downsample_encode.m:61
    mc_pred=inter_mc[frame_idx]
# unit_test_downsample_encode.m:62
    res=res_all[frame_idx]
# unit_test_downsample_encode.m:63
    recon_frame=recon_together[frame_idx]
# unit_test_downsample_encode.m:64
    recon_gt=ref_Y[frame_idx]
# unit_test_downsample_encode.m:65
    mv_x=other_info.mv_x[frame_idx]
# unit_test_downsample_encode.m:66
    mv_y=other_info.mv_y[frame_idx]
# unit_test_downsample_encode.m:67
    fprintf('-------------------------------------------------------------\n')
    fprintf('intra final \n')
    blk_intra=intra_final(arange((cu_y + 1),(cu_y + h)),arange((cu_x + 1),(cu_x + w)))
# unit_test_downsample_encode.m:71
    fprintf('-------------------------------------------------------------\n')
    fprintf('inter mc\n')
    blk_inter_mc=mc_pred(arange((cu_y + 1),(cu_y + h)),arange((cu_x + 1),(cu_x + w)))
# unit_test_downsample_encode.m:75
    fprintf('-------------------------------------------------------------\n')
    fprintf('Residue \n')
    blk_res=res(arange((cu_y + 1),(cu_y + h)),arange((cu_x + 1),(cu_x + w)))
# unit_test_downsample_encode.m:79
    fprintf('-------------------------------------------------------------\n')
    fprintf('Recon all\n')
    blk_final=recon_frame(arange((cu_y + 1),(cu_y + h)),arange((cu_x + 1),(cu_x + w)))
# unit_test_downsample_encode.m:83
    fprintf('-------------------------------------------------------------\n')
    fprintf('Motion vector\n')
    mx=mv_x(arange((cu_y + 1),(cu_y + h)),arange((cu_x + 1),(cu_x + w)))
# unit_test_downsample_encode.m:87
    my=mv_y(arange((cu_y + 1),(cu_y + h)),arange((cu_x + 1),(cu_x + w)))
# unit_test_downsample_encode.m:88