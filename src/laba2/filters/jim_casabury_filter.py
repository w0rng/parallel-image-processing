from copy import deepcopy
import random

from src.image import Image, pixel
from src.laba2.utils.adjust_image_by_mode import adjust_image_by_mode


def jim_casabury_filter(image: Image, window_width: int, window_height: int, threshold: float) -> Image:
    new_image = deepcopy(image)

    width, height = image.size

    for y in range(height):
        for x in range(width):
            tot_red = tot_green = tot_blue = 0
            count_red = count_green = count_blue = 0

            half_window_width = window_width // 2
            half_window_height = window_height // 2

            center_pixel = image.pixels[y][x]

            start_y = max(0, y - half_window_height)
            end_y = min(height, y + half_window_height + 1)
            start_x = max(0, x - half_window_width)
            end_x = min(width, x + half_window_width + 1)

            for y_ in range(start_y, end_y):
                for x_ in range(start_x, end_x):
                    neighbour_pixel = image.pixels[y_][x_]

                    if abs(neighbour_pixel[0] - center_pixel[0]) < threshold:
                        tot_red += neighbour_pixel[0]
                        count_red += 1

                    if abs(neighbour_pixel[1] - center_pixel[1]) < threshold:
                        tot_green += neighbour_pixel[1]
                        count_green += 1

                    if abs(neighbour_pixel[2] - center_pixel[2]) < threshold:
                        tot_blue += neighbour_pixel[2]
                        count_blue += 1

            new_image.pixels[y][x] = (
                int(tot_red / count_red),
                int(tot_green / count_green),
                int(tot_blue / count_blue),
            )

    adjust_image_by_mode(new_image)

    return new_image
