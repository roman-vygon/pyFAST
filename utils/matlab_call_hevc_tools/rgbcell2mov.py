# Generated with SMOP  0.41
from libsmop import *
# rgbcell2mov.m

    
@function
def rgbcell2mov(image_cell=None,*args,**kwargs):
    varargin = rgbcell2mov.varargin
    nargin = rgbcell2mov.nargin

    N_frames=length(image_cell)
# rgbcell2mov.m:2
    for i in arange(1,N_frames).reshape(-1):
        mov[i]=im2frame(image_cell[i])
# rgbcell2mov.m:4
    
    return mov
    
if __name__ == '__main__':
    pass
    