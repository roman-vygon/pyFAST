# Generated with SMOP  0.41
from libsmop import *


# parse_dumped_coeff_multiple_poc.m


def parse_dumped_coeff_multiple_poc(file_path=None):
    # Parse Multiple Frames. Parse Intra and MV.

    fid = fopen(file_path, 'r')
    # parse_dumped_coeff_multiple_poc.m:5
    line = fgetl(fid)
    # parse_dumped_coeff_multiple_poc.m:6
    PU_all = cellarray([])
    # parse_dumped_coeff_multiple_poc.m:7
    res_luma_all = cellarray([])
    # parse_dumped_coeff_multiple_poc.m:8
    tid = - 1
    # parse_dumped_coeff_multiple_poc.m:10
    res_frame_all = cell(1, 3)
    # parse_dumped_coeff_multiple_poc.m:12
    res_frame_all[1] = struct('x', cellarray([[]]), 'y', cellarray([[]]), 'w', cellarray([[]]), 'residual',
                              cellarray([[]]))
    # parse_dumped_coeff_multiple_poc.m:13
    res_frame_all[2] = struct('x', cellarray([[]]), 'y', cellarray([[]]), 'w', cellarray([[]]), 'residual',
                              cellarray([[]]))
    # parse_dumped_coeff_multiple_poc.m:14
    res_frame_all[3] = struct('x', cellarray([[]]), 'y', cellarray([[]]), 'w', cellarray([[]]), 'residual',
                              cellarray([[]]))
    # parse_dumped_coeff_multiple_poc.m:15
    PU_frame_all = struct('intra', cellarray([[]]), 'x', cellarray([[]]), 'y', cellarray([[]]), 'w', cellarray([[]]),
                          'h', cellarray([[]]), 'mv_x', cellarray([[]]), 'mv_y', cellarray([[]]), 't', cellarray([[]]),
                          't_r', cellarray([[]]), 'luma_mode', cellarray([[]]))
    # parse_dumped_coeff_multiple_poc.m:16
    while ischar(line):

        # Judge whether the line starts with one of the keywords.
        line_segments = strsplit(line, cellarray([':', ',', ' ']))
        # parse_dumped_coeff_multiple_poc.m:23
        if 'coeff' == lower(line_segments[1]):
            nums = cellstr2num(line_segments(arange(2, end())))
            # parse_dumped_coeff_multiple_poc.m:26
            qper = nums(1)
            # parse_dumped_coeff_multiple_poc.m:27
            qrem = nums(2)
            # parse_dumped_coeff_multiple_poc.m:28
            w = nums(3)
            # parse_dumped_coeff_multiple_poc.m:29
            list = nums(4)
            # parse_dumped_coeff_multiple_poc.m:30
            n = dot(w, w)
            # parse_dumped_coeff_multiple_poc.m:31
            if length(nums) != 4 + dot(4, n):
                fprintf('Last line reached!')
            scaling = nums(arange((4 + 1), (4 + n)))
            # parse_dumped_coeff_multiple_poc.m:35
            levels = nums(arange((4 + n + 1), (4 + dot(2, n))))
            # parse_dumped_coeff_multiple_poc.m:36
            try:
                coeffs = nums(arange((4 + dot(2, n) + 1), (4 + dot(2, n) + n)))
                # parse_dumped_coeff_multiple_poc.m:38
                residuals = nums(arange((4 + dot(2, n) + n + 1), (4 + dot(2, n) + n + n)))
            # parse_dumped_coeff_multiple_poc.m:39
            finally:
                pass
            res_frame_all[tid](end()).w = copy(w)
            # parse_dumped_coeff_multiple_poc.m:46
            res_frame_all[tid](end()).residual = copy(residuals)
            # parse_dumped_coeff_multiple_poc.m:47
            if all(levels == 0):
                #                 fprintf('Encountering an all-zero TU!\n');
                assert_(all(coeffs == 0) and all(residuals == 0),
                        'A TU with all zero scalings has non zero coeffs & residuals')
            tid = - 1
        # parse_dumped_coeff_multiple_poc.m:53
        else:
            if 'tu' == lower(line_segments[1]):
                nums = cellstr2num(line_segments(arange(2, end())))
                # parse_dumped_coeff_multiple_poc.m:56
                x = nums(1)
                # parse_dumped_coeff_multiple_poc.m:57
                y = nums(2)
                # parse_dumped_coeff_multiple_poc.m:58
                text = nums(3)
                # parse_dumped_coeff_multiple_poc.m:59
                intra = nums(4)
                # parse_dumped_coeff_multiple_poc.m:60
                #                 x, y, text, intra);
                # Initialize a TU
                res_struct = struct('x', cellarray([x]), 'y', cellarray([y]), 'w', cellarray([[]]), 'residual',
                                    cellarray([[]]))
                # parse_dumped_coeff_multiple_poc.m:66
                tid = max(text, 1)
                # parse_dumped_coeff_multiple_poc.m:68
                res_frame_all[tid][length(res_frame_all[tid]) + 1] = res_struct
            # parse_dumped_coeff_multiple_poc.m:69
            else:
                if 'intra' == lower(line_segments[1]):
                    prop_map = parse_prop(line_segments(arange(2, end())))
                    # parse_dumped_coeff_multiple_poc.m:71
                    PU_frame = struct('intra', cellarray([1]), 'x', cellarray([prop_map('x')]), 'y',
                                      cellarray([prop_map('y')]), 'w', cellarray([prop_map('w')]), 'h',
                                      cellarray([prop_map('h')]), 'mv_x', cellarray([[]]), 'mv_y', cellarray([[]]), 't',
                                      cellarray([prop_map('t')]), 't_r', cellarray([[]]), 'luma_mode',
                                      cellarray([prop_map('luma_mode')]))
                    # parse_dumped_coeff_multiple_poc.m:72
                    PU_frame_all[length(PU_frame_all) + 1] = PU_frame
                # parse_dumped_coeff_multiple_poc.m:77
                else:
                    if 'mv' == lower(line_segments[1]):
                        prop_map = parse_prop(line_segments(arange(2, end())))
                        # parse_dumped_coeff_multiple_poc.m:79
                        PU_frame = struct('intra', cellarray([0]), 'x', cellarray([prop_map('x')]), 'y',
                                          cellarray([prop_map('y')]), 'w', cellarray([prop_map('w')]), 'h',
                                          cellarray([prop_map('h')]), 'mv_x', cellarray([prop_map('mv_x')]), 'mv_y',
                                          cellarray([prop_map('mv_y')]), 't', cellarray([prop_map('t')]), 't_r',
                                          cellarray([prop_map('t_r')]), 'luma_mode', cellarray([[]]))
                        # parse_dumped_coeff_multiple_poc.m:80
                        PU_frame_all[length(PU_frame_all) + 1] = PU_frame
                    # parse_dumped_coeff_multiple_poc.m:86
                    else:
                        if 'poc' == lower(line_segments[1]):
                            fprintf('POC found! Start a new frame!\n')
                            res_luma_all[length(res_luma_all) + 1] = res_frame_all[1]
                            # parse_dumped_coeff_multiple_poc.m:89
                            PU_all[length(PU_all) + 1] = PU_frame_all
                            # parse_dumped_coeff_multiple_poc.m:90
                            res_frame_all = cell(1, 3)
                            # parse_dumped_coeff_multiple_poc.m:91
                            res_frame_all[1] = struct('x', cellarray([[]]), 'y', cellarray([[]]), 'w', cellarray([[]]),
                                                      'residual', cellarray([[]]))
                            # parse_dumped_coeff_multiple_poc.m:92
                            res_frame_all[2] = struct('x', cellarray([[]]), 'y', cellarray([[]]), 'w', cellarray([[]]),
                                                      'residual', cellarray([[]]))
                            # parse_dumped_coeff_multiple_poc.m:93
                            res_frame_all[3] = struct('x', cellarray([[]]), 'y', cellarray([[]]), 'w', cellarray([[]]),
                                                      'residual', cellarray([[]]))
                            # parse_dumped_coeff_multiple_poc.m:94
                            PU_frame_all = struct('intra', cellarray([[]]), 'x', cellarray([[]]), 'y', cellarray([[]]),
                                                  'w', cellarray([[]]), 'h', cellarray([[]]), 'mv_x', cellarray([[]]),
                                                  'mv_y', cellarray([[]]), 't', cellarray([[]]), 't_r', cellarray([[]]),
                                                  'luma_mode', cellarray([[]]))
                        # parse_dumped_coeff_multiple_poc.m:95
                        else:
                            fprintf('Unparsed statement: %s\n', line)
        line = fgetl(fid)
    # parse_dumped_coeff_multiple_poc.m:102

    fclose(fid)
    return PU_all, res_luma_all


def parse_prop(line=None):
    prop_map = containers.Map()
    # parse_dumped_coeff_multiple_poc.m:110
    for i in arange(1, length(line)).reshape(-1):
        vars = strsplit(line[i], '=')
        # parse_dumped_coeff_multiple_poc.m:112
        for t in arange(1, (length(vars) - 1)).reshape(-1):
            prop_map[vars[t]] = str2num(vars[end()])
    # parse_dumped_coeff_multiple_poc.m:114

    return prop_map
