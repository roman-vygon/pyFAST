# Generated with SMOP  0.41
from libsmop import *


# parse_all_saved_info.m


def parse_all_saved_info(dec_info=None):
    # ------------------------------------------------------------------------
    # Parse the dumped.txt
    # ------------------------------------------------------------------------
    PU_all, res_luma_all = parse_dumped_coeff_multiple_poc(dec_info.dump_txt_name, nargout=2)
    # parse_all_saved_info.m:7
    img_width = dec_info.enc_info.img_width
    # parse_all_saved_info.m:9
    img_height = dec_info.enc_info.img_height
    # parse_all_saved_info.m:10
    N_frames = length(PU_all)
    # parse_all_saved_info.m:11
    # ------------------------------------------------------------------------
    # For DEBUG ONLY!
    # ------------------------------------------------------------------------
    db_var = 0
    # parse_all_saved_info.m:16
    if db_var == 1:
        if logical_not(exist(fullfile(cd, 'temp_data'), 'dir')):
            mkdir(fullfile(cd, 'temp_data'))
        save(fullfile(cd, 'temp_data', 'db_parse_all_saved_info.mat'), 'dec_info', 'PU_all', 'res_luma_all',
             'img_width', 'img_height', 'N_frames')
        load(fullfile(cd, 'temp_data', 'db_parse_all_saved_info.mat'), 'dec_info', 'PU_all', 'res_luma_all',
             'img_width', 'img_height', 'N_frames')

    # ------------------------------------------------------------------------
    # Load the decoded sequence
    # ------------------------------------------------------------------------
    final_Y = load_Y_of_yuv(dec_info.enc_info.yuv_recon_name, img_width, img_height, N_frames)
    # parse_all_saved_info.m:33
    # ------------------------------------------------------------------------
    # Reconstruct Residue
    # ------------------------------------------------------------------------
    recon_res = cell(1, N_frames)
    # parse_all_saved_info.m:39
    for f_idx in arange(1, N_frames).reshape(-1):
        recon_res[f_idx] = reconstruct_res(res_luma_all[f_idx], concat([img_height, img_width]))
    # parse_all_saved_info.m:41

    # ------------------------------------------------------------------------
    # Reconstruct inter
    # ------------------------------------------------------------------------
    inter_mc, inter_mask, mv_x_map, mv_y_map = get_recon_inter(PU_all, final_Y, nargout=4)
    # parse_all_saved_info.m:48
    # ------------------------------------------------------------------------
    # Reconstruct intra
    # ------------------------------------------------------------------------
    intra_recon = cell(1, N_frames)
    # parse_all_saved_info.m:54
    for f_idx in arange(1, N_frames).reshape(-1):
        intra_recon[f_idx] = zeros(img_height, img_width)
        # parse_all_saved_info.m:56
        intra_mask_frame = inter_mask[f_idx] == 0
        # parse_all_saved_info.m:57
        intra_recon[f_idx][intra_mask_frame] = final_Y[f_idx](intra_mask_frame)
    # parse_all_saved_info.m:58

    # ------------------------------------------------------------------------
    # Output Other Information
    # ------------------------------------------------------------------------
    other_info = struct('PU', cellarray([PU_all]), 'TU', cellarray([res_luma_all]), 'mv_x', cellarray([mv_x_map]),
                        'mv_y', cellarray([mv_y_map]))
    # parse_all_saved_info.m:64
    return intra_recon, inter_mc, recon_res, inter_mask, other_info
