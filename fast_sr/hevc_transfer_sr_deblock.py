# Generated with SMOP  0.41
from libsmop import *


# hevc_transfer_sr_deblock.m


def hevc_transfer_sr_deblock(sr_results=None, hevc_info=None, params=None):
    if logical_not(exist('params', 'var')):
        params = []
    # hevc_transfer_sr_deblock.m:5

    if logical_not(isfield(params, 'transfer_thresh')):
        params.transfer_thresh = copy(10)
    # hevc_transfer_sr_deblock.m:9

    if logical_not(isfield(params, 'deblock')):
        params.deblock = copy(1)
    # hevc_transfer_sr_deblock.m:13

    if logical_not(isfield(params, 'QP')):
        params.QP = copy(47)
    # hevc_transfer_sr_deblock.m:17

    b_debug = 0
    # hevc_transfer_sr_deblock.m:20
    # ------------------------------------------------------------------------
    # Parse Parameters
    # ------------------------------------------------------------------------
    N_frames = length(sr_results)
    # hevc_transfer_sr_deblock.m:24
    img_width = size(sr_results[1], 2)
    # hevc_transfer_sr_deblock.m:25
    img_height = size(sr_results[1], 1)
    # hevc_transfer_sr_deblock.m:26
    # ------------------------------------------------------------------------
    # Reconstruct low-resolution image
    # ------------------------------------------------------------------------
    recon_together = combine_dumped_info(hevc_info.intra_recon, hevc_info.inter_mc, hevc_info.res_all,
                                         hevc_info.inter_mask)
    # hevc_transfer_sr_deblock.m:31
    # ------------------------------------------------------------------------
    # Frame-by-frame transfer of high-resolution image
    # ------------------------------------------------------------------------
    img_h_transfer = cell(1, N_frames)
    # hevc_transfer_sr_deblock.m:37
    other_info = []
    # hevc_transfer_sr_deblock.m:38
    if params.deblock == 1:
        other_info.img_h_transfer_nodeblock = copy(cell(1, N_frames))
    # hevc_transfer_sr_deblock.m:40

    # I-frame
    img_h_transfer[1] = sr_results[1]
    # hevc_transfer_sr_deblock.m:44
    other_info.img_h_transfer_nodeblock[1] = sr_results[1]
    # hevc_transfer_sr_deblock.m:45
    # Perform a single threshold on the residue!

    # P-frames
    for f_idx in arange(2, N_frames).reshape(-1):
        tic
        img_h_transfer[f_idx] = zeros(img_height, img_width)
        # hevc_transfer_sr_deblock.m:52
        PU_now = hevc_info.other_info.PU[f_idx]
        # hevc_transfer_sr_deblock.m:53
        TU_now = hevc_info.other_info.TU[f_idx]
        # hevc_transfer_sr_deblock.m:54
        res_h = Blockwise_upsample_with_TU(hevc_info.res_all[f_idx], TU_now)
        # hevc_transfer_sr_deblock.m:57
        for pu_idx in arange(1, length(hevc_info.other_info.PU[f_idx])).reshape(-1):
            if isempty(PU_now(pu_idx).x) or isempty(PU_now(pu_idx).w):
                continue
            x_l = PU_now(pu_idx).x
            # hevc_transfer_sr_deblock.m:63
            y_l = PU_now(pu_idx).y
            # hevc_transfer_sr_deblock.m:64
            x_h = dot(2, x_l)
            # hevc_transfer_sr_deblock.m:65
            y_h = dot(2, y_l)
            # hevc_transfer_sr_deblock.m:66
            w = PU_now(pu_idx).w
            # hevc_transfer_sr_deblock.m:67
            h = PU_now(pu_idx).h
            # hevc_transfer_sr_deblock.m:68
            if 0 == PU_now(pu_idx).intra:
                # Inter prediction!
                # Decide whether to transfer or not by residue!
                res_l_patch = hevc_info.res_all[f_idx](arange((y_l + 1), (y_l + h)), arange((x_l + 1), (x_l + w)))
                # hevc_transfer_sr_deblock.m:75
                mean_ssd = sum(abs(ravel(res_l_patch))) / numel(res_l_patch)
                # hevc_transfer_sr_deblock.m:77
                if mean_ssd < params.transfer_thresh:
                    # Perform transfer
                    mv_x_h = dot(2, PU_now(pu_idx).mv_x) / 4
                    # hevc_transfer_sr_deblock.m:80
                    mv_y_h = dot(2, PU_now(pu_idx).mv_y) / 4
                    # hevc_transfer_sr_deblock.m:81
                    f_ref = PU_now(pu_idx).t_r + 1
                    # hevc_transfer_sr_deblock.m:82
                    ref_h_patch = sr_interpolate(img_h_transfer[f_ref], x_h, y_h, dot(2, w), dot(2, h), mv_x_h, mv_y_h)
                    # hevc_transfer_sr_deblock.m:84
                    #                     ref_h_patch = subpix_interp(img_h_transfer{f_ref}, ...
                    #                         (x_h + 1 + mv_x_h):(x_h + mv_x_h + 2 * w), ...
                    #                         (y_h + 1 + mv_y_h):(y_h + mv_y_h + 2 * h));
                    res_h_patch = res_h(arange((y_h + 1), (y_h + dot(2, h))), arange((x_h + 1), (x_h + dot(2, w))))
                    # hevc_transfer_sr_deblock.m:90
                    img_h_transfer[f_idx][arange((y_h + 1), (y_h + dot(2, h))), arange((x_h + 1), (
                                x_h + dot(2, w)))] = ref_h_patch + res_h_patch
                    # hevc_transfer_sr_deblock.m:95
                    if any(isnan(ravel(ref_h_patch))) or any(isnan(ravel(res_h_patch))):
                        db_var = 1
                # hevc_transfer_sr_deblock.m:98
                else:
                    # Otherwise: Prediction error is too large, perform
                    # bicubic interpolation on the low-res reconstruction
                    inter_patch = recon_together[f_idx](arange((y_l + 1), (y_l + h)), arange((x_l + 1), (x_l + w)))
                    # hevc_transfer_sr_deblock.m:103
                    img_h_transfer[f_idx][
                        arange((y_h + 1), (y_h + dot(2, h))), arange((x_h + 1), (x_h + dot(2, w)))] = imresize(
                        inter_patch, 2, 'bicubic')
                    # hevc_transfer_sr_deblock.m:106
                    if any(isnan(ravel(inter_patch))):
                        db_var = 1
            # hevc_transfer_sr_deblock.m:109
            else:
                if 1 == PU_now(pu_idx).intra:
                    # Intra prediction: Copy the intra prediction results, and
                    # SR!!
                    intra_patch = recon_together[f_idx](arange((y_l + 1), (y_l + h)), arange((x_l + 1), (x_l + w)))
                    # hevc_transfer_sr_deblock.m:115
                    if any(isnan(ravel(intra_patch))):
                        db_var = 1
                    # hevc_transfer_sr_deblock.m:118
                    img_h_transfer[f_idx][
                        arange((y_h + 1), (y_h + dot(2, h))), arange((x_h + 1), (x_h + dot(2, w)))] = imresize(
                        intra_patch, 2, 'bicubic')
                # hevc_transfer_sr_deblock.m:121
                else:
                    error('Intra indicator can only be 0 or 1 in PU!')
        t1 = copy(toc)
        # hevc_transfer_sr_deblock.m:128
        tic
        # Perform deblock if needed
        # --------------------------------------------------------------------
        if params.deblock == 1:
            # Perform deblocking on img_h_transfer{f_idx} according to PU and
            # TU structure.
            img_before_deblock = img_h_transfer[f_idx]
            # hevc_transfer_sr_deblock.m:139
            if b_debug == 1:
                imwrite(uint8(img_before_deblock),
                        fullfile(cd, '..', 'temp_data', sprintf('deblock_input_%d.bmp', f_idx)), 'BMP')
            # Generate the PU and TU boundary
            # Deblock the image vertically
            deblock_v_all = vertical_edge_deblock(img_before_deblock, params.QP)
            # hevc_transfer_sr_deblock.m:149
            deblock_v = copy(deblock_v_all)
            # hevc_transfer_sr_deblock.m:152
            deblock_h_all = vertical_edge_deblock(deblock_v.T, params.QP).T
            # hevc_transfer_sr_deblock.m:155
            deblock_h = copy(deblock_h_all)
            # hevc_transfer_sr_deblock.m:156
            img_h_transfer[f_idx] = deblock_h
            # hevc_transfer_sr_deblock.m:159
            other_info.img_h_transfer_nodeblock[f_idx] = img_before_deblock
        # hevc_transfer_sr_deblock.m:160
        t2 = copy(toc)
        # hevc_transfer_sr_deblock.m:162
        t_deblock = t2 / (t1 + t2)
    # hevc_transfer_sr_deblock.m:164

    return img_h_transfer, other_info