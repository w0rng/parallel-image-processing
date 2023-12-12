import numpy as np
from scipy.ndimage import convolve
from copy import deepcopy

from src.image import Image


def harris_corner_detector(image: Image, window_size=3, k=0.04, threshold=0.05):
    if image.mode != 'grayscale':
        image.to_grayscale()

    width, height = image.size

    img = np.array([[pixel[0] for pixel in row] for row in image.pixels])

    Ix = convolve(img, np.array([[-1, 0, 1]]), mode='constant')
    Iy = convolve(img, np.array([[-1], [0], [1]]), mode='constant')

    Ix2 = Ix ** 2
    Iy2 = Iy ** 2
    Ixy = Ix * Iy

    Sx2 = convolve(Ix2, np.ones((window_size, window_size)), mode='constant')
    Sy2 = convolve(Iy2, np.ones((window_size, window_size)), mode='constant')
    Sxy = convolve(Ixy, np.ones((window_size, window_size)), mode='constant')

    # Harris corner response function
    det_M = Sx2 * Sy2 - Sxy ** 2
    trace_M = Sx2 + Sy2
    R = det_M - k * trace_M ** 2

    # Thresholding
    corners = np.zeros_like(R)
    corners[R > threshold * np.max(R)] = 1

    new_image = Image(pixels=[[image.pixels[y][x] if corners[y][x] != 1 else (255, 0, 0) for x in range(width)] for y in
                              range(height)])

    return new_image


def fast_is_corner(image: Image, x: int, y: int, threshold: int):
    pixel_value = image.pixels[y][x][0]
    threshold_values = [pixel_value - threshold, pixel_value + threshold]

    circle_pixels = [
        (x, y - 3), (x + 1, y - 3), (x + 2, y - 2), (x + 3, y - 1),
        (x + 3, y), (x + 3, y + 1), (x + 2, y + 2), (x + 1, y + 3),
        (x, y + 3), (x - 1, y + 3), (x - 2, y + 2), (x - 3, y + 1),
        (x - 3, y), (x - 3, y - 1), (x - 2, y - 2), (x - 1, y - 3)
    ]

    # Check if enough consecutive pixels are brighter or darker than the central pixel
    consecutive_brighter = sum(image.pixels[cy][cx][0] > threshold_values[1] for cx, cy in circle_pixels)
    consecutive_darker = sum(image.pixels[cy][cx][0] < threshold_values[0] for cx, cy in circle_pixels)

    return consecutive_brighter >= 9 or consecutive_darker >= 9


def fast_corner_detector(image: Image, threshold=20) -> Image:
    if image.mode != 'grayscale':
        image.to_grayscale()

    new_image = deepcopy(image)
    width, height = new_image.size

    for y in range(3, height - 3):
        for x in range(3, width - 3):
            if fast_is_corner(new_image, x, y, threshold):
                new_image.pixels[y][x] = (255, 0, 0)

    return new_image
