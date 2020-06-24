# Generated with SMOP  0.41
from libsmop import *


# cellstr2num.m


def cellstr2num(cell_str=None):
    tmp = concat([[ravel(cell_str).T], [repmat(cellarray([' ']), 1, length(cell_str))]])
    # cellstr2num.m:3
    tmp = cell2mat(ravel(tmp).T)
    # cellstr2num.m:4
    nums = str2num(tmp)
    # cellstr2num.m:5
    return nums
