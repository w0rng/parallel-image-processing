from image import Image
from copy import deepcopy

from laba2.utils.adjust_image_by_mode import adjust_image_by_mode
from laba2.models.kernel import Kernel


def linear_filter(image: Image, kernel: Kernel) -> Image:
    new_image = deepcopy(image)

    image_width, image_height = new_image.size
    kernel_width, kernel_height = kernel.size

    pad_height = kernel_height // 2
    pad_width = kernel_width // 2

    for y in range(pad_height, image_height - pad_height):
        for x in range(pad_width, image_width - pad_width):
            roi = [row[x - pad_width:x + pad_width + 1] for row in new_image.pixels[y - pad_height:y + pad_height + 1]]

            channels_sums = [0, 0, 0]
            for i in range(kernel_height):
                for j in range(kernel_width):
                    channels_sums[0] += roi[i][j][0] * kernel.coefficients[i][j]
                    channels_sums[1] += roi[i][j][1] * kernel.coefficients[i][j]
                    channels_sums[2] += roi[i][j][2] * kernel.coefficients[i][j]

            new_image.pixels[y][x] = (channels_sums[0], channels_sums[1], channels_sums[2])

    adjust_image_by_mode(new_image)

    return new_image
