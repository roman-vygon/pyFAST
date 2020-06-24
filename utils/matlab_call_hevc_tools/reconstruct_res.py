# Generated with SMOP  0.41
from libsmop import *
# reconstruct_res.m

    
@function
def reconstruct_res(res_struct=None,img_size=None,*args,**kwargs):
    varargin = reconstruct_res.varargin
    nargin = reconstruct_res.nargin

    res_recon=zeros(img_size)
# reconstruct_res.m:2
    hit_map=zeros(img_size)
# reconstruct_res.m:3
    for i in arange(1,length(res_struct)).reshape(-1):
        if isempty(res_struct(i).x) or isempty(res_struct(i).w) or isempty(res_struct(i).residual):
            continue
        x0=res_struct(i).x
# reconstruct_res.m:10
        y0=res_struct(i).y
# reconstruct_res.m:11
        r=y0 + 1
# reconstruct_res.m:12
        c=x0 + 1
# reconstruct_res.m:13
        w=res_struct(i).w
# reconstruct_res.m:14
        assert_(all(all(hit_map(arange(r,(r + w - 1)),arange(c,(c + w - 1))) == 0)),'duplicate coverage!')
        tmp=reshape(res_struct(i).residual,concat([w,w])).T
# reconstruct_res.m:19
        res_recon[arange(r,(r + w - 1)),arange(c,(c + w - 1))]=tmp
# reconstruct_res.m:20
        hit_map[arange(r,(r + w - 1)),arange(c,(c + w - 1))]=1
# reconstruct_res.m:21
    
    return res_recon
    
if __name__ == '__main__':
    pass
    