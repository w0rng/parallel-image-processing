from src.image import Image, pixel
from src.utils import Pool

from src.laba2.utils.adjust_image_by_mode import adjust_image_by_mode
from src.laba2.models.kernel import Kernel


def linear_filter(image: Image, kernel: Kernel) -> Image:
    image_width, image_height = image.size
    kernel_width, kernel_height = kernel.size

    pad_height = kernel_height // 2

    res = []
    for count in range(1, 5):
        with Pool("linear_filter", count) as pool:
            res = pool.map(
                _tmp_row_linear_filter,
                [(image, image_width, kernel_width, kernel_height, kernel.coefficients[0][0], y)
                 for y in range(pad_height, image_height - pad_height)]
            )

    new_image = Image(pixels=res)

    adjust_image_by_mode(new_image)

    return new_image


def _tmp_row_linear_filter(args) -> [pixel]:
    return _row_linear_filter(*args)


def _row_linear_filter(image: Image, image_width: int, kernel_width: int, kernel_height: int, coef: float, y: int) \
        -> [pixel]:
    res = []

    for x in range(kernel_width // 2, image_width - kernel_width // 2):
        res.append(_get_filtered_pixel(image, kernel_height, kernel_width, coef, x, y))
    return res


def _get_filtered_pixel(image: Image, kernel_height: int, kernel_width: int, coef: float, x: int, y: int) -> pixel:
    roi = [row[x - kernel_width // 2: x + kernel_width // 2 + 1]
           for row in image.pixels[y - kernel_height // 2: y + kernel_height // 2 + 1]]

    channels_sums = [0, 0, 0]
    for i in range(kernel_height):
        for j in range(kernel_width):
            channels_sums[0] += roi[i][j][0] * coef
            channels_sums[1] += roi[i][j][1] * coef
            channels_sums[2] += roi[i][j][2] * coef

    return channels_sums[0], channels_sums[1], channels_sums[2]