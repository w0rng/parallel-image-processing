from copy import deepcopy
from typing import Literal
from random import randrange, choice

from image import Image
from laba2.utils.random_coordinates_set_by_percent import random_coordinates_set_by_percent


def make_noize_multiplicatively(
    image: Image,
    percent: float,
    chosen_channel: int,
    multiplicator_range: range
) -> Image:
    assert 0 <= percent <= 1

    new_image = deepcopy(image)

    coordinates = random_coordinates_set_by_percent(new_image, percent)

    multiplicators = list(multiplicator_range)
    for (x, y) in coordinates:
        p = new_image.pixels[y][x]
        multiplicator = choice(multiplicators)
        new_image.pixels[y][x] = (
            p[0] * multiplicator if chosen_channel == 0 else p[0],
            p[1] * multiplicator if chosen_channel == 1 else p[1],
            p[2] * multiplicator if chosen_channel == 2 else p[2],
        )

    return new_image
