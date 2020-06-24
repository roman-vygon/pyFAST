# Generated with SMOP  0.41
from libsmop import *
# load_rgb_cell_from_yuv.m

    
@function
def load_rgb_cell_from_yuv(yuv_path=None,img_width=None,img_height=None,num_frames=None,*args,**kwargs):
    varargin = load_rgb_cell_from_yuv.varargin
    nargin = load_rgb_cell_from_yuv.nargin

    rgb_cell=cell(1,num_frames)
# load_rgb_cell_from_yuv.m:4
    for i in arange(1,num_frames).reshape(-1):
        __,rgb_cell[i],__=loadFileYuv(yuv_path,img_width,img_height,i,nargout=3)
# load_rgb_cell_from_yuv.m:7
    
    return rgb_cell
    
if __name__ == '__main__':
    pass
    