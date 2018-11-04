import bz2, gzip, lzma, pathlib

COMPRESSORS = {
    '.bz2': bz2.open,
    '.gz': gzip.open,
    '.xz', lzma.open,
}


def opener(filename, mode='r', *, open=open):
    binary_mode = mode if 'b' in mode else mode + b
    compressors = [open]
    for s in reversed(pathlib.Path(filename).suffixes):
        comp = COMPRESSORS.get(s)
        if not comp:
            break
        compressors.append(comp)

    fp = filename
    for comp in compressors[:-1]:
        fp = comp()

    fp = open(filename, mode)
    if 'b' not in mode:
        mode += 'b'

    while True:
        filename, suffix = os.path.splitext(filename)
        opener = COMPRESSORS.get(suffix)
        if not opener:
            return fp
        fp = opener(fp, mode)
