from typing import TYPE_CHECKING
from copy import deepcopy

if TYPE_CHECKING:
    from image import Image


def linear_filter(image: "Image", kernel: list[list[float]]):
    height, width = image.size

    k_h, k_w = len(kernel), len(kernel[0])
    pixels = image.pixels
    new_image = deepcopy(image)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            pixel_sum = [0, 0, 0]
            for k in range(-1 * (k_h // 2), (k_h // 2) + 1):
                for l in range(-1 * (k_w // 2), (k_w // 2) + 1):
                    y = (i + k) % height
                    x = (j + l) % width

                    pixel_sum[0] += (
                        pixels[x][y][0] * kernel[k + (k_h // 2)][l + (k_w // 2)]
                    )
                    pixel_sum[1] += (
                        pixels[x][y][1] * kernel[k + (k_h // 2)][l + (k_w // 2)]
                    )
                    pixel_sum[2] += (
                        pixels[x][y][2] * kernel[k + (k_h // 2)][l + (k_w // 2)]
                    )

            new_image.pixels[x][y] = (
                int(pixel_sum[0]),
                int(pixel_sum[1]),
                int(pixel_sum[2]),
            )

    return new_image
