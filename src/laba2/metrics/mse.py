from image import Image
from math import sqrt


def mse(a: Image, b: Image) -> float:
    a_width, a_height = a.size
    b_width, b_height = b.size

    min_width = min(a_width, b_width)
    min_height = min(a_height, b_height)

    result = 0
    for y in range(min_height):
        for x in range(min_width):
            for channel in range(3):
                result += (a.pixels[y][x][channel] - b.pixels[y][x][channel])**2

    return sqrt(result / min_height / min_height / 3)
