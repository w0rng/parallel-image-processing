import math
from collections import defaultdict
from copy import deepcopy

from algorithms.contours.sobel import sobel_method
from image import Image
from utils import Pool


def hough_transform_row(pixels, y: int, width: int, theta_max: int) -> dict:
    accumulator = defaultdict(lambda: 0)

    for x in range(width):
        if pixels[y][x][0] != 255:  # Если текущий пиксель не является фоном (не черный)
            continue
        for theta in range(theta_max):
            # Преобразование координат изображения в параметры прямой (ρ, theta)
            rho = int(x * math.cos(math.radians(theta)) + y * math.sin(math.radians(theta)))
            accumulator[(rho, theta)] += 1  # Увеличиваем значение в аккумуляторе

    return dict(accumulator)


def _tmp_hough_circle_row(args):
    return hough_transform_row(*args)


def hough_transform(image):
    height = len(image)
    width = len(image[0])
    theta_max = 180  # Максимальное значение угла theta (в градусах)

    dicts = []
    for count in range(1, 5):
        with Pool("hough_transform_linear", count) as pool:
            dicts = pool.map(
                _tmp_hough_circle_row,
                [(image, y, width, theta_max) for y in range(height)]
            )

    result = defaultdict(lambda: 0)

    for d in dicts:
        for key, value in d.items():
            result[key] += value

    return result


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
