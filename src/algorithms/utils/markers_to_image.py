from copy import deepcopy
from random import randint

from image import Image


def markers_to_image(markers: list[list[int]]) -> Image:
    rbg_by_marker = dict()

    pixels = deepcopy(markers)

    for y in range(len(pixels)):
        for x in range(len(pixels[0])):
            marker = pixels[y][x]
            if marker not in rbg_by_marker:
                rbg_by_marker[marker] = (
                    randint(0, 255),
                    randint(0, 255),
                    randint(0, 255),
                )
            rbg = rbg_by_marker[marker]
            pixels[y][x] = rbg

    return Image(pixels=pixels, mode='grayscale')
