from src.image import Image, pixel
from copy import deepcopy
from src.laba2.utils.adjust_image_by_mode import adjust_image_by_mode
from src.laba2.utils.clip import clip


def sobel_method(image: Image) -> Image:
    new_image = deepcopy(image)

    image_width, image_height = new_image.size

    sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

    for y in range(1, image_height - 1):
        for x in range(1, image_width - 1):
            gradient_x = (
                new_image.pixels[y - 1][x - 1][0] * sobel_x[0][0] +
                new_image.pixels[y - 1][x][0] * sobel_x[1][0] +
                new_image.pixels[y - 1][x + 1][0] * sobel_x[2][0] +

                new_image.pixels[y][x - 1][0] * sobel_x[0][1] +
                new_image.pixels[y][x][0] * sobel_x[1][1] +
                new_image.pixels[y][x + 1][0] * sobel_x[2][1] +

                new_image.pixels[y + 1][x - 1][0] * sobel_x[0][2] +
                new_image.pixels[y + 1][x][0] * sobel_x[1][2] +
                new_image.pixels[y + 1][x + 1][0] * sobel_x[2][2]
            )

            gradient_y = (
                new_image.pixels[y - 1][x - 1][0] * sobel_y[0][0] +
                new_image.pixels[y - 1][x][0] * sobel_y[1][0] +
                new_image.pixels[y - 1][x + 1][0] * sobel_y[2][0] +

                new_image.pixels[y][x - 1][0] * sobel_y[0][1] +
                new_image.pixels[y][x][0] * sobel_y[1][1] +
                new_image.pixels[y][x + 1][0] * sobel_y[2][1] +

                new_image.pixels[y + 1][x - 1][0] * sobel_y[0][2] +
                new_image.pixels[y + 1][x][0] * sobel_y[1][2] +
                new_image.pixels[y + 1][x + 1][0] * sobel_y[2][2]
            )

            gradient_x = int(clip(gradient_x, 0, 255))
            gradient_y = int(clip(gradient_y, 0, 255))

            magnitude = (gradient_x**2 + gradient_y**2)**0.5
            new_image.pixels[y][x] = (
                magnitude,
                magnitude,
                magnitude
            )

    adjust_image_by_mode(new_image)

    return new_image

