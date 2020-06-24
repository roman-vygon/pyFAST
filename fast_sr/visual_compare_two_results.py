# Generated with SMOP  0.41
from libsmop import *


# visual_compare_two_results.m


def visual_compare_two_results(m1_result=None, m2_result=None, ground_truth=None, params=None):
    if logical_not(exist('params', 'var')):
        params = []
    # visual_compare_two_results.m:4

    if logical_not(isfield(params, 'block_size')):
        params.block_size = copy(32)
    # visual_compare_two_results.m:8

    if logical_not(isfield(params, 'large_block_size')):
        large_block_size = dot(floor(100 / params.block_size), params.block_size)
        # visual_compare_two_results.m:12
        params.large_block_size = copy(large_block_size)
    # visual_compare_two_results.m:13

    if logical_not(isfield(params, 'interp_method')):
        params.interp_method = copy('bilinear')
    # visual_compare_two_results.m:17

    if logical_not(isfield(params, 'max_block_num')):
        params.max_block_num = copy(20)
    # visual_compare_two_results.m:21

    if logical_not(isfield(params, 'block_contrast_normalize')):
        params.block_contrast_normalize = copy(0)
    # visual_compare_two_results.m:25

    diff_1 = conv2((ground_truth - m1_result) ** 2, ones(params.block_size), 'valid')
    # visual_compare_two_results.m:28
    diff_2 = conv2((ground_truth - m2_result) ** 2, ones(params.block_size), 'valid')
    # visual_compare_two_results.m:30
    m1_gain = max(diff_2 - diff_1, 0)
    # visual_compare_two_results.m:33
    m2_gain = max(diff_1 - diff_2, 0)
    # visual_compare_two_results.m:34
    # ------------------------------------------------------------------------
    # Pick the positive patches!
    # ------------------------------------------------------------------------
    pos_patches = cell(params.max_block_num, 3)
    # visual_compare_two_results.m:39
    pos_loc = zeros(2, params.max_block_num)
    # visual_compare_two_results.m:40
    for i in arange(1, params.max_block_num).reshape(-1):
        v, idx = max(ravel(m1_gain), nargout=2)
        # visual_compare_two_results.m:42
        r, c = ind2sub(size(m1_gain), idx, nargout=2)
        # visual_compare_two_results.m:43
        pos_patches[i, 1] = m1_result(arange(r, (r + params.block_size - 1)), arange(c, (c + params.block_size - 1)))
        # visual_compare_two_results.m:44
        pos_patches[i, 2] = m2_result(arange(r, (r + params.block_size - 1)), arange(c, (c + params.block_size - 1)))
        # visual_compare_two_results.m:46
        pos_patches[i, 3] = ground_truth(arange(r, (r + params.block_size - 1)), arange(c, (c + params.block_size - 1)))
        # visual_compare_two_results.m:48
        pos_loc[arange(), i] = concat([[c], [r]])
        # visual_compare_two_results.m:51
        r0 = max(1, r - dot(2, params.block_size))
        # visual_compare_two_results.m:53
        r1 = min(size(diff_1, 1), r + dot(2, params.block_size))
        # visual_compare_two_results.m:54
        c0 = max(1, c - dot(2, params.block_size))
        # visual_compare_two_results.m:55
        c1 = min(size(diff_1, 2), c + dot(2, params.block_size))
        # visual_compare_two_results.m:56
        m1_gain[arange(r0, r1), arange(c0, c1)] = 0
    # visual_compare_two_results.m:57

    # ------------------------------------------------------------------------
    # Pick the negative patches!
    # ------------------------------------------------------------------------
    neg_patches = cell(params.max_block_num, 3)
    # visual_compare_two_results.m:63
    neg_loc = zeros(2, params.max_block_num)
    # visual_compare_two_results.m:64
    for i in arange(1, params.max_block_num).reshape(-1):
        __, idx = max(ravel(m2_gain), nargout=2)
        # visual_compare_two_results.m:66
        r, c = ind2sub(size(diff_1), idx, nargout=2)
        # visual_compare_two_results.m:67
        neg_patches[i, 1] = m1_result(arange(r, (r + params.block_size - 1)), arange(c, (c + params.block_size - 1)))
        # visual_compare_two_results.m:68
        neg_patches[i, 2] = m2_result(arange(r, (r + params.block_size - 1)), arange(c, (c + params.block_size - 1)))
        # visual_compare_two_results.m:70
        neg_patches[i, 3] = ground_truth(arange(r, (r + params.block_size - 1)), arange(c, (c + params.block_size - 1)))
        # visual_compare_two_results.m:72
        neg_loc[arange(), i] = concat([[c], [r]])
        # visual_compare_two_results.m:75
        r0 = max(1, r - dot(2, params.block_size))
        # visual_compare_two_results.m:77
        r1 = min(size(diff_1, 1), r + dot(2, params.block_size))
        # visual_compare_two_results.m:78
        c0 = max(1, c - dot(2, params.block_size))
        # visual_compare_two_results.m:79
        c1 = min(size(diff_1, 2), c + dot(2, params.block_size))
        # visual_compare_two_results.m:80
        m2_gain[arange(r0, r1), arange(c0, c1)] = 0
    # visual_compare_two_results.m:81

    # ------------------------------------------------------------------------
    # Concatenate pos and neg patches!
    # ------------------------------------------------------------------------
    all_patches = concat([pos_patches, neg_patches])
    # visual_compare_two_results.m:87
    for r in arange(1, size(all_patches, 1)).reshape(-1):
        for c in arange(1, size(all_patches, 2)).reshape(-1):
            if params.block_contrast_normalize == 1:
                all_patches[r, c] = histeq(uint8(all_patches[r, c]))
            # visual_compare_two_results.m:91
            all_patches[r, c] = imresize(all_patches[r, c], concat([params.large_block_size, params.large_block_size]),
                                         params.interp_method)
    # visual_compare_two_results.m:93

    h = copy(figure)
    # visual_compare_two_results.m:99
    imshow(uint8(ground_truth))
    hold('on')
    bs = params.block_size
    # visual_compare_two_results.m:102
    for i in arange(1, params.max_block_num).reshape(-1):
        plot(pos_loc(1, i) + concat([0, bs - 1, bs - 1, 0, 0]), pos_loc(2, i) + concat([0, 0, bs - 1, bs - 1, 0]), 'r-')
        hold('on')

    for i in arange(1, params.max_block_num).reshape(-1):
        plot(neg_loc(1, i) + concat([0, bs - 1, bs - 1, 0, 0]), neg_loc(2, i) + concat([0, 0, bs - 1, bs - 1, 0]), 'b-')
        hold('on')

    block_mark_img = frame2im(getframe(gca))
    # visual_compare_two_results.m:114
    close_(h)
    other_info = struct('pos_loc', cellarray([pos_loc]), 'neg_loc', cellarray([neg_loc]))
    # visual_compare_two_results.m:118
    cmp_image = cell2mat(all_patches)
# visual_compare_two_results.m:120
