# Generated with SMOP  0.41
from libsmop import *
# modcrop.m

    
@function
def modcrop(imgs=None,modulo=None,*args,**kwargs):
    varargin = modcrop.varargin
    nargin = modcrop.nargin

    if size(imgs,3) == 1:
        sz=size(imgs)
# modcrop.m:5
        sz=sz - mod(sz,modulo)
# modcrop.m:7
        imgs=imgs(arange(1,sz(1)),arange(1,sz(2)))
# modcrop.m:9
    else:
        tmpsz=size(imgs)
# modcrop.m:13
        sz=tmpsz(arange(1,2))
# modcrop.m:15
        sz=sz - mod(sz,modulo)
# modcrop.m:17
        imgs=imgs(arange(1,sz(1)),arange(1,sz(2)),arange())
# modcrop.m:19
    