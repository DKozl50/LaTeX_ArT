from collections import UserList

from utils import translate, get_info
from score import ScoreFast

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
        return f'{self.symbol}: {self.width},\n{self.colormap}'


class ModList(UserList):
    def __init__(self, mod):
        super().__init__()
        self.mod = mod
        self.data = [None] * mod

    def __getitem__(self, item):
        item = item % self.mod
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        key = key % self.mod
        super().__setitem__(key, value)


# any whitespace is bad
# letters = list('qwertyuiopasdfghjklzxcvbnm'
#                'йцукенгшщзхъфывапролджэячсмитьбю'
#                '!?1234567890-+—.,'
#                'QWERTYUIOPASDFGHJKLZXCVBNM'
#                'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ')
# letters = list('qwertyiopasdfghjklzxcvbnm')
# letters = list('ЙlSf!im-+—vWHabcde')
# letters = list('l—L')
letters = list('.kнRqpмщ6KЮхiOftVYлlушпДzЬчЪu,2-жBвHНZТгgзPAйь4XЭoDMъ+тx1n78IФ?!aдwЧиdыЯc—ЙhкГvИCEц')

nice_len = 36400  # around 0.55 pt
# nice_in_page = 620
nice_in_page = 1000  # landscape
size = nice_len * nice_in_page
# print(size)

# baselineskip is 12pt = 12*65536sp
baselineskip = 12 * 65536


symbols: list[SymbolInfo] = []
for letter in tqdm(letters):
    symbols.append(SymbolInfo(letter, *get_info(letter)))
min_color = min([s.colormap.min() for s in symbols])
max_width = max([s.width for s in symbols])

image = np.array(Image.open('frog.jpg').convert('L'))
lines = round(size / baselineskip / image.shape[1] * image.shape[0])
print(lines)

scorer = ScoreFast(image, size, baselineskip * lines, col_min=min_color)


def dp(height):
    arr = ModList(max_width+1)
    arr[0] = DPNode(0, [])
    for i in tqdm(range(size), leave=False):
        if arr[i]:
            curr_score = arr[i].score
            curr_seq = arr[i].sequence
            for symbol_ind, symb in enumerate(symbols):
                w = symb.width
                if i + w <= size:
                    s = scorer(i, height, w, baselineskip, symb.colormap)
                    if (arr[i + w] is None
                            or curr_score + s < arr[i + w].score):
                        arr[i + w] = DPNode(curr_score + s, curr_seq + [symbol_ind])
            arr[i] = None
    return arr[size]


answer = ''
curr_height = 0
for line in tqdm(range(lines)):
    answer += translate(dp(curr_height).sequence, letters) + '\n\n'
    curr_height += baselineskip
print(answer)
