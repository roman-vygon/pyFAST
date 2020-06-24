# Generated with SMOP  0.41
from libsmop import *
# SRCNN.m

    
@function
def SRCNN(model=None,im_b=None,*args,**kwargs):
    varargin = SRCNN.varargin
    nargin = SRCNN.nargin

    ## load CNN model parameters
    
    load(model)
    conv1_patchsize2,conv1_filters=size(weights_conv1,nargout=2)
# SRCNN.m:9
    conv1_patchsize=sqrt(conv1_patchsize2)
# SRCNN.m:11
    conv2_channels,conv2_patchsize2,conv2_filters=size(weights_conv2,nargout=3)
# SRCNN.m:13
    conv2_patchsize=sqrt(conv2_patchsize2)
# SRCNN.m:15
    conv3_channels,conv3_patchsize2=size(weights_conv3,nargout=2)
# SRCNN.m:17
    conv3_patchsize=sqrt(conv3_patchsize2)
# SRCNN.m:19
    hei,wid=size(im_b,nargout=2)
# SRCNN.m:21
    ## conv1
    
    weights_conv1=reshape(weights_conv1,conv1_patchsize,conv1_patchsize,conv1_filters)
# SRCNN.m:27
    conv1_data=zeros(hei,wid,conv1_filters)
# SRCNN.m:29
    for i in arange(1,conv1_filters).reshape(-1):
        conv1_data[arange(),arange(),i]=imfilter(im_b,weights_conv1(arange(),arange(),i),'same','replicate')
# SRCNN.m:33
        conv1_data[arange(),arange(),i]=max(conv1_data(arange(),arange(),i) + biases_conv1(i),0)
# SRCNN.m:35
    
    ## conv2
    
    conv2_data=zeros(hei,wid,conv2_filters)
# SRCNN.m:43
    for i in arange(1,conv2_filters).reshape(-1):
        for j in arange(1,conv2_channels).reshape(-1):
            conv2_subfilter=reshape(weights_conv2(j,arange(),i),conv2_patchsize,conv2_patchsize)
# SRCNN.m:49
            conv2_data[arange(),arange(),i]=conv2_data(arange(),arange(),i) + imfilter(conv1_data(arange(),arange(),j),conv2_subfilter,'same','replicate')
# SRCNN.m:51
        conv2_data[arange(),arange(),i]=max(conv2_data(arange(),arange(),i) + biases_conv2(i),0)
# SRCNN.m:55
    
    ## conv3
    
    conv3_data=zeros(hei,wid)
# SRCNN.m:63
    for i in arange(1,conv3_channels).reshape(-1):
        conv3_subfilter=reshape(weights_conv3(i,arange()),conv3_patchsize,conv3_patchsize)
# SRCNN.m:67
        conv3_data[arange(),arange()]=conv3_data(arange(),arange()) + imfilter(conv2_data(arange(),arange(),i),conv3_subfilter,'same','replicate')
# SRCNN.m:69
    
    ## SRCNN reconstruction
    
    im_h=conv3_data(arange(),arange()) + biases_conv3
# SRCNN.m:77