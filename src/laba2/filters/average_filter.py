from src.image import Image
from copy import deepcopy
from src.laba2.utils.adjust_image_by_mode import adjust_image_by_mode


def average_filter_recursive(image: Image, radius_x: int, radius_y: int) -> Image:
    new_image = deepcopy(image)

    image_width, image_height = new_image.size

    for y in range(0, image_height):
        for x in range(0, image_width):
            total_brightness = (0, 0, 0)
            total_pixels = 0

            for i in range(-radius_x, radius_x + 1):
                for j in range(-radius_y, radius_y + 1):
                    nx, ny = x + i, y + j

                    if 0 <= nx < image_width and 0 <= ny < image_height:
                        pixel = new_image.pixels[ny][nx]
                        total_brightness = (
                            total_brightness[0] + pixel[0], total_brightness[1] + pixel[1],
                            total_brightness[2] + pixel[2])
                        total_pixels += 1

            average_value = (total_brightness[0] / total_pixels, total_brightness[1] / total_pixels,
                             total_brightness[2] / total_pixels) if total_pixels > 0 else (0, 0, 0)
            new_image.pixels[y][x] = average_value

    adjust_image_by_mode(new_image)

    return new_image


# Тут еще рекурсивная реализация
# def average_filter_recursive(image: Image, x: int, y: int, radius_x: int, radius_y: int) -> Image:
#     new_image = deepcopy(image)
#
#     image_width, image_height = new_image.size
#     total_brightness = (0, 0, 0)
#     total_pixels = 0
#
#     for i in range(-radius_x, radius_x + 1):
#         for j in range(-radius_y, radius_y + 1):
#             nx, ny = x + i, y + j
#
#             if 0 <= nx < image_width and 0 <= ny < image_height:
#                 pixel = new_image.pixels[nx][ny]
#                 total_brightness = (
#                     total_brightness[0] + pixel[0], total_brightness[1] + pixel[1], total_brightness[2] + pixel[2])
#                 total_pixels += 1
#
#     average_value = (total_brightness[0] / total_pixels, total_brightness[1] / total_pixels,
#                      total_brightness[2] / total_pixels) if total_pixels > 0 else (0, 0, 0)
#     new_image.pixels[x][y] = average_value
#
#     if x + 1 < image_width:
#         average_filter_recursive(new_image, x + 1, y, radius_x, radius_y)
#     elif y + 1 < image_height:
#         average_filter_recursive(new_image, 0, y + 1, radius_x, radius_y)
#
#     adjust_image_by_mode(new_image)
#
#     return new_image