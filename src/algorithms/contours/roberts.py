from src.image import Image
from src.algorithms.utils.adjust_image_by_mode import adjust_image_by_mode
from copy import deepcopy


def roberts_method(image: Image, threshold: float, gain_factor: float) -> Image:
    if image.mode != 'grayscale':
        image = image.to_grayscale()

    res_pixels = deepcopy(image.pixels)

    image_width, image_height = image.size

    roberts_x = [[1, 0], [0, -1]]
    roberts_y = [[0, 1], [-1, 0]]

    for y in range(1, image_height - 1):
        for x in range(1, image_width - 1):
            gx = (roberts_x[0][0] * image.pixels[y - 1][x - 1][0] +
                  roberts_x[0][1] * image.pixels[y - 1][x][0] +
                  roberts_x[1][0] * image.pixels[y][x - 1][0] +
                  roberts_x[1][1] * image.pixels[y][x][0])

            gy = (roberts_y[0][0] * image.pixels[y - 1][x - 1][0] +
                  roberts_y[0][1] * image.pixels[y - 1][x][0] +
                  roberts_y[1][0] * image.pixels[y][x - 1][0] +
                  roberts_y[1][1] * image.pixels[y][x][0])

            g = (gx**2 + gy**2)**0.5

            res_pixels[y][x] = (g * gain_factor, g * gain_factor, g * gain_factor) if g > threshold else (0, 0, 0)

    new_image = Image(pixels=res_pixels, mode='grayscale')

    adjust_image_by_mode(new_image)

    return new_image
