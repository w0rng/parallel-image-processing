from copy import deepcopy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from image import Image, pixel


def to_yuv(pixel: "pixel") -> tuple[int, int, int]:
    r, g, b = pixel
    y = 0.299 * r + 0.587 * g + 0.114 * b
    u = -0.1687 * r - 0.3313 * g + 0.5 * b + 128
    v = 0.5 * r - 0.4187 * g - 0.0813 * b + 128

    return int(y), int(u), int(v)


def to_rgb(pixel: "pixel") -> "pixel":
    y, u, v = pixel
    r = y + 1.14 * v
    g = y - 0.395 * u - 0.518 * v
    b = y + 2.032 * u
    return int(r), int(g), int(b)


def rgb_to_yuv(image: "Image") -> "Image":
    from image import Image

    pixels: list[list[pixel]] = []
    for row in image.pixels:
        tmp_row = []
        for pixel_ in row:
            tmp_row.append(to_yuv(pixel_))
        pixels.append(tmp_row)

    return Image(pixels=pixels, mode="yuv")


def yuv_to_rgb(image: "Image") -> "Image":
    from image import Image

    pixels: list[list[pixel]] = []
    for row in image.pixels:
        tmp_row = []
        for pixel_ in row:
            tmp_row.append(to_rgb(pixel_))
        pixels.append(tmp_row)

    return Image(pixels=pixels, mode="yuv")


def change_yuv_brightnes_and_contrast(
    image: "Image", brightnes: float, contrast: float
) -> "Image":
    from image import Image

    res = deepcopy(image.pixels)
    for y, row in enumerate(res):
        for x, pixel_ in enumerate(row):
            res[y][x] = (
                int(pixel_[0] * contrast + brightnes),
                pixel_[1],
                pixel_[2],
            )
    return Image(pixels=res, mode="yuv")
