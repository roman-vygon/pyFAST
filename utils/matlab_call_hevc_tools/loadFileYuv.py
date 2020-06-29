# Generated with SMOP  0.41
from libsmop import *

"""def loadFileYuv(fileName=None, width=None, height=None, idxFrame=None):
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
        fseek(fileId, (idxFrame(f) - 1) * sizeFrame, 'bof')
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
"""


def loadFileYuv(fileName=None, width=None, height=None, num_frames=None):
    stream = open(fileName, 'rb')
    # Seek to the fourth frame in the file
    rgb_frames = []

    for i in range(num_frames):
        stream.seek(int(i * width * height * 1.5))
        # Calculate the actual image size in the stream (accounting for rounding
        # of the resolution)
        fwidth = (width + 31) // 32 * 32
        fheight = (height + 15) // 16 * 16
        # Load the Y (luminance) data from the stream
        Y = np.fromfile(stream, dtype=np.uint8, count=fwidth * fheight). \
            reshape((fheight, fwidth))
        # Load the UV (chrominance) data from the stream, and double its size
        U = np.fromfile(stream, dtype=np.uint8, count=(fwidth // 2) * (fheight // 2)). \
            reshape((fheight // 2, fwidth // 2)). \
            repeat(2, axis=0).repeat(2, axis=1)
        V = np.fromfile(stream, dtype=np.uint8, count=(fwidth // 2) * (fheight // 2)). \
            reshape((fheight // 2, fwidth // 2)). \
            repeat(2, axis=0).repeat(2, axis=1)
        # Stack the YUV channels together, crop the actual resolution, convert to
        # floating point for later calculations, and apply the standard biases
        YUV = np.dstack((Y, U, V))[:height, :width, :].astype(np.float)
        YUV[:, :, 0] = YUV[:, :, 0] - 16  # Offset Y by 16
        YUV[:, :, 1:] = YUV[:, :, 1:] - 128  # Offset UV by 128
        # YUV conversion matrix from ITU-R BT.601 version (SDTV)
        # Note the swapped R and B planes!
        #              Y       U       V
        M = np.array([[1.164, 2.017, 0.000],  # B
                      [1.164, -0.392, -0.813],  # G
                      [1.164, 0.000, 1.596]])  # R
        # Take the dot product with the matrix to produce BGR output, clamp the
        # results to byte range and convert to bytes
        BGR = YUV.dot(M.T).clip(0, 255).astype(np.uint8)
        rgb_frames.append(BGR)
    return rgb_frames


def loadFileYuvMatlab(fileName=None, width=None, height=None, num_frames=None):
    stream = open(fileName, 'rb')
    # Seek to the fourth frame in the file
    rgb_frames = []
    subSampleMat = np.ones((2, 2))
    for i in range(num_frames):
        sizeFrame = int(1.5 * width * height)
        stream.seek(i * sizeFrame)

        buf = np.fromfile(stream, dtype=np.uint8, count=width * height)
        print(buf)
        Y = np.reshape(buf, (width, height)).T

        buf = np.fromfile(stream, dtype=np.uint8, count=width * height // 4)
        U = np.kron(np.reshape(buf, (width // 2, height // 2)).T, subSampleMat)

        buf = np.fromfile(stream, dtype=np.uint8, count=width * height // 4)
        V = np.kron(np.reshape(buf, (width // 2, height // 2)).T, subSampleMat)
        # Calculate the actual image size in the stream (accounting for rounding
        # of the resolution)

        # Load the Y (luminance) data from the stream

        YUV = np.dstack([Y, U, V])
        # Stack the YUV channels together, crop the actual resolution, convert to
        # floating point for later calculations, and apply the standard biases
        # YUV = np.dstack((Y, U, V))[:height, :width, :].astype(np.float)
        YUV[:, :, 0] = YUV[:, :, 0] - 16  # Offset Y by 16
        YUV[:, :, 1:] = YUV[:, :, 1:] - 128  # Offset UV by 128
        # YUV conversion matrix from ITU-R BT.601 version (SDTV)
        # Note the swapped R and B planes!
        #              Y       U       V
        M = np.array([[1.164, 2.017, 0.000],  # B
                      [1.164, -0.392, -0.813],  # G
                      [1.164, 0.000, 1.596]])  # R
        # Take the dot product with the matrix to produce BGR output, clamp the
        # results to byte range and convert to bytes
        BGR = YUV.dot(M.T).clip(0, 255).astype(np.uint8)
        rgb_frames.append(BGR[..., ::-1])
    return rgb_frames
