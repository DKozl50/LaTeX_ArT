from abc import ABC, abstractmethod
from fractions import Fraction

import numpy as np


def multiple_floor(num, divisor):
    # round the result down to a multiple of divisor
    return int(num / divisor) * divisor


def empty_mean(arr: np.ndarray):
    if arr.size == 0:
        return 0
    else:
        return arr.mean()


class BaseScore(ABC):
    def __init__(self, image: np.ndarray, width, height, col_min=0, col_max=1):
        # image  --  numpy array
        # width, height  --  in sp
        self.image = image
        self.width = width
        self.height = height
        self.col_min = col_min
        self.col_delta = col_max - col_min
        n, m = image.shape
        self.w_per_pixel = Fraction(width, m)
        self.h_per_pixel = Fraction(height, n)

    def __call__(self, x, y, w, h, cmap):
        # x, y  --  top left coordinates of a symbol in sp
        # w, h  --  width and height of a symbol

        ch, cw = cmap.shape
        sp_per_w = Fraction(w, cw)
        sp_per_h = Fraction(h, ch)
        img_slice = np.zeros(cmap.shape)
        for j in range(ch):
            for i in range(cw):
                cx = x + i * sp_per_w
                cy = y + j * sp_per_h
                img_slice[j, i] = self.calc_pixel(cx, cy, sp_per_w, sp_per_h)

        res = np.linalg.norm(img_slice - self._norm_cmap(cmap))**2 * w / ch / cw
        return res

    def _norm_cmap(self, cmap):
        return (cmap - self.col_min) / self.col_delta

    @abstractmethod
    def calc_pixel(self, x: int, y: int, w, h):
        pass


class ScoreClever(BaseScore):
    def calc_pixel(self, x: int, y: int, w, h):
        #   x  first_x  last_x right
        #   v    v         v    v
        #   |----|---------|----| < y
        #   |    |         |    |
        #   |    |         |    |
        #   |----+---------+----| < first_y
        #   |    |         |    |
        #   |    |         |    |
        #   |----+---------+----| < last_y
        #   |    |         |    |
        #   |    |         |    |
        #   |----|---------|----| < bottom
        #
        #   first_* and last_* are multiples of corresponding *_per_pixel
        res = 0
        right = x + w
        bottom = y + h

        first_x = min(multiple_floor(x + self.w_per_pixel, self.w_per_pixel), right)
        last_x = max(multiple_floor(right, self.w_per_pixel), x)
        if first_x > last_x:
            first_x, last_x = last_x, first_x
            flip_x = True
        else:
            flip_x = False

        # same applies to y
        first_y = min(multiple_floor(y + self.h_per_pixel, self.h_per_pixel), bottom)
        last_y = max(multiple_floor(bottom, self.h_per_pixel), y)
        if first_y > last_y:
            first_y, last_y = last_y, first_y
            flip_y = True
        else:
            flip_y = False

        img_x = int(x // self.w_per_pixel)
        img_first_x = int(first_x // self.w_per_pixel)
        img_last_x = int(last_x // self.w_per_pixel)
        img_y = int(y // self.h_per_pixel)
        img_first_y = int(first_y // self.h_per_pixel)
        img_last_y = int(last_y // self.h_per_pixel)

        # corners
        res += self.image[img_y, img_x] * (first_x - x) * (first_y - y)
        if area := (right - last_x) * (first_y - y):
            res += self.image[img_y, img_last_x] * area
        if area := (first_x - x) * (bottom - last_y):
            res += self.image[img_last_y, img_x] * area
        if area := (right - last_x) * (bottom - last_y):
            res += self.image[img_last_y, img_last_x] * area

        fl_slice_x = slice(img_first_x, img_last_x + (1 if flip_x else 0))
        fl_slice_y = slice(img_first_y, img_last_y + (1 if flip_y else 0))

        # edges
        res += empty_mean(self.image[fl_slice_y, img_x]) * (last_y - first_y) * (first_x - x)
        if area := (last_y - first_y) * (right - last_x):
            res += empty_mean(self.image[fl_slice_y, img_last_x]) * area
        res += empty_mean(self.image[img_y, fl_slice_x]) * (first_y - y) * (last_x - first_x)
        if area := (bottom - last_y) * (last_x - first_x):
            res += empty_mean(self.image[img_last_y, fl_slice_x]) * area

        # middle
        res += empty_mean(self.image[fl_slice_y, fl_slice_x]) * (last_y - first_y) * (last_x - first_x)
        res /= w * h  # area
        return res


class ScoreFast(BaseScore):
    def calc_pixel(self, x: int, y: int, w, h):
        x += w/2
        y += h/2
        img_x = int(x // self.w_per_pixel)
        img_y = int(y // self.h_per_pixel)
        return self.image[img_y, img_x]
