import math
from collections import defaultdict
from copy import deepcopy

from algorithms.contours.sobel import sobel_method
from image import Image


def hough_transform(image):
    height = len(image)
    width = len(image[0])
    theta_max = 180  # Максимальное значение угла theta (в градусах)

    # Инициализация массива аккумуляторов
    accumulator = defaultdict(lambda: 0)
    coss = {theta: math.cos(math.radians(theta)) for theta in range(theta_max)}
    sins = {theta: math.sin(math.radians(theta)) for theta in range(theta_max)}

    for y in range(height):
        for x in range(width):
            if image[y][x][0] != 255:  # Если текущий пиксель не является фоном (не черный)
                continue
            for theta in range(theta_max):
                # Преобразование координат изображения в параметры прямой (ρ, theta)
                rho = int(x * coss[theta] + y * sins[theta])
                accumulator[(rho, theta)] += 1  # Увеличиваем значение в аккумуляторе

    return accumulator


def draw_detected_lines(image, detected_lines):
    height = len(image)
    width = len(image[0])

    for line in detected_lines:
        rho, theta = line
        a = math.cos(math.radians(theta))
        b = math.sin(math.radians(theta))
        if math.isclose(b, 0):  # Обработка вертикальных линий
            for y in range(height):
                x = int((rho - y * b) / a)
                if 0 <= x < width:
                    image[y][x] = (255, 0, 0)
        else:
            for x in range(width):
                y = int((rho - x * a) / b)
                if 0 <= y < height:
                    image[y][x] = (255, 0, 0)

    return image


def get_top_n_max(matrix, n):
    # Преобразование матрицы в одномерный список
    top_value = sorted(matrix.values(), reverse=True)[:n][-1]
    result = []
    for key, value in matrix.items():
        if value >= top_value:
            result.append(key)
    return result


def hough_transform_linear(image: Image, count_lines: int = 10) -> Image:
    image = deepcopy(image)
    contur = sobel_method(image, 150, 3, 10)

    accumulator = hough_transform(contur.pixels)
    lines = get_top_n_max(accumulator, count_lines)

    pixels = draw_detected_lines(image.pixels, lines)
    return Image(pixels=pixels)


__all__ = ["hough_transform_linear"]
