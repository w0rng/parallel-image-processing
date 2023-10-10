from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from image import Image, pixel


def equalization(image: "Image") -> "Image":
    from image import Image

    k = 256
    hr = [0.0] * 256
    hg = [0.0] * 256
    hb = [0.0] * 256
    for row in image.pixels:
        for pixel in row:
            r, g, b = pixel
            hr[int(r)] += 1
            hg[int(g)] += 1
            hb[int(b)] += 1
    cumulative_sum_r = [sum(hr[: i + 1]) for i in range(k)]
    cumulative_sum_g = [sum(hg[: i + 1]) for i in range(k)]
    cumulative_sum_b = [sum(hb[: i + 1]) for i in range(k)]
    normalized_cumulative_sum_r = [
        int(255 * s / cumulative_sum_r[-1]) for s in cumulative_sum_r
    ]
    normalized_cumulative_sum_g = [
        int(255 * s / cumulative_sum_g[-1]) for s in cumulative_sum_g
    ]
    normalized_cumulative_sum_b = [
        int(255 * s / cumulative_sum_b[-1]) for s in cumulative_sum_b
    ]

    pixels: list[list["pixel"]] = []
    for row in image.pixels:
        tmp_row = []
        for pixel in row:
            r, g, b = pixel
            tmp_row.append(
                (
                    normalized_cumulative_sum_r[int(r)],
                    normalized_cumulative_sum_g[int(g)],
                    normalized_cumulative_sum_b[int(b)],
                )
            )
        pixels.append(tmp_row)

    return Image(pixels=pixels, mode=image.mode)
