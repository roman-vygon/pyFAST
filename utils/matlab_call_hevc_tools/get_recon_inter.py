# Generated with SMOP  0.41
from libsmop import *
# get_recon_inter.m

    
@function
def get_recon_inter(PU_all=None,prefilt_Y=None,*args,**kwargs):
    varargin = get_recon_inter.varargin
    nargin = get_recon_inter.nargin

    N_frames=length(PU_all)
# get_recon_inter.m:4
    recon_inter=cell(1,N_frames)
# get_recon_inter.m:5
    inter_mask=cell(1,N_frames)
# get_recon_inter.m:6
    mv_x_map=cell(1,N_frames)
# get_recon_inter.m:7
    mv_y_map=cell(1,N_frames)
# get_recon_inter.m:8
    for t in arange(1,N_frames).reshape(-1):
        N_PU=length(PU_all[t])
# get_recon_inter.m:11
        recon_inter[t]=zeros(size(prefilt_Y[1],1),size(prefilt_Y[1],2))
# get_recon_inter.m:12
        inter_mask[t]=zeros(size(prefilt_Y[1],1),size(prefilt_Y[1],2))
# get_recon_inter.m:13
        mv_x_map[t]=zeros(size(prefilt_Y[1],1),size(prefilt_Y[1],2))
# get_recon_inter.m:14
        mv_y_map[t]=zeros(size(prefilt_Y[1],1),size(prefilt_Y[1],2))
# get_recon_inter.m:15
        for pu_idx in arange(1,N_PU).reshape(-1):
            pu_struct=PU_all[t](pu_idx)
# get_recon_inter.m:17
            if isempty(pu_struct.intra):
                continue
            if pu_struct.intra == 1:
                continue
            r=pu_struct.y + 1
# get_recon_inter.m:24
            c=pu_struct.x + 1
# get_recon_inter.m:25
            w=pu_struct.w
# get_recon_inter.m:26
            h=pu_struct.h
# get_recon_inter.m:27
            mv_x=pu_struct.mv_x
# get_recon_inter.m:28
            mv_y=pu_struct.mv_y
# get_recon_inter.m:29
            ref_idx=pu_struct.t_r + 1
# get_recon_inter.m:30
            assert_(pu_struct.t == t - 1,'Frame indexing for MC is wrong')
            r0=r + floor(mv_y / 4 + 0.01)
# get_recon_inter.m:33
            c0=c + floor(mv_x / 4 + 0.01)
# get_recon_inter.m:34
            refer_patch=get_referenced_patch(prefilt_Y[ref_idx],r0,c0,w,h)
# get_recon_inter.m:35
            interp_patch=fractional_interpolate(refer_patch,mod(mv_x,4),mod(mv_y,4))
# get_recon_inter.m:37
            try:
                recon_inter[t][arange(r,(r + h - 1)),arange(c,(c + w - 1))]=interp_patch
# get_recon_inter.m:40
            finally:
                pass
            inter_mask[t][arange(r,(r + h - 1)),arange(c,(c + w - 1))]=pu_idx
# get_recon_inter.m:44
            mv_x_map[t][arange(r,(r + h - 1)),arange(c,(c + w - 1))]=mv_x
# get_recon_inter.m:46
            mv_y_map[t][arange(r,(r + h - 1)),arange(c,(c + w - 1))]=mv_y
# get_recon_inter.m:47
    
    return recon_inter,inter_mask,mv_x_map,mv_y_map
    
if __name__ == '__main__':
    pass
    
    
@function
def get_referenced_patch(input_image=None,r=None,c=None,w=None,h=None,*args,**kwargs):
    varargin = get_referenced_patch.varargin
    nargin = get_referenced_patch.nargin

    r0=r - 3
# get_recon_inter.m:54
    r1=r + h - 1 + 4
# get_recon_inter.m:55
    c0=c - 3
# get_recon_inter.m:56
    c1=c + w - 1 + 4
# get_recon_inter.m:57
    X=arange(c0,c1)
# get_recon_inter.m:59
    Y=arange(r0,r1)
# get_recon_inter.m:60
    X_clip=min(max(X,1),size(input_image,2))
# get_recon_inter.m:61
    Y_clip=min(max(Y,1),size(input_image,1))
# get_recon_inter.m:62
    ref_patch=input_image(Y_clip,X_clip)
# get_recon_inter.m:64
    # r0_clip = max(r0, 1);
# c0_clip = max(c0, 1);
# r1_clip = min(r1, size(input_image, 1));
# c1_clip = min(c1, size(input_image, 2));
    
    # clip_patch = input_image(r0_clip:r1_clip, c0_clip:c1_clip);
# if r0 < r0_clip
#     clip_patch = padarray(clip_patch, [r0_clip - r0, 0], 'pre', 'replicate');
# end
# 
# if r1 > r1_clip
#     clip_patch = padarray(clip_patch, [r1 - r1_clip, 0], 'post', 'replicate');
# end
# 
# if c0 < c0_clip
#     clip_patch = padarray(clip_patch, [0, c0_clip - c0], 'pre', 'replicate');
# end
# 
# if c1 > c1_clip
#     clip_patch = padarray(clip_patch, [0, c1 - c1_clip], 'post', 'replicate');
# end
# 
# ref_patch = clip_patch;
    return ref_patch
    
if __name__ == '__main__':
    pass
    
    
@function
def fractional_interpolate(refer_patch=None,mv_x_ind=None,mv_y_ind=None,*args,**kwargs):
    varargin = fractional_interpolate.varargin
    nargin = fractional_interpolate.nargin

    filter_coeff=concat([[0,0,0,64,0,0,0,0],[- 1,4,- 10,58,17,- 5,1,0],[- 1,4,- 11,40,40,- 11,4,- 1],[0,1,- 5,17,58,- 10,4,- 1]])
# get_recon_inter.m:94
    patch_1=conv2(refer_patch,rot90(filter_coeff(mv_x_ind + 1,arange()),2),'valid')
# get_recon_inter.m:99
    patch_2=conv2(patch_1,rot90(filter_coeff(mv_y_ind + 1,arange()),2).T,'valid')
# get_recon_inter.m:101
    interp_patch=floor(patch_2 / 64 + 0.01)
# get_recon_inter.m:104
    interp_patch=round(interp_patch / 64)
# get_recon_inter.m:106
    interp_patch=max(min(interp_patch,255),0)
# get_recon_inter.m:108
    return interp_patch
    
if __name__ == '__main__':
    pass
    