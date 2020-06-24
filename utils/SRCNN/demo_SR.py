# Generated with SMOP  0.41
from libsmop import *
# demo_SR.m

    # =========================================================================
    
    # Test code for Super-Resolution Convolutional Neural Networks (SRCNN)
    
    
    # Reference
    
    #   Chao Dong, Chen Change Loy, Kaiming He, Xiaoou Tang. Learning a Deep Convolutional Network for Image Super-Resolution,
    
    #   in Proceedings of European Conference on Computer Vision (ECCV), 2014
    
    
    #   Chao Dong, Chen Change Loy, Kaiming He, Xiaoou Tang. Image Super-Resolution Using Deep Convolutional Networks,
    
    #   arXiv:1501.00092
    
    
    # Chao Dong
    
    # IE Department, The Chinese University of Hong Kong
    
    # For any question, send email to ndc.forward@gmail.com
    
    # =========================================================================
    
    close_('all')
    clear('all')
    ## read ground truth image
    
    im=imread(fullfile('Set5','butterfly_GT.bmp'))
# demo_SR.m:39
    #im  = imread('Set14\zebra.bmp');
    
    ## set parameters
    
    # up_scale = 3;
    
    # model = 'model\9-5-5(ImageNet)\x3.mat';
    
    # up_scale = 3;
    
    # model = 'model\9-3-5(ImageNet)\x3.mat';
    
    # up_scale = 3;
    
    # model = 'model\9-1-5(91 images)\x3.mat';
    
    up_scale=2
# demo_SR.m:59
    model=fullfile('model','9-5-5(ImageNet)','x2.mat')
# demo_SR.m:61
    # up_scale = 4;
    
    # model = 'model\9-5-5(ImageNet)\x4.mat';
    
    ## work on illuminance only
    
    if size(im,3) > 1:
        im=rgb2ycbcr(im)
# demo_SR.m:73
        im=im(arange(),arange(),1)
# demo_SR.m:75
    
    im_gnd=modcrop(im,up_scale)
# demo_SR.m:79
    im_gnd=single(im_gnd) / 255
# demo_SR.m:81
    ## bicubic interpolation
    
    im_l=imresize(im_gnd,1 / up_scale,'bicubic')
# demo_SR.m:87
    im_b=imresize(im_l,up_scale,'bicubic')
# demo_SR.m:89
    ## SRCNN
    
    im_h=SRCNN(model,im_b)
# demo_SR.m:95
    ## remove border
    
    im_h=shave(uint8(dot(im_h,255)),concat([up_scale,up_scale]))
# demo_SR.m:101
    im_gnd=shave(uint8(dot(im_gnd,255)),concat([up_scale,up_scale]))
# demo_SR.m:103
    im_b=shave(uint8(dot(im_b,255)),concat([up_scale,up_scale]))
# demo_SR.m:105
    ## compute PSNR
    
    psnr_bic=compute_psnr(im_gnd,im_b)
# demo_SR.m:111
    psnr_srcnn=compute_psnr(im_gnd,im_h)
# demo_SR.m:113
    ## show results
    
    fprintf('PSNR for Bicubic Interpolation: %f dB\n',psnr_bic)
    fprintf('PSNR for SRCNN Reconstruction: %f dB\n',psnr_srcnn)
    figure
    imshow(im_b)
    title('Bicubic Interpolation')
    figure
    imshow(im_h)
    title('SRCNN Reconstruction')
    #imwrite(im_b, ['Bicubic Interpolation' '.bmp']);
    
    #imwrite(im_h, ['SRCNN Reconstruction' '.bmp']);
    