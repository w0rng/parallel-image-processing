import math

import numpy as np

from algorithms.contours.sobel import sobel_method
from image import Image


def hough_circle(image_matrix, min_radius, max_radius):
    height = len(image_matrix)
    width = len(image_matrix[0])

    # Создание пустого аккумулятора (accumulator)
    accumulator = [[[0 for _ in range(max_radius - min_radius + 1)] for _ in range(width)] for _ in range(height)]

    # Проход по всем пикселям изображения
    for y in range(height):
        for x in range(width):
            # Если текущий пиксель является граничным (принадлежит объекту)
            if image_matrix[y][x] != (
                    0, 0, 0):  # Проверка на черный цвет, можно изменить в зависимости от формата цветов
                # Проход по возможным радиусам окружности
                for r in range(min_radius, max_radius + 1):
                    for angle in range(0, 360):
                        # Вычисление координат центра окружности
                        a = x - r * math.cos(math.radians(angle))
                        b = y - r * math.sin(math.radians(angle))
                        if 0 <= round(a) < width and 0 <= round(b) < height:
                            accumulator[round(b)][round(a)][r - min_radius] += 1

    # Поиск окружностей с числом голосов выше порога
    circles = {}
    for y in range(height):
        for x in range(width):
            for r in range(max_radius - min_radius + 1):
                circles[(x, y, r + min_radius)] = accumulator[y][x][r]

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
    circles = hough_circle(contur.pixels, min(image.size) // 10, min(image.size) // 2)
    result = get_top_circles(circles, count)
    img = draw_circles(image.pixels, result)
    return Image(pixels=img)
