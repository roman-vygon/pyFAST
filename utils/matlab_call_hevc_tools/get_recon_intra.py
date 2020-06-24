# Generated with SMOP  0.41
from libsmop import *
# get_recon_intra.m

    
@function
def get_recon_intra(PU_all=None,prefilt_Y=None,*args,**kwargs):
    varargin = get_recon_intra.varargin
    nargin = get_recon_intra.nargin

    N_frames=length(PU_all)
# get_recon_intra.m:3
    recon_intra=cell(1,N_frames)
# get_recon_intra.m:4
    intra_mask=cell(1,N_frames)
# get_recon_intra.m:5
    for t in arange(1,N_frames).reshape(-1):
        N_PU=length(PU_all[t])
# get_recon_intra.m:8
        recon_intra[t]=zeros(size(prefilt_Y[1],1),size(prefilt_Y[1],2))
# get_recon_intra.m:9
        intra_mask[t]=false(size(prefilt_Y[1],1),size(prefilt_Y[1],2))
# get_recon_intra.m:10
        for pu_idx in arange(1,N_PU).reshape(-1):
            pu_struct=PU_all[t](pu_idx)
# get_recon_intra.m:12
            if isempty(pu_struct.intra):
                continue
            if pu_struct.intra == 0:
                continue
            r=pu_struct.y + 1
# get_recon_intra.m:20
            c=pu_struct.x + 1
# get_recon_intra.m:21
            w=pu_struct.w
# get_recon_intra.m:22
            h=pu_struct.h
# get_recon_intra.m:23
            recon_intra[t][arange(r,(r + w - 1)),arange(c,(c + h - 1))]=prefilt_Y[t](arange(r,(r + w - 1)),arange(c,(c + h - 1)))
# get_recon_intra.m:24
            intra_mask[t][arange(r,(r + w - 1)),arange(c,(c + h - 1))]=true
# get_recon_intra.m:26
    
    return recon_intra,intra_mask
    
if __name__ == '__main__':
    pass
    