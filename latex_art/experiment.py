from typing import Optional

from utils import translate, get_info
from score import ScoreController

from tqdm import tqdm
from PIL import Image
import numpy as np


class DPNode:
    def __init__(self, score, sequence):
        self.score = score
        self.sequence = sequence


class SymbolInfo:
    def __init__(self, symbol, width, colormap):
        self.symbol = symbol
        self.width = width
        self.colormap = colormap

    def __repr__(self):
        return f'{self.symbol}: {self.width},\t{self.colormap}'


# any whitespace is bad
# letters = list('qwertyuiopasdfghjklzxcvbnm'
#                'йцукенгшщзхъфывапролджэячсмитьбю'
#                '!?1234567890-+—'
#                'QWERTYUIOPASDFGHJKLZXCVBNM'
#                'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ')
# letters = list('qwertyiopasdfghjklzxcvbnm')
letters = list('ЙlSf!im-+—vWHabcde')
# letters = list('l—')

nice_len = 36400  # around 0.55 pt
nice_in_page = 700
size = nice_len * nice_in_page
# print(size)

# baselineskip is 12pt = 12*65536sp
baselineskip = 12 * 65536

symbols: list[SymbolInfo] = []
for letter in tqdm(letters):
    symbols.append(SymbolInfo(letter, *get_info(letter)))
# print(symbols)
# for symb in symbols:
#     print(symb.symbol)
# for symb in symbols:
#     print(symb.width)
# for symb in symbols:
#     print(symb.colormap)
# tmp_colors = [s.colormap for s in symbols]

image = np.array(Image.open('test.jpg').convert('L'))
lines = round(size / baselineskip / image.shape[1] * image.shape[0])
print(lines)

scorer = ScoreController(image, size, baselineskip * lines)

def dp(height):
    arr: list[Optional[DPNode]] = [None] * (size + 1)
    arr[0] = DPNode(0, [])
    for i in tqdm(range(size), leave=False):
        if arr[i]:
            curr_score = arr[i].score
            curr_seq = arr[i].sequence
            for symbol_ind, symb in enumerate(symbols):
                w = symb.width
                if i + w <= size:
                    s = scorer(i, height, w, baselineskip, symb.colormap)
                    # # score symbols according to their brightness
                    # # now it should result in a gradient-ish latex-art
                    # s = color_penalty_score(
                    #     i, height,
                    #     w,
                    #     symb.colormap,
                    #     size,
                    #     baselineskip * 30,
                    #     min(tmp_colors),
                    #     max(tmp_colors),
                    # )  # TODO better score
                    if (arr[i + w] is None
                            or curr_score + s < arr[i + w].score):
                        arr[i + w] = DPNode(curr_score + s, curr_seq + [symbol_ind])
            arr[i] = None
    return arr[-1]


answer = ''
curr_height = 0
for line in tqdm(range(lines)):
    answer += translate(dp(curr_height).sequence, letters) + '\n\n'
    curr_height += baselineskip
print(answer)
