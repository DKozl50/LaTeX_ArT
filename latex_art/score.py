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

        ch, cw = cmap.shape
        sp_per_w = w / cw
        sp_per_h = h / ch
        img_slice = np.zeros(cmap.shape)
        for j in range(ch):
            for i in range(cw):
                cx = x + (i + 0.5) * sp_per_w
                cx = int(cx // self.w_per_pixel)
                cy = y + (j + 0.5) * sp_per_h
                cy = int(cy // self.h_per_pixel)
                img_slice[j, i] = self.image[cy, cx]

        res = np.linalg.norm(img_slice - self._norm_cmap(cmap))**2 / ch / cw
        return  res * w

    def _norm_cmap(self, cmap):
        return (cmap - self.col_min) / self.col_delta
