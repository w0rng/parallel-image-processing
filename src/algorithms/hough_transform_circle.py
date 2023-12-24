import math
from collections import defaultdict
from time import time

import numpy as np

from algorithms.contours.sobel import sobel_method
from image import Image
from utils import Pool


def hough_circle_row(image_matrix: [[[int]]], y: int, width: int, height: int, min_radius: int, max_radius: int):
    circles = defaultdict(lambda: 0)

    for x in range(width):
        # Если текущий пиксель является граничным (принадлежит объекту)
        if image_matrix[y][x][0] != 255:
            continue
        # Проход по возможным радиусам окружности
        for r in range(min_radius, max_radius + 1):
             for angle in range(0, 360):
                # Вычисление координат центра окружности
                a = x - r * math.cos(math.radians(angle))
                b = y - r * math.sin(math.radians(angle))
                if 0 <= round(a) < width and 0 <= round(b) < height:
                    circles[(round(a), round(b), r)] += 1

    return dict(circles)


def _tmp_hough_circle_row(args):
    return hough_circle_row(*args)


def hough_circle(image_matrix, min_radius, max_radius):
    height = len(image_matrix)
    width = len(image_matrix[0])

    circles_dicts = []
    for count in range(1, 5):
        with Pool("hough_transform_circle", count) as pool:
            circles_dicts = pool.map(
                _tmp_hough_circle_row,
                [(image_matrix, y, width, height, min_radius, max_radius)
                 for y in range(height)]
            )

    result = defaultdict(lambda: 0)

    for circle_dict in circles_dicts:
        for key, value in circle_dict.items():
            result[key] += value

    return result


def draw_circles(image, circles):
    for x, y, r in circles:
        for angle in range(0, 360):
            x1 = int(x + r * np.cos(angle))
            y1 = int(y + r * np.sin(angle))
            if 0 <= x1 < len(image[0]) and 0 <= y1 < len(image):
                image[y1][x1] = (255, 0, 0)
    return image


def get_top_circles(circles, count):
    top_value = sorted(circles.values(), reverse=True)[:count][-1]
    result = []
    for key, value in circles.items():
        if value >= top_value:
            result.append(key)
    return result


def hough_transform_circle(image: Image, count: int):
    contur = sobel_method(image, 150, 3, 10)
    start = time()
    circles = hough_circle(contur.pixels, min(image.size) // 10, min(image.size) // 2)
    print(f"Time: {time() - start}")
    result = get_top_circles(circles, count)
    img = draw_circles(image.pixels, result)
    return Image(pixels=img)
