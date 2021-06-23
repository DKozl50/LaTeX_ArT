from subprocess import check_call, DEVNULL

def symbol2width(symbol: str):
    with open('./symbol', 'w') as s:
        s.write(symbol)
    check_call(['pdflatex', './singlewidth.tex'], stdout=DEVNULL)
    check_call(['pdftotext', './singlewidth.pdf', 'width'], stdout=DEVNULL)
    with open('./width', 'r') as w:
        width = w.readline()
    return int(width)
