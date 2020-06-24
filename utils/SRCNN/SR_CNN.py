# Generated with SMOP  0.41
from libsmop import *
# SR_CNN.m

    
@function
def SR_CNN(iml=None,ratio=None,model=None,*args,**kwargs):
    varargin = SR_CNN.varargin
    nargin = SR_CNN.nargin

    if 2 == ratio:
        sr_model=model.x2_model
# SR_CNN.m:5
    else:
        if 3 == ratio:
            sr_model=model.x3_model
# SR_CNN.m:7
        else:
            if 4 == ratio:
                sr_model=model.x4_model
# SR_CNN.m:9
            else:
                error('Unsupported upsampling ratio: %f',ratio)
    
    iml=single(iml) / 255
# SR_CNN.m:14
    imh_bicubic=imresize(iml,ratio,'bicubic')
# SR_CNN.m:15
    imh_sr=SRCNN(sr_model,imh_bicubic)
# SR_CNN.m:16
    border=copy(ratio)
# SR_CNN.m:19
    imh=copy(imh_bicubic)
# SR_CNN.m:20
    imh[arange((1 + border),(end() - border)),arange((1 + border),(end() - border))]=imh_sr(arange((1 + border),(end() - border)),arange((1 + border),(end() - border)))
# SR_CNN.m:21
    imh=uint8(dot(255,imh))
# SR_CNN.m:24
    return imh
    
if __name__ == '__main__':
    pass
    