from copy import deepcopy
from typing import TYPE_CHECKING

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
    for y, row in enumerate(pixels):
        tmp = []
        for x, pixel_ in enumerate(row):
            tmp.append((
                grey_world_pixel_modify(pixels[y][x][0], avg_r, avg),
                grey_world_pixel_modify(pixels[y][x][1], avg_g, avg),
                grey_world_pixel_modify(pixels[y][x][2], avg_b, avg)
            ))
        res.append(tmp)

    return Image(pixels=res, mode="rgb")


def grey_world_pixel_modify(old: int, avg_channel: int, avg: int) -> int:
    return int(old * (avg / avg_channel))
