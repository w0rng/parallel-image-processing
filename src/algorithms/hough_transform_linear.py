import math

from algorithms.contours.sobel import sobel_method
from image import Image


def hough_transform(image):
    height = len(image)
    width = len(image[0])
    max_rho = int(math.sqrt(height ** 2 + width ** 2))  # Максимальное значение ρ - диагональ изображения
    theta_max = 180  # Максимальное значение угла theta (в градусах)

    # Инициализация массива аккумуляторов
    accumulator = [[0 for _ in range(theta_max)] for _ in range(2 * max_rho)]

    for y in range(height):
        for x in range(width):
            if sum(image[y][x]) == 255 * 3:  # Если текущий пиксель не является фоном (не черный)
                for theta in range(theta_max):
                    # Преобразование координат изображения в параметры прямой (ρ, theta)
                    rho = int(x * math.cos(math.radians(theta)) + y * math.sin(math.radians(theta)))
                    accumulator[rho + max_rho][theta] += 1  # Увеличиваем значение в аккумуляторе

    return accumulator, max_rho, theta_max


def detect_lines(accumulator, max_rho, theta_max, threshold=100):
    lines = []
    for rho in range(len(accumulator)):
        for theta in range(theta_max):
            if accumulator[rho][theta] > threshold:
                rho_val = rho - max_rho
                lines.append((rho_val, theta))
    return lines


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
    flattened_matrix = [num for row in matrix for num in row]

    # Сортировка списка в порядке убывания
    flattened_matrix.sort(reverse=True)

    top_10_values = flattened_matrix[:n]

    return top_10_values


def hough_transform_linear(image: Image, count_lines: int = 10) -> Image:
    contur = sobel_method(image, 150, 3, 10)

    accumulator, max_rho, theta_max = hough_transform(contur.pixels)
    threshold = get_top_n_max(accumulator, count_lines)[-1]

    detected_lines = detect_lines(accumulator, max_rho, theta_max, threshold=threshold)

    pixels = draw_detected_lines(image.pixels, detected_lines)
    return Image(pixels=pixels)


__all__ = ["hough_transform_linear"]
