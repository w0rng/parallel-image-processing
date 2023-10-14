from typing import TYPE_CHECKING

from utils import Pool

if TYPE_CHECKING:
    from image import Image, pixel


def _equalization_row(row: list["pixel"]) -> tuple[list[int], list[int], list[int]]:
    k = 256
    hr = [0] * 256
    hg = [0] * 256
    hb = [0] * 256

    for pixel in row:
        r, g, b = pixel
        hr[int(r)] += 1
        hg[int(g)] += 1
        hb[int(b)] += 1

    return hr, hg, hb


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def sum_rows(matrix):
    r = [0] * len(matrix[0])
    for row in matrix:
        for i, el in enumerate(row):
            r[i] += el
    cumulative_sum_r = [sum(r[: i + 1]) for i in range(256)]
    return [int(255 * s / cumulative_sum_r[-1]) for s in cumulative_sum_r]


def _equalization(image: "Image", count: int) -> "Image":
    from image import Image

    with Pool("equalization_sum", count) as pool:
        result = pool.map(_equalization_row, image.pixels)
        t_result = transpose(result)
    with Pool("equalization_calc", count) as pool:
        hr, hg, hb = pool.map(sum_rows, t_result)

    pixels: list[list["pixel"]] = []
    for row in image.pixels:
        tmp_row = []
        for pixel in row:
            r, g, b = pixel
            tmp_row.append(
                (
                    hr[int(r)],
                    hg[int(g)],
                    hb[int(b)],
                )
            )
        pixels.append(tmp_row)

    return Image(pixels=pixels, mode="rgb")


def equalization(image: "Image") -> "Image":
    r = None
    for i in range(1, 5):
        r = _equalization(image, i)
    return r
