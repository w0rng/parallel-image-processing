from copy import deepcopy

from src.algorithms.utils.adjust_image_by_mode import adjust_image_by_mode
from src.image import Image


def laplace_method(image: Image, threshold: float, gain_factor: float, laplace_kernel: list[list[int]]) -> Image:
    if image.mode != 'grayscale':
        image = image.to_grayscale()

    image_width, image_height = image.size
    res_pixels = deepcopy(image.pixels)

    for y in range(1, image_height - 1):
        for x in range(1, image_width - 1):
            # TODO: Сделать универсальным (не только для 3на3 ядра)
            g = (
                    image.pixels[y - 1][x - 1][0] * laplace_kernel[0][0] +
                    image.pixels[y - 1][x][0] * laplace_kernel[1][0] +
                    image.pixels[y - 1][x + 1][0] * laplace_kernel[2][0] +

                    image.pixels[y][x - 1][0] * laplace_kernel[0][1] +
                    image.pixels[y][x][0] * laplace_kernel[1][1] +
                    image.pixels[y][x + 1][0] * laplace_kernel[2][1] +

                    image.pixels[y + 1][x - 1][0] * laplace_kernel[0][2] +
                    image.pixels[y + 1][x][0] * laplace_kernel[1][2] +
                    image.pixels[y + 1][x + 1][0] * laplace_kernel[2][2]
            )

            res_pixels[y][x] = (
                gain_factor * g,
                gain_factor * g,
                gain_factor * g
            ) if g > threshold else (0, 0, 0)

    new_image = Image(pixels=res_pixels, mode='grayscale')

    adjust_image_by_mode(new_image)

    return new_image
