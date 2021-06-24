import numpy as np

class ScoreController:
    def __init__(self, image: np.ndarray, width, height, col_min=0, col_max=1):
        # image  --  numpy array
        # width, height  --  in sp
        self.image = image
        self.width = width
        self.height = height
        self.col_min = col_min
        self.col_delta = col_max - col_min
        n, m = image.shape
        self.w_per_pixel = width / m
        self.h_per_pixel = height / n

    def __call__(self, x, y, w, h, cmap):
        # x, y  --  top left coordinates of a symbol in sp
        # w, h  --  width and height of a symbol
        center_x = x + w/2
        center_y = y + h/2
        cx = int(center_x // self.w_per_pixel)
        cy = int(center_y // self.h_per_pixel)

        return (self.image[cy, cx] - self._norm_cmap(cmap))**2 * w

    def _norm_cmap(self, cmap):
        return (cmap - self.col_min) / self.col_delta


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
    return (v01 - normcolor)**2 * swidth
