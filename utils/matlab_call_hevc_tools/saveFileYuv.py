# Generated with SMOP  0.41
from libsmop import *


# saveFileYuv.m


def saveFileYuv(mov=None, fileName=None, mode=None):
    # save RGB movie [0, 255] to YUV 4:2:0 file

    if 1 == mode:
        fileId = fopen(fileName, 'w')
    # saveFileYuv.m:11
    else:
        if 2 == mode:
            fileId = fopen(fileName, 'a')
        # saveFileYuv.m:15
        else:
            fileId = fopen(fileName, 'w')
    # saveFileYuv.m:19

    dim = size(mov(1).cdata)
    # saveFileYuv.m:25
    nrFrame = length(mov)
    # saveFileYuv.m:27
    for f in arange(1, nrFrame, 1).reshape(-1):
        imgRgb = frame2im(mov(f))
        # saveFileYuv.m:33
        imgYuv = reshape(convertRgbToYuv(reshape(imgRgb, dot(dim(1), dim(2)), 3)), dim(1), dim(2), 3)
        # saveFileYuv.m:39
        buf = reshape(imgYuv(arange(), arange(), 1).T, [], 1)
        # saveFileYuv.m:45
        count = fwrite(fileId, buf, 'uchar')
        # saveFileYuv.m:47
        buf = reshape(imgYuv(arange(1, end(), 2), arange(1, end(), 2), 2).T, [], 1)
        # saveFileYuv.m:53
        count = fwrite(fileId, buf, 'uchar')
        # saveFileYuv.m:55
        buf = reshape(imgYuv(arange(1, end(), 2), arange(1, end(), 2), 3).T, [], 1)
        # saveFileYuv.m:61
        count = fwrite(fileId, buf, 'uchar')
    # saveFileYuv.m:63

    fclose(fileId)
