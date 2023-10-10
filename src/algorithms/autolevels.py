from copy import deepcopy
from typing import TYPE_CHECKING

from utils import Pool

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
    for count in range(1, 5):
        with Pool("rgb_autolevels", count) as pool:
            res = pool.map(
                _tmp_row_rgb_autolevels,
                [(p, r_min, r_max, g_min, g_max, b_min, b_max) for p in image.pixels]
            )

    return Image(pixels=res, mode="rgb")


def _tmp_row_rgb_autolevels(args):
    return _row_rgb_autolevels(*args)

def _row_rgb_autolevels(row: list["pixel"], r_min: int, r_max: int, g_min: int, g_max: int, b_min: int, b_max: int) -> list["pixel"]:
    res = []
    for p in row:
        res.append((
            _modify_pixel_chan(p[0], r_min, r_max),
            _modify_pixel_chan(p[1], g_min, g_max),
            _modify_pixel_chan(p[2], b_min, b_max),
        ))
    return res


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
