import math
from collections import defaultdict
from time import time

import numpy as np
from joblib import Parallel, delayed

from algorithms.contours.sobel import sobel_method
from image import Image


def hough_circle(image_matrix, min_radius, max_radius):
    height = len(image_matrix)
    width = len(image_matrix[0])

    # Создание пустого аккумулятора (accumulator)
    circles = defaultdict(lambda: 0)
    coss = {angle: math.cos(math.radians(angle)) for angle in range(0, 360)}
    sins = {angle: math.sin(math.radians(angle)) for angle in range(0, 360)}

    # Проход по всем пикселям изображения
    for y in range(height):
        for x in range(width):
            # Если текущий пиксель является граничным (принадлежит объекту)
            if image_matrix[y][x][0] != 255:
                continue
            # Проход по возможным радиусам окружности
            for r in range(min_radius, max_radius + 1):
                for angle in range(0, 360):
                    # Вычисление координат центра окружности
                    a = x - r * coss[angle]
                    b = y - r * sins[angle]
                    if 0 <= round(a) < width and 0 <= round(b) < height:
                        circles[(round(a), round(b), r)] += 1

    return circles


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


def run_hough_transform_with_joblib(image, count):
    return Parallel(n_jobs=-1)(delayed(hough_transform_circle)(image, count) for _ in range(1))[0]
