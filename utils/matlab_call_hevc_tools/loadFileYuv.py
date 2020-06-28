# Generated with SMOP  0.41
from libsmop import *


# loadFileYuv.m

# function mov = loadFileYuv(fileName, width, height, idxFrame)


def loadFileYuv(fileName=None, width=None, height=None, idxFrame=None):
    # load RGB movie [0, 255] from YUV 4:2:0 file

    fileId = fopen(fileName, 'r')
    # loadFileYuv.m:11
    subSampleMat = concat([[1, 1], [1, 1]])
    # loadFileYuv.m:15
    nrFrame = length(idxFrame)
    # loadFileYuv.m:17
    for f in arange(1, nrFrame, 1).reshape(-1):
        # search fileId position
        sizeFrame = 1.5 * width * height
        # loadFileYuv.m:25
        fseek(fileId, dot((idxFrame(f) - 1), sizeFrame), 'bof')
        buf = fread(fileId, dot(width, height), 'uchar')
        # loadFileYuv.m:33
        imgYuv[arange(), arange(), 1] = reshape(buf, width, height).T
        # loadFileYuv.m:35
        # read U component
        buf = fread(fileId, dot(width / 2, height) / 2, 'uchar')
        # loadFileYuv.m:41
        imgYuv[arange(), arange(), 2] = kron(reshape(buf, width / 2, height / 2).T, subSampleMat)
        # loadFileYuv.m:43
        # read V component
        buf = fread(fileId, dot(width / 2, height) / 2, 'uchar')
        # loadFileYuv.m:49
        imgYuv[arange(), arange(), 3] = kron(reshape(buf, width / 2, height / 2).T, subSampleMat)
        # loadFileYuv.m:51
        # normalize YUV values
        # imgYuv = imgYuv / 255;
        # convert YUV to RGB
        imgRgb = reshape(convertYuvToRgb(reshape(imgYuv, dot(height, width), 3)), height, width, 3)
        # loadFileYuv.m:63
        # imwrite(imgRgb,'ActualBackground.bmp','bmp');
        mov[f] = im2frame(imgRgb)
    # loadFileYuv.m:69
    # 	mov(f).colormap =  [];
    #     imwrite(imgRgb,'ActualBackground.bmp','bmp');
    # figure, imshow(imgRgb);
    # name = 'ActualBackground.bmp';
    # Image = imread(name, 'bmp');
    # figure, imshow(Image);

    fclose(fileId)
