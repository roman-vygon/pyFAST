# Generated with SMOP  0.41
from libsmop import *
from fast_sr.Blockwise_upsample_with_TU import Blockwise_upsample_with_TU
from fast_sr.sr_interpolate import sr_interpolate
from utils.matlab_call_hevc_tools.combine_dumped_info import combine_dumped_info
# hevc_transfer_sr.m


def hevc_transfer_sr(sr_result=None, N_frames=None, hevc_info=None, params=None):
    if params is None:
        params = {}

    if 'tranfer_thresh' not in params:
        params['transfer_thresh'] = 10

    if 'deblock' not in params:
        params['deblock'] = 1

    if 'QP' not in params:
        params['QP'] = 47

    # ------------------------------------------------------------------------
    # Parse Parameters
    # ------------------------------------------------------------------------
    img_width = sr_result.shape[1]
    img_height = sr_result.shape[0]

    # ------------------------------------------------------------------------
    # Reconstruct low-resolution image
    # ------------------------------------------------------------------------
    recon_together = combine_dumped_info(hevc_info.intra_recon, hevc_info.inter_mc, hevc_info.res_all,
                                         hevc_info.inter_mask)
    # hevc_transfer_sr.m:30
    # ------------------------------------------------------------------------
    # Frame-by-frame transfer of high-resolution image
    # ------------------------------------------------------------------------
    img_h_transfer = cell(1, N_frames)
    # hevc_transfer_sr.m:36
    other_info = []
    # hevc_transfer_sr.m:37
    # I-frame
    img_h_transfer[1] = sr_result
    # hevc_transfer_sr.m:40
    other_info.runtime = copy(zeros(1, N_frames))
    # hevc_transfer_sr.m:41
    # Perform a single threshold on the residue!

    # P-frames
    for f_idx in arange(2, N_frames).reshape(-1):
        tic
        img_h_transfer[f_idx] = zeros(img_height, img_width)
        # hevc_transfer_sr.m:47
        PU_now = hevc_info.other_info.PU[f_idx]
        # hevc_transfer_sr.m:48
        TU_now = hevc_info.other_info.TU[f_idx]
        # hevc_transfer_sr.m:49
        res_h = Blockwise_upsample_with_TU(hevc_info.res_all[f_idx], TU_now)
        # hevc_transfer_sr.m:52
        for pu_idx in arange(1, length(hevc_info.other_info.PU[f_idx])).reshape(-1):
            if isempty(PU_now(pu_idx).x) or isempty(PU_now(pu_idx).w):
                continue
            x_l = PU_now(pu_idx).x
            # hevc_transfer_sr.m:58
            y_l = PU_now(pu_idx).y
            # hevc_transfer_sr.m:59
            x_h = dot(2, x_l)
            # hevc_transfer_sr.m:60
            y_h = dot(2, y_l)
            # hevc_transfer_sr.m:61
            w = PU_now(pu_idx).w
            # hevc_transfer_sr.m:62
            h = PU_now(pu_idx).h
            # hevc_transfer_sr.m:63
            if 0 == PU_now(pu_idx).intra:
                # Inter prediction!
                # Decide whether to transfer or not by residue!
                res_l_patch = hevc_info.res_all[f_idx](arange((y_l + 1), (y_l + h)), arange((x_l + 1), (x_l + w)))
                # hevc_transfer_sr.m:70
                #                 dy_patch = conv2(res_l_patch, [-1; 1], 'valid');
                #                 mean_diff = (sum(abs(dx_patch(:))) + ...
                #                     sum(abs(dy_patch(:)))) / numel(res_l_patch);
                mean_ssd = sum(abs(ravel(res_l_patch))) / numel(res_l_patch)
                # hevc_transfer_sr.m:76
                if mean_ssd < params.transfer_thresh:
                    #                 if mean_diff < params.transfer_thresh
                    # Perform transfer
                    mv_x_h = dot(2, PU_now(pu_idx).mv_x) / 4
                    # hevc_transfer_sr.m:80
                    mv_y_h = dot(2, PU_now(pu_idx).mv_y) / 4
                    # hevc_transfer_sr.m:81
                    f_ref = PU_now(pu_idx).t_r + 1
                    # hevc_transfer_sr.m:82
                    ref_h_patch = sr_interpolate(img_h_transfer[f_ref], x_h, y_h, dot(2, w), dot(2, h), mv_x_h, mv_y_h)
                    # hevc_transfer_sr.m:84
                    #                         (x_h + 1 + mv_x_h):(x_h + mv_x_h + 2 * w), ...
                    #                         (y_h + 1 + mv_y_h):(y_h + mv_y_h + 2 * h));
                    res_h_patch = res_h(arange((y_h + 1), (y_h + dot(2, h))), arange((x_h + 1), (x_h + dot(2, w))))
                    # hevc_transfer_sr.m:90
                    img_h_transfer[f_idx][arange((y_h + 1), (y_h + dot(2, h))), arange((x_h + 1), (
                            x_h + dot(2, w)))] = ref_h_patch + res_h_patch
                    # hevc_transfer_sr.m:95
                    if any(isnan(ravel(ref_h_patch))) or any(isnan(ravel(res_h_patch))):
                        db_var = 1
                # hevc_transfer_sr.m:98
                else:
                    # Otherwise: Prediction error is too large, perform
                    # bicubic interpolation on the low-res reconstruction
                    inter_patch = recon_together[f_idx](arange((y_l + 1), (y_l + h)), arange((x_l + 1), (x_l + w)))
                    # hevc_transfer_sr.m:103
                    img_h_transfer[f_idx][
                        arange((y_h + 1), (y_h + dot(2, h))), arange((x_h + 1), (x_h + dot(2, w)))] = imresize(
                        inter_patch, 2, 'bicubic')
                    # hevc_transfer_sr.m:106
                    if any(isnan(ravel(inter_patch))):
                        db_var = 1
            # hevc_transfer_sr.m:109
            else:
                if 1 == PU_now(pu_idx).intra:
                    # Intra prediction: Copy the intra prediction results, and
                    # SR!!
                    intra_patch = recon_together[f_idx](arange((y_l + 1), (y_l + h)), arange((x_l + 1), (x_l + w)))
                    # hevc_transfer_sr.m:115
                    if any(isnan(ravel(intra_patch))):
                        db_var = 1
                    # hevc_transfer_sr.m:118
                    img_h_transfer[f_idx][
                        arange((y_h + 1), (y_h + dot(2, h))), arange((x_h + 1), (x_h + dot(2, w)))] = imresize(
                        intra_patch, 2, 'bicubic')
                # hevc_transfer_sr.m:121
                else:
                    error('Intra indicator can only be 0 or 1 in PU!')
        # --------------------------------------------------------------------
        # Perform deblock if needed
        # --------------------------------------------------------------------
        if params.deblock == 1:
            # Perform deblocking on img_h_transfer{f_idx} according to PU and
            # TU structure.
            # Deblock the image vertically
            deblock_v_all = deblock_mex(int32(img_h_transfer[f_idx]))
            # hevc_transfer_sr.m:135
            deblock_h_all = deblock_mex(deblock_v_all.T).T
            # hevc_transfer_sr.m:138
            deblock_h = double(deblock_h_all)
            # hevc_transfer_sr.m:139
            img_h_transfer[f_idx] = deblock_h
        # hevc_transfer_sr.m:142
        other_info.runtime[f_idx] = toc
    # hevc_transfer_sr.m:146

    return img_h_transfer, other_info