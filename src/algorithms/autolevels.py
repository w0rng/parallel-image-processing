from copy import deepcopy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from image import Image, pixel


def rgb_autolevels(image: "Image") -> "Image":
    from image import Image

    if image.mode != "rgb":
        return

    pixels = deepcopy(image.pixels)

    r_min, r_max = _min_and_max_in_chan(pixels, 0)
    g_min, g_max = _min_and_max_in_chan(pixels, 1)
    b_min, b_max = _min_and_max_in_chan(pixels, 2)

    res = []
    for y, row in enumerate(pixels):
        tmp = []
        for x, pixel_ in enumerate(row):
            tmp.append((
                _modify_pixel_chan(pixels[y][x][0], r_min, r_max),
                _modify_pixel_chan(pixels[y][x][1], g_min, g_max),
                _modify_pixel_chan(pixels[y][x][2], b_min, b_max),
            ))
        res.append(tmp)

    return Image(pixels=res, mode="rgb")


def _min_and_max_in_chan(pixels: list[list["pixel"]], chan: int) -> (int, int):
    min = 255
    max = 0

    for row in pixels:
        for pixel in row:
            curr = pixel[chan]
            if curr > max:
                max = curr
            if curr < min:
                min = curr

    return (min, max)


def _modify_pixel_chan(old: int, min: int, max: int) -> int:
    return int((old - min) * 255 / (max - min))
