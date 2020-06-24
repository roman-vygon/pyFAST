# Generated with SMOP  0.41
from libsmop import *
# SRload_CNN.m

    
@function
def SRload_CNN(*args,**kwargs):
    varargin = SRload_CNN.varargin
    nargin = SRload_CNN.nargin

    file_path=mfilename('fullpath')
# SRload_CNN.m:3
    pathstr,__,__=fileparts(file_path,nargout=3)
# SRload_CNN.m:4
    x2_model=fullfile(pathstr,'model','9-5-5(ImageNet)','x2.mat')
# SRload_CNN.m:6
    x3_model=fullfile(pathstr,'model','9-5-5(ImageNet)','x3.mat')
# SRload_CNN.m:7
    x4_model=fullfile(pathstr,'model','9-5-5(ImageNet)','x4.mat')
# SRload_CNN.m:8
    Model=struct('x2_model',cellarray([x2_model]),'x3_model',cellarray([x3_model]),'x4_model',cellarray([x4_model]))
# SRload_CNN.m:10
    return Model
    
if __name__ == '__main__':
    pass
    