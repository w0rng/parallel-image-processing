import numpy as np
from scipy.ndimage import convolve

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

    new_image = Image(pixels=[[image.pixels[y][x] if corners[y][x] != 1 else (255, 0, 0) for x in range(width)] for y in range(height)])

    return new_image
