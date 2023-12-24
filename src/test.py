import math

import numpy as np

from algorithms.contours.sobel import sobel_method
from image import Image


def hough_circle_transform(image):
    rows = len(image)
    cols = len(image[0])

    max_radius = min(rows, cols) // 2
    accumulator = [[[0 for _ in range(max_radius + 1)] for _ in range(cols)] for _ in range(rows)]

    # Проход по всем пикселям изображения
    for y in range(rows):
        for x in range(cols):
            # Если пиксель не является частью окружности, продолжаем
            if image[y][x] != (255, 255, 255):  # На примере белого цвета (255, 255, 255)
                continue

            print("x: ", x, "y: ", y)

            # Просмотр всех радиусов
            for r in range(1, max_radius + 1):
                for theta in range(360):
                    a = x - r * math.cos(math.radians(theta))
                    b = y - r * math.sin(math.radians(theta))

                    # Если центр окружности находится в пределах изображения, увеличиваем значение в аккумуляторе
                    if 0 <= round(a) < cols and 0 <= round(b) < rows:
                        accumulator[round(b)][round(a)][r] += 1

    return accumulator


import math

def draw_circles(image, accumulator, threshold=100):
    rows = len(accumulator)
    cols = len(accumulator[0])

    result_image = [row[:] for row in image]

    # Проход по всем пикселям аккумулятора
    for y in range(rows):
        for x in range(cols):
            for r, t in enumerate(accumulator[y][x]):
                # Если значение в аккумуляторе превышает порог, рисуем окружность
                if t == 1:
                    # Расчет координат центра окружности
                    center_x = x
                    center_y = y

                    # Рисование окружности по формуле окружности
                    for theta in range(360):
                        a = center_x - r * math.cos(math.radians(theta))
                        b = center_y - r * math.sin(math.radians(theta))

                        # Проверка на наличие координат в пределах изображения
                        if 0 <= round(a) < cols and 0 <= round(b) < rows:
                            result_image[round(b)][round(a)] = (255, 0, 0)  # Например, красный цвет для окружности

    return result_image


def get_top_n_from_accumulator(accumulator, n):
    flatten = []
    for y in accumulator:
        for x in y:
            for r in x:
                flatten.append(r)
    return sorted(flatten, reverse=True)[:n]


if __name__ == '__main__':
    # Пример использования:
    # Пусть у вас есть изображение в виде матрицы pixels
    image = Image.load("assets/example.jpeg")
    contur = sobel_method(image, 150, 3, 10)
    result = hough_circle_transform(contur.pixels)
    # print(result)
    print(get_top_n_from_accumulator(result, 100))
    threshold = get_top_n_from_accumulator(result, 100)[-1]
    img = draw_circles(image.pixels, result, threshold)
    Image(pixels=img).show()
