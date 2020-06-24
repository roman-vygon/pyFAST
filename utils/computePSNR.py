# Generated with SMOP  0.41
from libsmop import *
# computePSNR.m

    
@function
def computePSNR(X0=None,X=None,*args,**kwargs):
    varargin = computePSNR.varargin
    nargin = computePSNR.nargin

    # computePSNR(X0, X) computes the peak signal-to-noise ratio defined as:
# PSNR(X0, X) = 20 * log10(max(|X0|)) - 10 * log10(MSE(X0, X))
# ------------------------input-------------------------------------------
# X0, X:        two matrices with the same size.
# ------------------------output------------------------------------------
# psnr_value:   peak signal-to-noise ratio between X0 and X.
    X=double(X)
# computePSNR.m:8
    X0=double(X0)
# computePSNR.m:9
    psnr_value=dot(20,log10(255)) - dot(10,log10(sum((ravel(X0) - ravel(X)) ** 2) / numel(X)))
# computePSNR.m:10