from copy import deepcopy
from statistics import harmonic_mean

from src.image import Image, pixel
from src.laba2.utils.adjust_image_by_mode import adjust_image_by_mode


def harmonic_mean_filter(image: Image, window_width: int, window_height: int) -> Image:
    new_image = deepcopy(image)

    width, height = image.size

    half_window_width = window_width // 2
    half_window_height = window_height // 2

    for y in range(height):
        for x in range(width):
            start_y = max(0, y - half_window_height)
            end_y = min(height, y + half_window_height + 1)
            start_x = max(0, x - half_window_width)
            end_x = min(width, x + half_window_width + 1)

            chan1 = []
            chan2 = []
            chan3 = []

            for y_ in range(start_y, end_y):
                for x_ in range(start_x, end_x):
                    neighbour_pixel = image.pixels[y_][x_]
                    chan1.append(neighbour_pixel[0])
                    chan2.append(neighbour_pixel[1])
                    chan3.append(neighbour_pixel[2])

            new_image.pixels[y][x] = (
                int(_custom_harmonic_mean(chan1)),
                int(_custom_harmonic_mean(chan2)),
                int(_custom_harmonic_mean(chan3)),
            )

    adjust_image_by_mode(new_image)

    return new_image


def _custom_harmonic_mean(nums):
    summ = 0
    for num in nums:
        if num != 0:
            summ += (1 / num)

    return len(nums) / summ
