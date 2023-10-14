from copy import deepcopy
from random import random

from image import Image
from laba2.utils.adjust_image_by_mode import adjust_image_by_mode
from laba2.utils.random_coordinates_set_by_percent import \
    random_coordinates_set_by_percent


def make_noise_pulse(
    image: Image,
    percent: float,
    chosen_channel: float,
    percent_black: float,
) -> Image:
    assert 0 <= percent <= 1

    new_image = deepcopy(image)

    coordinates = random_coordinates_set_by_percent(new_image, percent)
    black = 0
    white = 255
    for x, y in coordinates:
        p = new_image.pixels[y][x]
        color = black if random() < percent_black else white
        new_image.pixels[y][x] = (
            color if chosen_channel == 0 else p[0],
            color if chosen_channel == 1 else p[1],
            color if chosen_channel == 2 else p[2],
        )

    adjust_image_by_mode(new_image)

    return new_image
