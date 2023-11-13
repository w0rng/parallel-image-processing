from image import Image, pixel
from copy import deepcopy
import numpy as np
from collections import defaultdict
from utils import Pool

from statistics import median_high

from laba2.utils.adjust_image_by_mode import adjust_image_by_mode


def local_histogram_filter(image: Image, window_size: int) -> Image:
    width, height = image.size
    half_window = window_size // 2

    res = []
    for count in range(1, 5):
        with Pool("local_histogram_filter", count) as pool:
            res = pool.map(
                _tmp_row_local_histogram_filter,
                [(image, width, height, y, half_window) for y in range(height)]
            )

    new_image = Image(pixels=res)

    adjust_image_by_mode(new_image)

    return new_image


def _tmp_row_local_histogram_filter(args) -> [pixel]:
    return _row_local_histogram_filter(*args)


def _row_local_histogram_filter(image: Image, width: int, height: int, y: int, half_window: int) -> [pixel]:
    res = []
    for x in range(width):
        res.append(_get_median_pixel(image, x, y, half_window, width, height))
    return res


def _get_median_pixel(image: Image, x: int, y: int, half_window: int, width: int, height: int) -> pixel:
    start_y = max(0, y - half_window)
    end_y = min(height, y + half_window + 1)
    start_x = max(0, x - half_window)
    end_x = min(width, x + half_window + 1)

    chan1 = defaultdict(lambda: 0)
    chan2 = defaultdict(lambda: 0)
    chan3 = defaultdict(lambda: 0)

    for y_ in range(start_y, end_y):
        for x_ in range(start_x, end_x):
            p = image.pixels[y_][x_]
            chan1[p[0]] += 1
            chan2[p[1]] += 1
            chan3[p[2]] += 1

    chan1 = {v: k for k, v in chan1.items()}
    chan2 = {v: k for k, v in chan2.items()}
    chan3 = {v: k for k, v in chan3.items()}

    return (
        chan1[median_high(chan1.keys())],
        chan2[median_high(chan2.keys())],
        chan3[median_high(chan3.keys())],
    )

if __name__ == '__main__':
    image = Image.load('../../assets/example.jpeg')
    print(_get_median_pixel(image, 40, 40, 2, image.size[0], image.size[1]))