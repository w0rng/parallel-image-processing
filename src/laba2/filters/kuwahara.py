from copy import deepcopy
import random

from src.image import Image, pixel
from src.laba2.utils.adjust_image_by_mode import adjust_image_by_mode


def average_pixel(pixels: list[list[pixel]]) -> pixel:
    average = (0, 0, 0)
    width, height = len(pixels[0]), len(pixels)
    pixels_count = width * height

    for row in pixels:
        for current_pixel in row:
            average = (average[0] + current_pixel[0], average[1] + current_pixel[1], average[2] + current_pixel[2])

    average = (average[0] / pixels_count, average[1] / pixels_count, average[2] / pixels_count)
    return average


def variance_pixel(pixels: list[list[pixel]], average_pixel_value: pixel) -> pixel:
    variance = (0, 0, 0)
    width, height = len(pixels[0]), len(pixels)
    pixels_count = width * height

    for row in pixels:
        for current_pixel in row:
            variance = (
                variance[0] + ((current_pixel[0] - average_pixel_value[0]) ** 2),
                variance[1] + ((current_pixel[1] - average_pixel_value[1]) ** 2),
                variance[2] + ((current_pixel[2] - average_pixel_value[2]) ** 2)
            )

    variance = (variance[0] / pixels_count, variance[1] / pixels_count, variance[2] / pixels_count)
    return variance[0], variance[1], variance[2]


def kuwahara_filter(image: Image, window_size: int = 5 ):
    if window_size % 2 == 0:
        return

    new_image = deepcopy(image)
    mode = new_image.mode

    if mode == 'rgb':
        new_image = new_image.to_hls()
    elif mode == 'yuv':
        new_image = new_image.to_rgb().to_hls()

    image_width, image_height = new_image.size
    half_size = window_size // 2

    for y in range(half_size, image_height - half_size):
        for x in range(half_size, image_width - half_size):
            subwindows = [
                [row[x - half_size: x] for row in new_image.pixels[y - half_size: y]],
                [row[x + 1: x + half_size + 1] for row in new_image.pixels[y - half_size: y]],
                [row[x - half_size: x] for row in new_image.pixels[y + 1: y + half_size + 1]],
                [row[x + 1: x + half_size + 1] for row in new_image.pixels[y + 1: y + half_size + 1]]
            ]

            averages = [average_pixel(subwindow) for subwindow in subwindows]
            average_of_averages = (
                 (averages[0][0] + averages[1][0] + averages[2][0] + averages[3][0]) / 4,
                 (averages[0][1] + averages[1][1] + averages[2][1] + averages[3][1]) / 4,
                 (averages[0][2] + averages[1][2] + averages[2][2] + averages[3][2]) / 4
                )
            variances = []
            for i in range(0, 4):
                variances.append(variance_pixel(subwindows[i], average_of_averages))

            min_variance_index = 0
            min_variance = 100_000
            for i in range(0, 4):
                current_variance = variances[i][1]
                if current_variance <= min_variance:
                    min_variance = current_variance
                    min_variance_index = i

            new_image.pixels[y][x] = averages[min_variance_index]

    adjust_image_by_mode(new_image)

    if new_image.mode != mode:
        if mode == 'rgb':
            new_image = new_image.to_rgb()
        else:
            new_image = new_image.to_rgb().to_yuv()

    return new_image
