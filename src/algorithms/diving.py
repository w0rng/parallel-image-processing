from copy import deepcopy
from collections import defaultdict
from random import randint

from algorithms.utils.markers_to_image import markers_to_image
from image import Image
from algorithms.utils.safe_get import safe_get_from_matrix


def diving(image: Image, level_count: int) -> Image:
    if image.mode != 'grayscale':
        image = image.to_grayscale()

    new_image = deepcopy(image)

    _levelize_image(new_image, level_count)

    width, height = new_image.size

    markers = [[0] * width for _ in range(height)]

    curr_marker = 0
    for level in range(level_count):
        for y in range(height):
            for x in range(width):
                p = new_image.pixels[y][x][0]
                top_left_right_bottom_markers = list(filter(lambda v: v, [
                    safe_get_from_matrix(markers, y - 1, x),
                    safe_get_from_matrix(markers, y, x - 1),
                    safe_get_from_matrix(markers, y, x + 1),
                    safe_get_from_matrix(markers, y + 1, x),
                ]))

                if p != level:
                    continue

                if not top_left_right_bottom_markers:
                    curr_marker += 1
                    markers[y][x] = curr_marker
                else:
                    markers[y][x] = min(top_left_right_bottom_markers)

    return markers_to_image(markers)


def _levelize_image(image: Image, level_count: int):
    """Приходит картинка со значениями 0-255, уходит со значениями 0-level_count"""

    width, height = image.size

    divider = 255 // level_count

    for y in range(height):
        for x in range(width):
            p = image.pixels[y][x]
            image.pixels[y][x] = (
                p[0] // divider,
                p[1] // divider,
                p[2] // divider,
            )

if __name__ == "__main__":
    diving(Image(pixels=[
        [(0, 0, 0),    (0, 0, 0),    (0, 0, 0),    (0, 0, 0)],
        [(1, 0, 0),    (2, 0, 0),    (2, 0, 0),    (3, 0, 0)],
        [(1, 0, 0),    (2, 0, 0),    (2, 0, 0),    (4, 0, 0)],
        [(2, 0, 0),    (2, 0, 0),    (1, 0, 0),    (5, 0, 0)],
        [(3, 0, 0),    (1, 0, 0),    (0, 0, 0),    (5, 0, 0)],
        [(3, 0, 0),    (4, 0, 0),    (4, 0, 0),    (4, 0, 0)],
    ], mode='grayscale'), level_count=6)
