from subprocess import check_call, DEVNULL

from numpy import array
from PIL import Image


def translate(seq, symbols):
    ans = ''
    for e in seq:
        ans += symbols[e]
    return ans


def get_info(symbol: str):
    with open('./symbol', 'w') as s:
        s.write(symbol)
    check_call(['pdflatex', './singlewidth.tex'], stdout=DEVNULL)
    check_call(['pdftotext', './singlewidth.pdf', './width'], stdout=DEVNULL)
    with open('./width', 'r') as w:
        width = w.readline()
    check_call(['pdflatex', './little.tex'], stdout=DEVNULL)
    check_call([
        'convert',
        '-density', '300',
        'little.pdf',
        '-colorspace', 'Gray',
        '-resize', '1x1!',
        '-quality', '100',
        '-background', 'white',
        '-alpha', 'remove',
        '-alpha', 'off',
        'map.png'
    ])

    # dirty conversion
    # TODO: rewrite this mess
    img = array(Image.open('./map.png'), dtype=float)
    img /= 65535

    return int(width), img[0, 0]
