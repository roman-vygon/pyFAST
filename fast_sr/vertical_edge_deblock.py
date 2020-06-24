# Generated with SMOP  0.41
from libsmop import *
# vertical_edge_deblock.m

    
@function
def vertical_edge_deblock(img=None,QP=None,*args,**kwargs):
    varargin = vertical_edge_deblock.varargin
    nargin = vertical_edge_deblock.nargin

    block_size=8
# vertical_edge_deblock.m:2
    N_r=size(img,1) / (block_size / 2)
# vertical_edge_deblock.m:3
    N_c=size(img,2) / block_size - 1
# vertical_edge_deblock.m:4
    beta,tc=get_beta_tc_from_QP(QP,nargout=2)
# vertical_edge_deblock.m:6
    img_deblock=copy(img)
# vertical_edge_deblock.m:8
    for r_idx in arange(1,N_r).reshape(-1):
        for c_idx in arange(1,N_c).reshape(-1):
            r0=1 + dot((r_idx - 1),(block_size / 2))
# vertical_edge_deblock.m:11
            c0=(block_size / 2) + 1 + dot((c_idx - 1),block_size)
# vertical_edge_deblock.m:12
            patch=img(arange(r0,(r0 + block_size / 2 - 1)),arange(c0,(c0 + block_size - 1)))
# vertical_edge_deblock.m:13
            p_l1=abs(patch(1,2) - dot(2,patch(1,3)) + patch(1,4))
# vertical_edge_deblock.m:17
            q_l1=abs(patch(1,5) - dot(2,patch(1,6)) + patch(1,7))
# vertical_edge_deblock.m:18
            p_l4=abs(patch(4,2) - dot(2,patch(4,3)) + patch(4,4))
# vertical_edge_deblock.m:19
            q_l4=abs(patch(4,5) - dot(2,patch(4,6)) + patch(4,7))
# vertical_edge_deblock.m:20
            if p_l1 + q_l1 + p_l4 + q_l4 > beta:
                # no deblocking!
                img_deblock[arange(r0,(r0 + block_size / 2 - 1)),arange(c0,(c0 + block_size - 1))]=patch
# vertical_edge_deblock.m:25
            else:
                # judge strong or normal filtering
                b1=(p_l1 + q_l1 < (beta / 8)) and (p_l4 + q_l4 < (beta / 8))
# vertical_edge_deblock.m:28
                b2=abs(patch(1,1) - patch(1,4)) + abs(patch(1,5) - patch(1,8)) < (beta / 8)
# vertical_edge_deblock.m:30
                b3=abs(patch(4,1) - patch(4,4)) + abs(patch(4,5) - patch(4,8)) < (beta / 8)
# vertical_edge_deblock.m:32
                b4=abs(patch(1,4) - patch(1,5)) < dot(2.5,tc)
# vertical_edge_deblock.m:34
                b5=abs(patch(4,4) - patch(4,5)) < dot(2.5,tc)
# vertical_edge_deblock.m:35
                if b1 and b2 and b3 and b4 and b5:
                    # strong deblocking filter
                    for i in arange(1,4).reshape(-1):
                        patch[i,arange()]=strong_filter(patch(i,arange()),tc)
# vertical_edge_deblock.m:40
                else:
                    # normal deblocking filter
                    # Judge how many elements to change
                    if (p_l1 + q_l1) < (dot(beta / 8,3)) and (p_l4 + q_l4) < (dot(beta / 8,3)):
                        # Change p0, q0, p1, q1
                        for i in arange(1,4).reshape(-1):
                            patch[i,arange()]=normal_filter_p0q0p1q1(patch(i,arange()),tc)
# vertical_edge_deblock.m:50
                    else:
                        # Only change p0, q0
                        for i in arange(1,4).reshape(-1):
                            patch[i,arange()]=normal_filter_p0q0(patch(i,arange()),tc)
# vertical_edge_deblock.m:55
                img_deblock[arange(r0,(r0 + block_size / 2 - 1)),arange(c0,(c0 + block_size - 1))]=patch
# vertical_edge_deblock.m:60
    
    return img_deblock
    
if __name__ == '__main__':
    pass
    
    
@function
def strong_filter(p_vec=None,tc=None,*args,**kwargs):
    varargin = strong_filter.varargin
    nargin = strong_filter.nargin

    c=dot(2,tc)
# vertical_edge_deblock.m:68
    dp0=floor((p_vec(2) + dot(2,p_vec(3)) - dot(6,p_vec(4)) + dot(2,p_vec(5)) + p_vec(6) + 4) / 8)
# vertical_edge_deblock.m:69
    dp1=floor((p_vec(2) - dot(3,p_vec(3)) + p_vec(4) + p_vec(5) + 2) / 4)
# vertical_edge_deblock.m:71
    dp2=floor((dot(2,p_vec(1)) - dot(5,p_vec(2)) + p_vec(3) + p_vec(4) + p_vec(5) + 4) / 8)
# vertical_edge_deblock.m:72
    dq0=floor((p_vec(7) + dot(2,p_vec(6)) - dot(6,p_vec(5)) + dot(2,p_vec(4)) + p_vec(3) + 4) / 8)
# vertical_edge_deblock.m:75
    dq1=floor((p_vec(7) - dot(3,p_vec(6)) + p_vec(5) + p_vec(4) + 2) / 4)
# vertical_edge_deblock.m:77
    dq2=floor((dot(2,p_vec(8)) - dot(5,p_vec(7)) + p_vec(6) + p_vec(5) + p_vec(4) + 4) / 8)
# vertical_edge_deblock.m:78
    dp0=min(max(- c,dp0),c)
# vertical_edge_deblock.m:82
    dp1=min(max(- c,dp1),c)
# vertical_edge_deblock.m:83
    dp2=min(max(- c,dp2),c)
# vertical_edge_deblock.m:84
    dq0=min(max(- c,dq0),c)
# vertical_edge_deblock.m:86
    dq1=min(max(- c,dq1),c)
# vertical_edge_deblock.m:87
    dq2=min(max(- c,dq2),c)
# vertical_edge_deblock.m:88
    # fprintf('dp0 = #d, dp1 = #d, dp2 = #d, dq0 = #d, dq1 = #d, dq2 = #d\n', ...
#     dp0, dp1, dp2, dq0, dq1, dq2);
    
    p_vec_deblock=p_vec + concat([0,dp2,dp1,dp0,dq0,dq1,dq2,0])
# vertical_edge_deblock.m:93
    p_vec_deblock=min(max(p_vec_deblock,0),255)
# vertical_edge_deblock.m:94
    return p_vec_deblock
    
if __name__ == '__main__':
    pass
    
    
@function
def normal_filter_p0q0p1q1(p_vec=None,tc=None,*args,**kwargs):
    varargin = normal_filter_p0q0p1q1.varargin
    nargin = normal_filter_p0q0p1q1.nargin

    d0=floor((dot(9,(p_vec(5) - p_vec(4))) - dot(3,(p_vec(6) - p_vec(3))) + 8) / 16)
# vertical_edge_deblock.m:99
    d0=min(max(- tc,d0),tc)
# vertical_edge_deblock.m:100
    dp1=floor((floor((p_vec(2) + p_vec(4) + 1) / 2) - p_vec(3) + d0 + 1) / 2)
# vertical_edge_deblock.m:102
    dq1=floor((floor((p_vec(7) + p_vec(5) + 1) / 2) - p_vec(6) - d0 + 1) / 2)
# vertical_edge_deblock.m:103
    dp1=min(max(- tc,dp1),tc / 2)
# vertical_edge_deblock.m:105
    dq1=min(max(- tc,dq1),tc / 2)
# vertical_edge_deblock.m:106
    # fprintf('p2 = #f, p3 = #f, p4 = #f, p5 = #f, p6 = #f, p7= #f, d0 = #f, dp1 = #f, dq1 = #f\n', ...
#     p_vec(2), p_vec(3), p_vec(4), p_vec(5), p_vec(6), p_vec(7), d0, dp1, dq1);
    
    p_vec_deblock=copy(p_vec)
# vertical_edge_deblock.m:111
    p_vec_deblock[arange(3,6)]=p_vec_deblock(arange(3,6)) + concat([dp1,d0,- d0,dq1])
# vertical_edge_deblock.m:112
    p_vec_deblock=min(max(p_vec_deblock,0),255)
# vertical_edge_deblock.m:113
    return p_vec_deblock
    
if __name__ == '__main__':
    pass
    
    
@function
def normal_filter_p0q0(p_vec=None,tc=None,*args,**kwargs):
    varargin = normal_filter_p0q0.varargin
    nargin = normal_filter_p0q0.nargin

    d0=floor((dot(9,(p_vec(5) - p_vec(4))) - dot(3,(p_vec(6) - p_vec(3))) + 8) / 16)
# vertical_edge_deblock.m:118
    d0=min(max(- tc,d0),tc)
# vertical_edge_deblock.m:119
    # fprintf('p3 = #f, p4 = #f, p5 = #f, p6 = #f, d0 = #f\n', p_vec(3), p_vec(4), ...
#     p_vec(5), p_vec(6), d0);
    
    p_vec_deblock=copy(p_vec)
# vertical_edge_deblock.m:124
    p_vec_deblock[arange(4,5)]=p_vec_deblock(arange(4,5)) + concat([d0,- d0])
# vertical_edge_deblock.m:125
    p_vec_deblock=min(max(p_vec_deblock,0),255)
# vertical_edge_deblock.m:126
    return p_vec_deblock
    
if __name__ == '__main__':
    pass
    
    
@function
def get_beta_tc_from_QP(QP=None,*args,**kwargs):
    varargin = get_beta_tc_from_QP.varargin
    nargin = get_beta_tc_from_QP.nargin

    # assert(QP == 37, ['For any other value other than 37, ' ...
#     'have not set how to determine beta, and tc']);
    if 37 == QP:
        beta=40
# vertical_edge_deblock.m:134
        tc=5
# vertical_edge_deblock.m:135
    else:
        if 42 == QP:
            beta=45
# vertical_edge_deblock.m:137
            tc=8
# vertical_edge_deblock.m:138
        else:
            if 47 == QP:
                beta=60
# vertical_edge_deblock.m:140
                tc=10
# vertical_edge_deblock.m:141
            else:
                error('Unrecognized QP!')
    
    return beta,tc
    
if __name__ == '__main__':
    pass
    