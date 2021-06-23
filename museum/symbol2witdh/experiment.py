from trick import symbol2width
from tqdm import tqdm
from random import randint

def score():
    return randint(0, 100)

def translate(seq, letters):
    ans = ''
    for e in seq:
        ans += letters[e]
    return ans

class dppoint():
    def __init__(self, score, sequence):
        self.score = score
        self.sequence = sequence

letters = list('qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъфывапролджэячсмитьбю !?1234567890-+—QWERTYUIOPASDFGHJKLZXCVBNMЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ')  # im lazy

pt = 345
spppt = 65536
size = pt * spppt
size -= 60
size += 3276000
print(size)

widths = []
for l in tqdm(letters):
    widths.append(symbol2width(l))
print(widths)

def dp():
    arr = [None] * (size + 1)
    arr[0] = dppoint(0, [])
    for i in tqdm(range(size), leave=False):
        if arr[i]:
            currsc = arr[i].score
            currseq = arr[i].sequence
            for symbol_ind, w in enumerate(widths):
                if i + w <= size:
                    s = score()
                    if (
                        arr[i+w] is None
                        or currsc + s < arr[i+w].score
                    ):
                        arr[i+w] = dppoint(currsc + s, currseq + [symbol_ind])
            arr[i] = None
    return arr[-1]

answer = ''
for line in tqdm(range(50)):
    answer += translate(dp().sequence, letters) + '\n\n'
print(answer)

