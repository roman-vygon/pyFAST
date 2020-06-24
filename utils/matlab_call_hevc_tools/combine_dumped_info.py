# Generated with SMOP  0.41
from libsmop import *


def combine_dumped_info(intra_recon=None, inter_mc=None, res_all=None, inter_mask=None):
    N_frames = length(intra_recon)
    # combine_dumped_info.m:4
    img_width = size(intra_recon[1], 2)
    # combine_dumped_info.m:5
    img_height = size(intra_recon[1], 1)
    # combine_dumped_info.m:6
    recon_together = cell(1, N_frames)
    # combine_dumped_info.m:8
    for f_idx in arange(1, N_frames).reshape(-1):
        recon_frame = zeros(img_height, img_width)
        # combine_dumped_info.m:11
        intra_mask_frame = inter_mask[f_idx] == 0
        # combine_dumped_info.m:12
        recon_frame[intra_mask_frame] = intra_recon[f_idx](intra_mask_frame)
        # combine_dumped_info.m:13
        recon_frame[logical_not(intra_mask_frame)] = inter_mc[f_idx](logical_not(intra_mask_frame)) + res_all[f_idx](
            logical_not(intra_mask_frame))
        # combine_dumped_info.m:14
        recon_together[f_idx] = recon_frame
    # combine_dumped_info.m:16

    return recon_together

