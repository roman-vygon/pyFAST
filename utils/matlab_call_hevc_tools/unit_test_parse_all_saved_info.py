# Generated with SMOP  0.41
from libsmop import *
# unit_test_parse_all_saved_info.m

    # This script tests the pipeline to call the encoder, decoder of HEVC, and
# parse the dumped information to MATLAB.
    
    clc
    clear
    close_('all')
    # ------------------------------------------------------------------------
# Basic setup
# ------------------------------------------------------------------------
    seq_name='BQSquare'
# unit_test_parse_all_saved_info.m:11
    num_frames=3
# unit_test_parse_all_saved_info.m:12
    # ------------------------------------------------------------------------
# Call the pipeline
# ------------------------------------------------------------------------
    enc_params=make_encoding_param('num_frames',num_frames)
# unit_test_parse_all_saved_info.m:17
    enc_info=encode_sequence(seq_name,enc_params)
# unit_test_parse_all_saved_info.m:18
    dec_info=get_dumped_information(enc_params,enc_info)
# unit_test_parse_all_saved_info.m:19
    intra_recon,inter_mc,res_all,inter_mask,other_info=parse_all_saved_info(dec_info,nargout=5)
# unit_test_parse_all_saved_info.m:20
    recon_together=combine_dumped_info(intra_recon,inter_mc,res_all,inter_mask)
# unit_test_parse_all_saved_info.m:22
    # ------------------------------------------------------------------------
# Load the actual decoded video
# ------------------------------------------------------------------------
    ref_Y=load_Y_of_yuv(dec_info.enc_info.yuv_recon_name,dec_info.enc_info.img_width,dec_info.enc_info.img_height,num_frames)
# unit_test_parse_all_saved_info.m:28
    # ------------------------------------------------------------------------
# Verify the results: Blockwise Comparison with CodecVisa
# ------------------------------------------------------------------------
# Variables to compare: Intra Recon vs Final, Residue vs True Residue,
# Inter prediction vs MC, motion vector
# Frames to compare: 1, 2, 3
    
    # Unfortunately, this has to be done interactively...
    
    frame_idx=3
# unit_test_parse_all_saved_info.m:40
    cu_x=0
# unit_test_parse_all_saved_info.m:41
    cu_y=0
# unit_test_parse_all_saved_info.m:42
    w=16
# unit_test_parse_all_saved_info.m:43
    h=16
# unit_test_parse_all_saved_info.m:44
    # is_intra = '?';
    intra_final=intra_recon[frame_idx]
# unit_test_parse_all_saved_info.m:47
    mc_pred=inter_mc[frame_idx]
# unit_test_parse_all_saved_info.m:48
    res=res_all[frame_idx]
# unit_test_parse_all_saved_info.m:49
    recon_frame=recon_together[frame_idx]
# unit_test_parse_all_saved_info.m:50
    recon_gt=ref_Y[frame_idx]
# unit_test_parse_all_saved_info.m:51
    mv_x=other_info.mv_x[frame_idx]
# unit_test_parse_all_saved_info.m:52
    mv_y=other_info.mv_y[frame_idx]
# unit_test_parse_all_saved_info.m:53
    fprintf('-------------------------------------------------------------\n')
    fprintf('intra final \n')
    blk_intra=intra_final(arange((cu_y + 1),(cu_y + h)),arange((cu_x + 1),(cu_x + w)))
# unit_test_parse_all_saved_info.m:57
    fprintf('-------------------------------------------------------------\n')
    fprintf('inter mc\n')
    blk_inter_mc=mc_pred(arange((cu_y + 1),(cu_y + h)),arange((cu_x + 1),(cu_x + w)))
# unit_test_parse_all_saved_info.m:61
    fprintf('-------------------------------------------------------------\n')
    fprintf('Residue \n')
    blk_res=res(arange((cu_y + 1),(cu_y + h)),arange((cu_x + 1),(cu_x + w)))
# unit_test_parse_all_saved_info.m:65
    fprintf('-------------------------------------------------------------\n')
    fprintf('Recon all\n')
    blk_final=recon_frame(arange((cu_y + 1),(cu_y + h)),arange((cu_x + 1),(cu_x + w)))
# unit_test_parse_all_saved_info.m:69
    fprintf('-------------------------------------------------------------\n')
    fprintf('Motion vector\n')
    mx=mv_x(arange((cu_y + 1),(cu_y + h)),arange((cu_x + 1),(cu_x + w)))
# unit_test_parse_all_saved_info.m:73
    my=mv_y(arange((cu_y + 1),(cu_y + h)),arange((cu_x + 1),(cu_x + w)))
# unit_test_parse_all_saved_info.m:74