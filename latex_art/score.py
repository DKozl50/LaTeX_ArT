def color_penalty_score(
        sx, sy,
        swidth,
        smap,
        entire_w, entire_h,
        colmin, colmax):
    x01 = sx / entire_w
    y01 = sy / entire_h
    v01 = (x01**2 + y01**2)**0.5
    normcolor = (smap - colmin) / (colmax - colmin)
    return abs(v01 - normcolor) * swidth
