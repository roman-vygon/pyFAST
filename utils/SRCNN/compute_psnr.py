# Generated with SMOP  0.41
from libsmop import *
# compute_psnr.m

    
@function
def compute_psnr(im1=None,im2=None,*args,**kwargs):
    varargin = compute_psnr.varargin
    nargin = compute_psnr.nargin

    if size(im1,3) == 3:
        im1=rgb2ycbcr(im1)
# compute_psnr.m:5
        im1=im1(arange(),arange(),1)
# compute_psnr.m:7
    
    if size(im2,3) == 3:
        im2=rgb2ycbcr(im2)
# compute_psnr.m:15
        im2=im2(arange(),arange(),1)
# compute_psnr.m:17
    
    imdff=double(im1) - double(im2)
# compute_psnr.m:23
    imdff=ravel(imdff)
# compute_psnr.m:25
    rmse=sqrt(mean(imdff ** 2))
# compute_psnr.m:29
    psnr=dot(20,log10(255 / rmse))
# compute_psnr.m:31