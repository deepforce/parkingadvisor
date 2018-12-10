"""
Create colormap based on rank mode
"""
import branca.colormap as cm

def color_bar(mode):
    """
    Create different colormap for each mode

    Attribute
    -----------------
    mode:   int
        1: Rate
        2: Occupancy
        3: Recommanded

    Return
    ---------------
    colormap: branca.Colormap
    """
    cm_name = {1: cm.linear.YlGnBu_07,
               2: cm.linear.RdPu_06,
               3: cm.linear.RdYlGn_06}
    step = {1: 6, 2: 6, 3: 5}
    colormap = cm_name[mode].to_step(step[mode])

    return colormap

