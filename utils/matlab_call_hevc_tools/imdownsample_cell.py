# Generated with SMOP  0.41
from libsmop import *
# imdownsample_cell.m

    
@function
def imdownsample_cell(rgb_cell=None,ratio=None,clip_dim=None,*args,**kwargs):
    varargin = imdownsample_cell.varargin
    nargin = imdownsample_cell.nargin

    rgb_half_cell=cell(size(rgb_cell))
# imdownsample_cell.m:3
    for i in arange(1,length(rgb_cell)).reshape(-1):
        rgb_half_cell[i]=imresize(rgb_cell[i],1 / ratio)
# imdownsample_cell.m:5
        if exist('clip_dim','var'):
            height_clip=dot(floor(size(rgb_half_cell[i],1) / clip_dim),clip_dim)
# imdownsample_cell.m:7
            width_clip=dot(floor(size(rgb_half_cell[i],2) / clip_dim),clip_dim)
# imdownsample_cell.m:9
            rgb_half_cell[i]=rgb_half_cell[i](arange(1,height_clip),arange(1,width_clip),arange())
# imdownsample_cell.m:11
    
    return rgb_half_cell
    
if __name__ == '__main__':
    pass
    