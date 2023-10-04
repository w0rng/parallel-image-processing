from colorsys import rgb_to_hls

def to_hls(r, g, b):
    r /= 255
    g /= 255
    b /= 255
    maxc = max(r, g, b)
    minc = min(r, g, b)
    sumc = (maxc+minc)
    rangec = (maxc-minc)
    l = sumc/2.0
    if minc == maxc:
        return 0.0, l, 0.0
    if l <= 0.5:
        s = rangec / sumc
    else:
        s = rangec / (2.0-maxc-minc)  # Not always 2.0-sumc: gh-106498.
    rc = (maxc-r) / rangec
    gc = (maxc-g) / rangec
    bc = (maxc-b) / rangec
    if r == maxc:
        h = bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return h, l, s

def row_to_hls(row: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    return list(map(lambda pixel: to_hls(*pixel), row))

def rgb_to_hls(pixels: list[list[tuple[int, int, int]]]) -> list[list[tuple[int, int, int]]]:
    return list(map(row_to_hls, pixels))

def to_yuv(r, g, b) -> tuple[int, int, int]:
    y = 0.299 * r + 0.587 * g + 0.114 * b
    cb = -0.1687 * r - 0.3313 * g + 0.5 * b + 128
    cr = 0.5 * r - 0.4187 * g - 0.0813 * b + 128

    return int(y), int(cb), int(cr)

def row_to_yuv(row: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    return list(map(lambda pixel: to_yuv(*pixel), row))

def rgb_to_yuv(pixels: list[list[tuple[int, int, int]]]) -> list[list[tuple[int, int, int]]]:
    return list(map(row_to_yuv, pixels))

def _hls_as_rgb(h, l, s) -> tuple[int, int, int]:
    return (
        int(h * 255),
        int(l * 255),
        int(s * 255),
    )

def row_hls_as_rgb(row: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    return list(map(lambda pixel: _hls_as_rgb(*pixel), row))

def hls_as_rbg(pixels: list[list[tuple[float, float, float]]]) -> list[list[tuple[int, int, int]]]:
    return list(map(row_hls_as_rgb, pixels))