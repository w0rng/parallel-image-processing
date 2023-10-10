from copy import deepcopy
from typing import Literal
from random import uniform

from image import Image
from laba2.utils.random_coordinates_set_by_percent import random_coordinates_set_by_percent
from laba2.utils.adjust_image_by_mode import adjust_image_by_mode


def make_noize_multiplicatively(
    image: Image,
    percent: float,
    chosen_channel: int,
    multiplicator_range_start: float,
    multiplicator_range_end: float,
) -> Image:
    assert 0 <= percent <= 1

    new_image = deepcopy(image)

    coordinates = random_coordinates_set_by_percent(new_image, percent)

    for (x, y) in coordinates:
        p = new_image.pixels[y][x]
        multiplicator = uniform(multiplicator_range_start, multiplicator_range_end)
        new_image.pixels[y][x] = (
            p[0] * multiplicator if chosen_channel == 0 else p[0],
            p[1] * multiplicator if chosen_channel == 1 else p[1],
            p[2] * multiplicator if chosen_channel == 2 else p[2],
        )

    adjust_image_by_mode(new_image)

    return new_image