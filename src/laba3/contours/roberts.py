from src.image import Image, pixel
from copy import deepcopy


def roberts_method(image: Image, threshold: int, gain_factor: int) -> Image:
    new_image = deepcopy(image)
    pixels = new_image.pixels

    image_width, image_height = new_image.size

    roberts_x = [[1, 0], [0, -1]]
    roberts_y = [[0, 1], [-1, 0]]

    for y in range(1, image_height - 1):
        for x in range(1, image_width - 1):
            gx = (roberts_x[0][0] * pixels[y - 1][x - 1][0] +
                  roberts_x[0][1] * pixels[y - 1][x][0] +
                  roberts_x[1][0] * pixels[y][x - 1][0] +
                  roberts_x[1][1] * pixels[y][x][0],
                  roberts_x[0][0] * pixels[y - 1][x - 1][1] +
                  roberts_x[0][1] * pixels[y - 1][x][1] +
                  roberts_x[1][0] * pixels[y][x - 1][1] +
                  roberts_x[1][1] * pixels[y][x][1],
                  roberts_x[0][0] * pixels[y - 1][x - 1][2] +
                  roberts_x[0][1] * pixels[y - 1][x][2] +
                  roberts_x[1][0] * pixels[y][x - 1][2] +
                  roberts_x[1][1] * pixels[y][x][2]
                )

            gy = (roberts_y[0][0] * pixels[y - 1][x - 1][0] +
                  roberts_y[0][1] * pixels[y - 1][x][0] +
                  roberts_y[1][0] * pixels[y][x - 1][0] +
                  roberts_y[1][1] * pixels[y][x][0],
                  roberts_y[0][0] * pixels[y - 1][x - 1][1] +
                  roberts_y[0][1] * pixels[y - 1][x][1] +
                  roberts_y[1][0] * pixels[y][x - 1][1] +
                  roberts_y[1][1] * pixels[y][x][1],
                  roberts_y[0][0] * pixels[y - 1][x - 1][2] +
                  roberts_y[0][1] * pixels[y - 1][x][2] +
                  roberts_y[1][0] * pixels[y][x - 1][2] +
                  roberts_y[1][1] * pixels[y][x][2]
            )

            energy = (
                int((gx[0]**2 + gy[0]**2)**0.5),
                int((gx[1]**2 + gy[1]**2)**0.5),
                int((gx[2]**2 + gy[2]**2)**0.5)
            )

            new_image.pixels[y][x] = (255, 255, 255) if energy[0] > 50 else (0, 0, 0)

    return new_image
