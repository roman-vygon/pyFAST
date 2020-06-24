# Generated with SMOP  0.41
from libsmop import *


# visualize_block_structure.m

def visualize_block_structure(img=None, block_struct=None):

    if logical_not(exist('plot_color', 'var')):
        plot_color = 'r'
    # visualize_block_structure.m:4

    # hf = figure;

    vis_img = copy(img)
    # visualize_block_structure.m:10
    for i in arange(1, length(block_struct)).reshape(-1):
        x = block_struct(i).x
        # visualize_block_structure.m:13
        y = block_struct(i).y
        # visualize_block_structure.m:14
        w = block_struct(i).w
        # visualize_block_structure.m:15
        if isempty(x) or isempty(w):
            continue
        if isfield(block_struct, 'h'):
            h = block_struct(i).h
        # visualize_block_structure.m:21
        else:
            h = copy(w)
        # visualize_block_structure.m:23
        #     plot([x + 1, x + w, x + w, x + 1, x + 1], ...
        #         [y + 1, y + 1, y + h, y + h, y + 1], ...
        #         [plot_color, '-']);
        vis_img = plot_block_loc(vis_img, concat([h + 1, w + 1]), concat([x + 1, y + 1]), 0)
    # visualize_block_structure.m:29
    #     hold on;

    # set(hf, 'Units', 'normalized', 'Position', [0, 0, 1, 1]);
    # vis_img = frame2im(getframe(gca));
    # close(hf);

    return vis_img

