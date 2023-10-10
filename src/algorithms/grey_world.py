from copy import deepcopy
from typing import TYPE_CHECKING
from utils import Pool

if TYPE_CHECKING:
    from image import Image


def grey_world_correction(image: "Image") -> "Image":
    from image import Image

    if image.mode != "rgb":
        return

    pixels = deepcopy(image.pixels)

    avg_r = 1
    avg_g = 1
    avg_b = 1

    for y, row in enumerate(pixels):
        for x, pixel_ in enumerate(row):
            avg_r += pixels[y][x][0]
            avg_g += pixels[y][x][1]
            avg_b += pixels[y][x][2]

    avg_r = int(avg_r / (len(pixels[0]) * len(pixels[0][0])))
    avg_g = int(avg_g / (len(pixels[0]) * len(pixels[0][0])))
    avg_b = int(avg_b / (len(pixels[0]) * len(pixels[0][0])))
    avg = int((avg_r + avg_g + avg_b) / 3)

    res = []

    for count in range(1, 5):
        with Pool('grey_world', count) as pool:
            res = pool.map(
                _tmp_row_grey_world,
                [(p, avg_r, avg_g, avg_b, avg) for p in pixels]
            )

    return Image(pixels=res, mode="rgb")


def _tmp_row_grey_world(args):
    return _row_grey_world(*args)


def _row_grey_world(row: list["pixel"], avg_r: int, avg_g: int, avg_b: int, avg: int) -> list["pixel"]:
    res = []
    for p in row:
        res.append((
            grey_world_pixel_modify(p[0], avg_r, avg),
            grey_world_pixel_modify(p[1], avg_g, avg),
            grey_world_pixel_modify(p[2], avg_b, avg)
        ))
    return res


def grey_world_pixel_modify(old: int, avg_channel: int, avg: int) -> int:
    return int(old * (avg / avg_channel))
