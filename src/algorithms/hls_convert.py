from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from image import Image, pixel


def to_hls(pixel: "pixel") -> tuple[float, float, float]:
    r = pixel[0] / 255
    g = pixel[1] / 255
    b = pixel[2] / 255
    maxc = max(r, g, b)
    minc = min(r, g, b)
    sumc = maxc + minc
    rangec = maxc - minc
    l = sumc / 2.0
    if minc == maxc:
        return 0.0, l, 0.0
    if l <= 0.5:
        s = rangec / sumc
    else:
        s = rangec / (2.0 - maxc - minc)
    rc = (maxc - r) / rangec
    gc = (maxc - g) / rangec
    bc = (maxc - b) / rangec
    if r == maxc:
        h = bc - gc
    elif g == maxc:
        h = 2.0 + rc - bc
    else:
        h = 4.0 + gc - rc
    h = (h / 6.0) % 1.0
    return h, l, s


def _v(q, p, t):
    if t > 1:
        t -= 1.0
    if t < 0:
        t += 1.0

    if t < 1 / 6:
        return p + ((q - p) * t * 6.0)
    if 1 / 6 <= t < 1 / 2:
        return q
    if 1 / 2 <= t < 2 / 3:
        return p + ((q - p) * (2 / 3 - t) * 6.0)
    return p


def to_rgb(pixel: "pixel") -> "pixel":
    h, l, s = pixel
    if l < 0.5:
        q = l * (1.0 + s)
    else:
        q = l + s - l * s
    p = 2.0 * l - q
    tr = h + 1 / 3
    tg = h
    tb = h - 1 / 3
    r = int(_v(q, p, tr) * 255)
    g = int(_v(q, p, tg) * 255)
    b = int(_v(q, p, tb) * 255)
    return r, g, b


def rgb_to_hls(image: "Image") -> "Image":
    from image import Image

    pixels: list[list["pixel"]] = []
    for row in image.pixels:
        tmp_row = []
        for pixel_ in row:
            tmp_row.append(to_hls(pixel_))
        pixels.append(tmp_row)

    return Image(pixels=pixels, mode="hls")


def hls_to_rgb(image: "Image") -> "Image":
    from image import Image

    pixels: list[list["pixel"]] = []
    for row in image.pixels:
        tmp_row = []
        for pixel_ in row:
            tmp_row.append(to_rgb(pixel_))
        pixels.append(tmp_row)

    return Image(pixels=pixels, mode="rgb")


def normalize(image: "Image") -> "Image":
    from image import Image

    normalize_ = lambda x: int(x * 255)
    pixels: list[list["pixel"]] = []
    for row in image.pixels:
        tmp_row = []
        for pixel_ in row:
            tmp_row.append(tuple(map(normalize_, pixel_)))
        pixels.append(tmp_row)

    return Image(pixels=pixels, mode="rgb")
