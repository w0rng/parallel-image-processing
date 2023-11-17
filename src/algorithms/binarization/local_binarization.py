from src.image import Image
from copy import deepcopy
import statistics


def local_binarization(image: Image, block_size: int):
    if image.mode != 'grayscale':
        return image

    image_width, image_height = image.size
    new_image = deepcopy(image)

    half_block = block_size // 2

    for y in range(half_block, image_height - half_block):
        for x in range(half_block, image_width - half_block):
            block = [
                row[x - half_block: x + half_block + 1] for row in image.pixels[y - half_block: y + half_block + 1]
            ]
            block = list(map(lambda row: list(map(lambda elem: elem[0], row)), block))
            block = [element for row in block for element in row]

            threshold = statistics.median(block)

            new_image.pixels[y][x] = (255, 255, 255) if image.pixels[y][x][0] > threshold else (0, 0, 0)

    return new_image
