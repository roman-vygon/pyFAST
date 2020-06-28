# Generated with SMOP  0.41
from libsmop import *
from fast_sr.hevc_transfer_sr import hevc_transfer_sr
from utils.matlab_call_hevc_tools.make_encoding_param import make_encoding_param
from utils.matlab_call_hevc_tools.get_file_info_in_video_test_set import get_file_info_in_video_test_set
import os
result_path = 'results'
if not os.path.exists(result_path):
    os.mkdir(result_path)

temp_path = 'temp'

if not os.path.exists(temp_path):
    os.mkdir(temp_path)

# ------------------------------------------------------------------------
# Add the paths of the sub-directories to the system path, and compile the
# mex if needed
# ------------------------------------------------------------------------


"""recompile_mex = 1
# start_fast_sr.m:21
if recompile_mex == 1:
    compile_mex_hevc_sr
"""

# ------------------------------------------------------------------------
# Configurations
# ------------------------------------------------------------------------

seq_name = 'calendar'
num_frames = 8
clip_dim = 16
QP = 27


# Although this is left as a parameter, there are few components where only
# sr_ratio = 2 is supported, right now.
sr_ratio = 2
method_name = 'CNN'

b_encode = 1
b_recall_sr = 1
b_make_plot = 1

# ------------------------------------------------------------------------
# Call HEVC to encode the sequence, and get the syntax elements
# ------------------------------------------------------------------------
save_file = 'temp/%s.dat' % seq_name


if b_encode == 1 or logical_not(exist(save_file, 'file')):
    # This function specifies where the HEVC dataset folder is
    enc_params = make_encoding_param(num_frames=num_frames, QP=QP)

    yuv_filename, img_width, img_height = get_file_info_in_video_test_set(enc_params.test_yuv_dir, seq_name)
    print(yuv_filename, img_height, img_width)

    #just load rgb frames
    rgb_cell = load_rgb_cell_from_yuv(fullfile(enc_params.test_yuv_dir, yuv_filename), img_width, img_height,
                                      num_frames)
    # start_fast_sr.m:57

    #convert tgb to ycbrb and get the Y component
    Y_high_res_gt = rgb2y_cell(rgb_cell)
    # start_fast_sr.m:59

    #downscale image
    rgb_half_cell = imdownsample_cell(rgb_cell, 2, clip_dim)
    # start_fast_sr.m:62
    #encode images with HEVC
    enc_info = encode_sequence_from_cell(rgb_half_cell, seq_name, enc_params)
    # start_fast_sr.m:65
    dec_info = get_dumped_information(enc_params, enc_info)
    # start_fast_sr.m:68
    intra_recon, inter_mc, res_all, inter_mask, other_info = parse_all_saved_info(dec_info, nargout=5)
    # start_fast_sr.m:69
    Y_low_res = load_Y_of_yuv(dec_info.enc_info.yuv_recon_name, dec_info.enc_info.img_width,
                              dec_info.enc_info.img_height, num_frames)
    # start_fast_sr.m:73
    hevc_info = struct('intra_recon', cellarray([intra_recon]), 'inter_mc', cellarray([inter_mc]), 'res_all',
                       cellarray([res_all]), 'inter_mask', cellarray([inter_mask]), 'other_info',
                       cellarray([other_info]))
    # start_fast_sr.m:77
    # there is a bug in this script later.
    save(save_file, 'Y_low_res', 'rgb_cell', 'Y_high_res_gt', 'dec_info', 'hevc_info')
else:
    load(save_file, 'Y_low_res', 'rgb_cell', 'Y_high_res_gt', 'dec_info', 'hevc_info')

# ------------------------------------------------------------------------
# Frame-by-frame SR
# ------------------------------------------------------------------------
sr_result_file = fullfile(cd, '..', 'temp_data', concat([seq_name, '_sr.mat']))
# start_fast_sr.m:95
if b_recall_sr == 1 or logical_not(exist(sr_result_file, 'file')):
    # We support multiple super-resolution methods to benchmark against,
    # but in this released code, we only include SRCNN to benchmark
    # against.
    sr_func = str2func(sprintf('SR_%s', method_name))
    # start_fast_sr.m:100
    sr_load_func = str2func(sprintf('SRload_%s', method_name))
    # start_fast_sr.m:101
    sr_model = sr_load_func()
    # start_fast_sr.m:102
    imgs_h_sr = cell(1, num_frames)
    # start_fast_sr.m:104
    imgs_h_bicubic = cell(1, num_frames)
    # start_fast_sr.m:105
    for i in arange(1, num_frames).reshape(-1):
        fprintf('Upsampling %d-th frame by %s\n', i, method_name)
        imgs_h_sr[i] = sr_func(Y_l
        ow_res[i], sr_ratio, sr_model)
        # start_fast_sr.m:108
        imgs_h_bicubic[i] = imresize(Y_low_res[i], sr_ratio, 'bicubic')
    # start_fast_sr.m:109
    save(sr_result_file, 'imgs_h_sr', 'imgs_h_bicubic')
else:
    load(sr_result_file, 'imgs_h_sr', 'imgs_h_bicubic')

for i in arange(1, num_frames).reshape(-1):
    imgs_h_sr[i] = double(imgs_h_sr[i])
# start_fast_sr.m:118

# ------------------------------------------------------------------------
# FAST algorithms
# ------------------------------------------------------------------------
imgs_h_transfer, other_info = hevc_transfer_sr(imgs_h_sr[1], num_frames, hevc_info, nargout=2)
# start_fast_sr.m:124
# ------------------------------------------------------------------------
# Compare the results
# ------------------------------------------------------------------------
# Crop the ground-truth image
crop_gt = cell(1, num_frames)
# start_fast_sr.m:131
for i in arange(1, num_frames).reshape(-1):
    crop_gt[i] = Y_high_res_gt[i](arange(1, size(imgs_h_sr[1], 1)), arange(1, size(imgs_h_sr[1], 2)))
# start_fast_sr.m:133

for i in arange(2, num_frames).reshape(-1):
    # --------------------------------------------------------------------
    # Visualize the SR results
    # --------------------------------------------------------------------
    imwrite(uint8(crop_gt[i]), sprintf('ground_truth_%d.bmp', i), 'BMP')
    if b_make_plot == 1:
        h = copy(figure)
        # start_fast_sr.m:145
        subplot(2, 2, 1)
        imshow(uint8(crop_gt[i]))
        title(sprintf('Frame %d, Ground-truth high-res', i))
    fprintf('------------------------------------------------\n')
    fprintf('- frame %d\n', i)
    psnr_bicubic = computePSNR(crop_gt[i], imgs_h_bicubic[i])
    # start_fast_sr.m:153
    fprintf('Bicubic psnr = %f\n', psnr_bicubic)
    if b_make_plot == 1:
        subplot(1, 3, 1)
        imshow(uint8(imgs_h_bicubic[i]))
        title(sprintf('Bicubic interpolation, psnr = %f', psnr_bicubic))
    psnr_sr = computePSNR(crop_gt[i], imgs_h_sr[i])
    # start_fast_sr.m:162
    fprintf('SR psnr = %f\n', psnr_sr)
    if b_make_plot == 1:
        subplot(1, 3, 2)
        imshow(uint8(imgs_h_sr[i]))
        title(sprintf('SR method %s, psnr = %f', method_name, psnr_sr))
    psnr_trans = computePSNR(crop_gt[i], imgs_h_transfer[i])
    # start_fast_sr.m:171
    fprintf('FAST psnr = %f\n', psnr_trans)
    if b_make_plot == 1:
        subplot(1, 3, 3)
        imshow(uint8(imgs_h_transfer[i]))
        title(sprintf('FAST psnr = %f', psnr_trans))
