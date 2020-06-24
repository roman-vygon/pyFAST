# Generated with SMOP  0.41
from libsmop import *


# Blockwise_upsample_with_TU.m


def Blockwise_upsample_with_TU(res_l=None, TU=None):
    res_h = zeros(dot(2, size(res_l)))
    # Blockwise_upsample_with_TU.m:3
    for i in arange(1, length(TU)).reshape(-1):
        if isempty(TU(i).x) or isempty(TU(i).w):
            continue
        x_l = TU(i).x
        # Blockwise_upsample_with_TU.m:10
        y_l = TU(i).y
        # Blockwise_upsample_with_TU.m:11
        x_h = dot(2, x_l)
        # Blockwise_upsample_with_TU.m:12
        y_h = dot(2, y_l)
        # Blockwise_upsample_with_TU.m:13
        w = TU(i).w
        # Blockwise_upsample_with_TU.m:15
        res_h[arange((y_h + 1), (y_h + dot(2, w))), arange((x_h + 1), (x_h + dot(2, w)))] = imresize(
            res_l(arange((y_l + 1), (y_l + w)), arange((x_l + 1), (x_l + w))), 2, 'bicubic')
    # Blockwise_upsample_with_TU.m:17

    return res_h


if __name__ == '__main__':
    pass
