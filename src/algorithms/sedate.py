from typing import TYPE_CHECKING

from utils import Pool

if TYPE_CHECKING:
    from image import Image, pixel


def row_sedate(row: list["pixel"], gamma: float) -> list["pixel"]:
    tmp_row = []
    for pixel in row:
        tmp_row.append(
            (
                int(255 * (pixel[0] / 255) ** gamma),
                int(255 * (pixel[1] / 255) ** gamma),
                int(255 * (pixel[2] / 255) ** gamma),
            )
        )
    return tmp_row


def tmp(args):
    return row_sedate(*args)


def sedate(image: "Image", gamma: float) -> "Image":
    from image import Image

    pixels: list[list["pixel"]] = []

    for count in range(1, 5):
        with Pool("sedate", count) as pool:
            pixels = pool.map(tmp, [(row, gamma) for row in image.pixels])
    return Image(pixels=pixels, mode=image.mode)
