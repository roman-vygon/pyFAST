clc;
clear;
close all;

result_path = fullfile(cd, '..', 'results');
if ~exist(result_path, 'dir')
    mkdir(result_path);
end

temp_path = fullfile(cd, '..', 'temp_data');
if ~exist(temp_path, 'dir')
    mkdir(temp_path);
end

% ------------------------------------------------------------------------
% Add the paths of the sub-directories to the system path, and compile the
% mex if needed
% ------------------------------------------------------------------------
set_path;

recompile_mex = 1;
if recompile_mex == 1
    compile_mex_hevc_sr;
end

% ------------------------------------------------------------------------
% Configurations
% ------------------------------------------------------------------------
seq_name = 'calendar';
num_frames = 8; % Number of frames to play with
clip_dim = 16;
QP = 27; % Quantization level!

% Although this is left as a parameter, there are few components where only
% sr_ratio = 2 is supported, right now.
sr_ratio = 2; 

method_name = 'CNN'; % Use SRCNN as benchmark method

b_encode = 1; % If we've encoded once, we don't need to encode the video again.
b_recall_sr = 1; % If we've called SR on this sequence once, we don't need to call it again.
b_make_plot = 1; % Do we need plots or just numbers?

% ------------------------------------------------------------------------
% Call HEVC to encode the sequence, and get the syntax elements
% ------------------------------------------------------------------------
save_file = fullfile(cd, '..', 'temp_data', ...
    sprintf('%s_info.mat', seq_name)); % 

if b_encode == 1 || ~exist(save_file, 'file')
    % This function specifies where the HEVC dataset folder is
    enc_params = make_encoding_param('num_frames', num_frames, 'QP', QP);
    [yuv_filename, img_width, img_height] = ...
        get_file_info_in_video_test_set(enc_params.test_yuv_dir, seq_name);
    
    % Load the RGB cells
    rgb_cell = load_rgb_cell_from_yuv(fullfile(enc_params.test_yuv_dir, ...
        yuv_filename), img_width, img_height, num_frames);
    Y_high_res_gt = rgb2y_cell(rgb_cell);
    
    % Downsample the video sequence by 2
    rgb_half_cell = imdownsample_cell(rgb_cell, 2, clip_dim);
    
    % Call the encoding function
    enc_info = encode_sequence_from_cell(rgb_half_cell, seq_name, enc_params);
    
    % Get the syntax elements
    dec_info = get_dumped_information(enc_params, enc_info);
    [intra_recon, inter_mc, res_all, inter_mask, other_info] = ...
        parse_all_saved_info(dec_info);
    
    % Get the compressed low-resolution video
    Y_low_res = load_Y_of_yuv(dec_info.enc_info.yuv_recon_name, ...
        dec_info.enc_info.img_width, dec_info.enc_info.img_height, num_frames);
    
    % Data structure to hold all of the compressed information
    hevc_info = struct('intra_recon', {intra_recon}, ...
        'inter_mc', {inter_mc}, ...
        'res_all', {res_all}, ...
        'inter_mask', {inter_mask}, ...
        'other_info', {other_info});
    
    % Save them, so that we do not encode the same sequence again, in case
    % there is a bug in this script later.
    save(save_file, 'Y_low_res', 'rgb_cell', 'Y_high_res_gt', ...
        'dec_info', 'hevc_info');
else
    load(save_file, 'Y_low_res', 'rgb_cell', 'Y_high_res_gt', ...
        'dec_info', 'hevc_info');
end

% ------------------------------------------------------------------------
% Frame-by-frame SR
% ------------------------------------------------------------------------
sr_result_file = fullfile(cd, '..', 'temp_data', [seq_name, '_sr.mat']);
if b_recall_sr == 1 || ~exist(sr_result_file, 'file')
    % We support multiple super-resolution methods to benchmark against,
    % but in this released code, we only include SRCNN to benchmark
    % against.
    sr_func = str2func(sprintf('SR_%s', method_name));
    sr_load_func = str2func(sprintf('SRload_%s', method_name));
    sr_model = sr_load_func();
    
    imgs_h_sr = cell(1, num_frames);
    imgs_h_bicubic = cell(1, num_frames);
    for i = 1:num_frames
        fprintf('Upsampling %d-th frame by %s\n', i, method_name);
        imgs_h_sr{i} = sr_func(Y_low_res{i}, sr_ratio, sr_model);
        imgs_h_bicubic{i} = imresize(Y_low_res{i}, sr_ratio, 'bicubic');
    end
    
    save(sr_result_file, 'imgs_h_sr', 'imgs_h_bicubic');
else
    load(sr_result_file, 'imgs_h_sr', 'imgs_h_bicubic');
end

for i = 1:num_frames
    imgs_h_sr{i} = double(imgs_h_sr{i});
end

% ------------------------------------------------------------------------
% FAST algorithms
% ------------------------------------------------------------------------
[imgs_h_transfer, other_info] = hevc_transfer_sr(...
    imgs_h_sr{1}, num_frames, hevc_info);

% ------------------------------------------------------------------------
% Compare the results
% ------------------------------------------------------------------------
% Crop the ground-truth image
crop_gt = cell(1, num_frames);
for i = 1:num_frames
    crop_gt{i} = Y_high_res_gt{i}(1:size(imgs_h_sr{1}, 1), ...
        1:size(imgs_h_sr{1}, 2));
end

for i = 2:num_frames
    % --------------------------------------------------------------------
    % Visualize the SR results
    % --------------------------------------------------------------------
    
    imwrite(uint8(crop_gt{i}), sprintf('ground_truth_%d.bmp', i), 'BMP');
    
    if b_make_plot == 1
        h = figure;
        subplot(2, 2, 1);
        imshow(uint8(crop_gt{i}));
        title(sprintf('Frame %d, Ground-truth high-res', i));
    end
    
    fprintf('------------------------------------------------\n');
    fprintf('- frame %d\n', i);
    psnr_bicubic = computePSNR(crop_gt{i}, imgs_h_bicubic{i});
    fprintf('Bicubic psnr = %f\n', psnr_bicubic);
    
    if b_make_plot == 1
        subplot(1, 3, 1);
        imshow(uint8(imgs_h_bicubic{i}));
        title(sprintf('Bicubic interpolation, psnr = %f', psnr_bicubic));
    end
    
    psnr_sr = computePSNR(crop_gt{i}, imgs_h_sr{i});
    fprintf('SR psnr = %f\n', psnr_sr);
    
    if b_make_plot == 1
        subplot(1, 3, 2);
        imshow(uint8(imgs_h_sr{i}));
        title(sprintf('SR method %s, psnr = %f', method_name, psnr_sr));
    end
    
    psnr_trans = computePSNR(crop_gt{i}, imgs_h_transfer{i});
    fprintf('FAST psnr = %f\n', psnr_trans);
    
    if b_make_plot == 1
        subplot(1, 3, 3);
        imshow(uint8(imgs_h_transfer{i}));
        title(sprintf('FAST psnr = %f', psnr_trans));
    end
    
end