# Generated with SMOP  0.41
from libsmop import *


# plot_block_loc.m


def plot_block_loc(img=None, block_size=None, block_loc=None, stroke_w=None):
    if logical_not(exist('stroke_w', 'var')):
        stroke_w = 2
    # plot_block_loc.m:3

    img_with_blk = copy(img)
    # plot_block_loc.m:6
    img_w = size(img, 2)
    # plot_block_loc.m:8
    img_h = size(img, 1)
    # plot_block_loc.m:9
    draw_color = dot(255, concat([1, 0, 0]))
    # plot_block_loc.m:11
    xl1 = max(min(block_loc(1) - stroke_w, img_w), 1)
    # plot_block_loc.m:12
    xl2 = max(min(block_loc(1) + stroke_w, img_w), 1)
    # plot_block_loc.m:13
    xr1 = max(min(block_loc(1) + block_size(2) - 1 - stroke_w, img_w), 1)
    # plot_block_loc.m:14
    xr2 = max(min(block_loc(1) + block_size(2) - 1 + stroke_w, img_w), 1)
    # plot_block_loc.m:15
    yt1 = max(min(block_loc(2) - stroke_w, img_h), 1)
    # plot_block_loc.m:17
    yt2 = max(min(block_loc(2) + stroke_w, img_h), 1)
    # plot_block_loc.m:18
    yb1 = max(min(block_loc(2) + block_size(1) - 1 - stroke_w, img_h), 1)
    # plot_block_loc.m:19
    yb2 = max(min(block_loc(2) + block_size(1) - 1 + stroke_w, img_h), 1)
    # plot_block_loc.m:20
    for c in arange(1, 3).reshape(-1):
        img_with_blk[arange(yt1, yt2), arange(xl1, xr2), c] = draw_color(c)
        # plot_block_loc.m:23
        img_with_blk[arange(yb1, yb2), arange(xl1, xr2), c] = draw_color(c)
        # plot_block_loc.m:24
        img_with_blk[arange(yt1, yb2), arange(xl1, xl2), c] = draw_color(c)
        # plot_block_loc.m:25
        img_with_blk[arange(yt1, yb2), arange(xr1, xr2), c] = draw_color(c)
# plot_block_loc.m:26
