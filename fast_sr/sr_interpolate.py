# Generated with SMOP  0.41
from libsmop import *


# sr_interpolate.m


def sr_interpolate(img_h_sr=None, x=None, y=None, w=None, h=None, mv_x=None, mv_y=None):
    # w, h are real fractional!
    xp = x + floor(mv_x + 0.01)
    # sr_interpolate.m:3
    yp = y + floor(mv_y + 0.01)
    # sr_interpolate.m:4
    ref_patch = get_reference_patch_sr(img_h_sr, yp + 1, xp + 1, w, h)
    # sr_interpolate.m:5
    mv_x_ind = mod(round(dot(mv_x, 4)), 4)
    # sr_interpolate.m:7
    mv_y_ind = mod(round(dot(mv_y, 4)), 4)
    # sr_interpolate.m:8
    patch = fractional_interpolate_sr(ref_patch, mv_x_ind, mv_y_ind)
    # sr_interpolate.m:9
    # [X, Y] = meshgrid(3 + mv_x_ind / 4 + (1:w), 3 + mv_y_ind / 4 + (1:h));
    # patch = min(max(round(interp2(ref_patch, X, Y, 'cubic')), 0), 255);

    return patch


def get_reference_patch_sr(input_image=None, r=None, c=None, w=None, h=None):
    r0 = r - 3
    # sr_interpolate.m:18
    r1 = r + h - 1 + 4
    # sr_interpolate.m:19
    c0 = c - 3
    # sr_interpolate.m:20
    c1 = c + w - 1 + 4
    # sr_interpolate.m:21
    X = arange(c0, c1)
    # sr_interpolate.m:23
    Y = arange(r0, r1)
    # sr_interpolate.m:24
    X_clip = min(max(X, 1), size(input_image, 2))
    # sr_interpolate.m:25
    Y_clip = min(max(Y, 1), size(input_image, 1))
    # sr_interpolate.m:26
    ref_patch = input_image(Y_clip, X_clip)
    # sr_interpolate.m:28
    # 
    # r0_clip = max(r0, 1);
    # c0_clip = max(c0, 1);
    # r1_clip = min(r1, size(input_image, 1));
    # c1_clip = min(c1, size(input_image, 2));
    #
    # clip_patch = input_image(r0_clip:r1_clip, c0_clip:c1_clip);
    # if r0 < r0_clip
    #     clip_patch = padarray(clip_patch, [r0_clip - r0, 0], 'pre', 'replicate');
    # end
    #
    # if r1 > r1_clip
    #     clip_patch = padarray(clip_patch, [r1 - r1_clip, 0], 'post', 'replicate');
    # end
    #
    # if c0 < c0_clip
    #     clip_patch = padarray(clip_patch, [0, c0_clip - c0], 'pre', 'replicate');
    # end
    #
    # if c1 > c1_clip
    #     clip_patch = padarray(clip_patch, [0, c1 - c1_clip], 'post', 'replicate');
    # end
    #
    # ref_patch = clip_patch;
    return ref_patch


if __name__ == '__main__':
    pass


def fractional_interpolate_sr(refer_patch=None, mv_x_ind=None, mv_y_ind=None):
    filter_coeff = concat(
        [[0, 0, 0, 64, 0, 0, 0, 0], [- 1, 4, - 10, 58, 17, - 5, 1, 0], [- 1, 4, - 11, 40, 40, - 11, 4, - 1],
         [0, 1, - 5, 17, 58, - 10, 4, - 1]])
    # sr_interpolate.m:59
    patch_1 = conv2(refer_patch, rot90(filter_coeff(mv_x_ind + 1, arange()), 2), 'valid')
    # sr_interpolate.m:64
    patch_2 = conv2(patch_1, rot90(filter_coeff(mv_y_ind + 1, arange()), 2).T, 'valid')
    # sr_interpolate.m:66
    interp_patch = floor(patch_2 / 64 + 0.01)
    # sr_interpolate.m:69
    interp_patch = round(interp_patch / 64)
    # sr_interpolate.m:71
    interp_patch = max(min(interp_patch, 255), 0)
    # sr_interpolate.m:73
    return interp_patch
