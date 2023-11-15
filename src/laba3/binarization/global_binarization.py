from src.image import Image
from copy import deepcopy


def global_binarization(image: Image, threshold: int) -> Image:
    if image.mode != 'grayscale':
        return image

    image_width, image_height = image.size
    new_image = deepcopy(image)

    for y in range(image_height):
        for x in range(image_width):
            new_image.pixels[y][x] = (255, 255, 255) if new_image.pixels[y][x][0] > threshold else (0, 0, 0)

    return new_image
