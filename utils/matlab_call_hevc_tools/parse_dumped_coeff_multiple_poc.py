# Generated with SMOP  0.41
from libsmop import *

# parse_dumped_coeff_multiple_poc.m


from libsmop import *


def parse_prop(line):
    prop_map = {}
    for prop in line:

        propvar = prop.split('=')
        for x in propvar[:-1]:
            prop_map[x] = int(propvar[-1])
    return prop_map


def parse_dumped_coeff_multiple_poc(file_path):
    # Parse Multiple Frames. Parse Intra and MV.
    f = open(file_path, 'r')

    tid = -1
    PU_all = []

    res_luma_all = cellarray([])

    res_frame_all = cell(1, 3)
    # res_frame_all[1] = struct('x', cellarray([[]]), 'y', cellarray([[]]), 'w', cellarray([[]]), 'residual',
    #                          cellarray([[]]))
    # res_frame_all[2] = struct('x', cellarray([[]]), 'y', cellarray([[]]), 'w', cellarray([[]]), 'residual',
    #                          cellarray([[]]))
    # res_frame_all[3] = struct('x', cellarray([[]]), 'y', cellarray([[]]), 'w', cellarray([[]]), 'residual',
    #                          cellarray([[]]))
    PU_frame_all = []
    # = struct('intra', cellarray([[]]), 'x', cellarray([[]]), 'y', cellarray([[]]), 'w', cellarray([[]]),
    #                      'h', cellarray([[]]), 'mv_x', cellarray([[]]), 'mv_y', cellarray([[]]), 't', cellarray([[]]),
    #                      't_r', cellarray([[]]), 'luma_mode', cellarray([[]]))

    import re
    for line in f:

        # Judge whether the line starts with one of the keywords.
        line_segments = re.split(r'[:, ]', line.replace('\n', ''))
        # print(line_segments)
        line_segments = [x for x in line_segments if len(x) > 0]
        # print(line_segments)
        if (len(line_segments) == 0):
            continue
        if 'coeff' == line_segments[0].lower():
            nums = list(map(int, line_segments[1:]))

            qper = nums[0]

            qrem = nums[1]

            w = nums[2]

            lst = nums[3]

            n = w * w

            if len(nums) != 4 + 4 * n:
                print('Last line reached!')
                break
            scaling = nums[4:4 + n];
            levels = nums[4 + n:4 + 2 * n]

            coeffs = nums[4 + 2 * n + 1:4 + 2 * n + n]
            residuals = nums[4 + 2 * n + n + 1:4 + 2 * n + n + n]

            res_frame_all[tid].w = w

            res_frame_all[tid].residual = residuals

            if all(levels == 0):
                #                 fprintf('Encountering an all-zero TU!\n');
                assert_(all(coeffs == 0) and all(residuals == 0),
                        'A TU with all zero scalings has non zero coeffs & residuals')
            tid = -1

        elif line_segments[0].lower() == 'tu':
            nums = list(map(int, line_segments[1:]))

            x = nums[0]

            y = nums[1]

            text = nums[2]

            intra = nums[3]

            #                 x, y, text, intra);
            # Initialize a TU
            res_struct = struct('x', cellarray([x]), 'y', cellarray([y]), 'w', cellarray([[]]), 'residual',
                                cellarray([[]]))

            tid = builtins.max(text, 1)

            res_frame_all[tid] = res_struct

        elif line_segments[0].lower() == 'intra':
            prop_map = parse_prop(line_segments[1:])
            PU_frame = struct('intra', cellarray([1]), 'x', cellarray([prop_map['x']]), 'y',
                              cellarray([prop_map['y']]), 'w', cellarray([prop_map['w']]), 'h',
                              cellarray([prop_map['h']]), 'mv_x', cellarray([[]]), 'mv_y', cellarray([[]]), 't',
                              cellarray([prop_map['t']]), 't_r', cellarray([[]]), 'luma_mode',
                              cellarray([prop_map['luma_mode']]))
            # print(PU_frame_all)
            PU_frame_all.append(PU_frame)
        elif line_segments[0].lower() == 'mv':
            prop_map = parse_prop(line_segments[1:])
            PU_frame = struct('intra', cellarray([0]), 'x', cellarray([prop_map['x']]), 'y',
                              cellarray([prop_map['y']]), 'w', cellarray([prop_map['w']]), 'h',
                              cellarray([prop_map['h']]), 'mv_x', cellarray([prop_map['mv_x']]), 'mv_y',
                              cellarray([prop_map['mv_y']]), 't', cellarray([prop_map['t']]), 't_r',
                              cellarray([prop_map['t_r']]), 'luma_mode', cellarray([[]]))
            PU_frame_all.append(PU_frame)
        elif line_segments[0].lower() == 'poc':
            print('POC found! Start a new frame!\n')
            res_luma_all[length(res_luma_all) + 1] = res_frame_all[1]
            PU_all.append(PU_frame_all)
            res_frame_all = cell(1, 3)
            # res_frame_all[1] = struct('x', cellarray([[]]), 'y', cellarray([[]]), 'w', cellarray([[]]),
            #                          'residual', cellarray([[]]))
            # res_frame_all[2] = struct('x', cellarray([[]]), 'y', cellarray([[]]), 'w', cellarray([[]]),
            #                          'residual', cellarray([[]]))
            # res_frame_all[3] = struct('x', cellarray([[]]), 'y', cellarray([[]]), 'w', cellarray([[]]),
            #                          'residual', cellarray([[]]))
            PU_frame_all = []  # struct('intra', cellarray([[]]), 'x', cellarray([[]]), 'y', cellarray([[]]),
            #     'w', cellarray([[]]), 'h', cellarray([[]]), 'mv_x', cellarray([[]]),
            #     'mv_y', cellarray([[]]), 't', cellarray([[]]), 't_r', cellarray([[]]),
            #     'luma_mode', cellarray([[]]))
        else:
            print('Unparsed statement: %s\n' % line)

    f.close()
    return PU_all, res_luma_all
