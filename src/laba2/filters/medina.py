from src.image import Image, pixel
from copy import deepcopy
from src.laba2.utils.adjust_image_by_mode import adjust_image_by_mode
from src.utils import Pool
from statistics import median as median_func



def median(image: Image, radius_x: int, radius_y: int) -> Image:
    new_image = deepcopy(image)

    image_width, image_height = new_image.size

    for y in range(image_height):
        for x in range(image_width):
            total_brightness: tuple[list[int], list[int], list[int]] = ([], [], [])

            for i in range(-radius_x, radius_x + 1):
                for j in range(-radius_y, radius_y + 1):
                    nx = min(image_width - 1, max(0, x + i))
                    ny = min(image_height - 1, max(0, y + j))

                    total_brightness[0].append(new_image.pixels[ny][nx][0])
                    total_brightness[1].append(new_image.pixels[ny][nx][1])
                    total_brightness[2].append(new_image.pixels[ny][nx][2])

            new_image.pixels[y][x] = (
                median_func(total_brightness[0]), median_func(total_brightness[1]), median_func(total_brightness[2])
            )

    adjust_image_by_mode(new_image)

    return new_image
