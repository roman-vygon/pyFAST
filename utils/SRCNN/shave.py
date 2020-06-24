# Generated with SMOP  0.41
from libsmop import *
# shave.m

    
@function
def shave(I=None,border=None,*args,**kwargs):
    varargin = shave.varargin
    nargin = shave.nargin

    I=I(arange(1 + border(1),end() - border(1)),arange(1 + border(2),end() - border(2)),arange(),arange())
# shave.m:3