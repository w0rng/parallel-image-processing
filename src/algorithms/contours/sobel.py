from src.utils import Pool
from src.algorithms.utils.adjust_image_by_mode import adjust_image_by_mode
from src.image import Image, pixel


def sobel_method(image: Image, threshold: float, gain_factor: float, balancing_factor: float) -> Image:
    if image.mode != 'grayscale':
        image = image.to_grayscale()

    image_width, image_height = image.size

    res = []
    for count in range(1, 2):
        with Pool("sobel_method", count) as pool:
            res = pool.map(
                _tmp_row_sobel,
                [(image, gain_factor, threshold,balancing_factor, y)
                 for y in range(1, image_height - 1)]
            )

    new_image = Image(pixels=res, mode='grayscale')

    adjust_image_by_mode(new_image)

    return new_image


def _tmp_row_sobel(args) -> [pixel]:
    return _row_sobel(*args)


def _row_sobel(image: Image, gain_factor: float, threshold: int, balancing_factor: float, y: int) \
        -> [pixel]:
    image_width, image_height = image.size
    res = []

    for x in range(image_width - 1):
        res.append(_get_sobel_modified_pixel(image, gain_factor, threshold, balancing_factor, y, x))
    return res


sobel_x1 = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]
sobel_y1 = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

sobel_x2 = [[2, 1, 0], [1, 0, -1], [0, -1, -2]]
sobel_y2 = [[0, 1, 2], [-1, 0, 1], [-2, -1, 0]]


def _get_sobel_modified_pixel(image: Image, gain_factor: float, threshold: int, balancing_factor: float, y: int, x: int) -> pixel:
    gradient_x1 = (
            image.pixels[y - 1][x - 1][0] * sobel_x1[0][0] +
            image.pixels[y - 1][x][0] * sobel_x1[1][0] +
            image.pixels[y - 1][x + 1][0] * sobel_x1[2][0] +

            image.pixels[y][x - 1][0] * sobel_x1[0][1] +
            image.pixels[y][x][0] * sobel_x1[1][1] +
            image.pixels[y][x + 1][0] * sobel_x1[2][1] +

            image.pixels[y + 1][x - 1][0] * sobel_x1[0][2] +
            image.pixels[y + 1][x][0] * sobel_x1[1][2] +
            image.pixels[y + 1][x + 1][0] * sobel_x1[2][2]
    )

    gradient_y1 = (
            image.pixels[y - 1][x - 1][0] * sobel_y1[0][0] +
            image.pixels[y - 1][x][0] * sobel_y1[1][0] +
            image.pixels[y - 1][x + 1][0] * sobel_y1[2][0] +

            image.pixels[y][x - 1][0] * sobel_y1[0][1] +
            image.pixels[y][x][0] * sobel_y1[1][1] +
            image.pixels[y][x + 1][0] * sobel_y1[2][1] +

            image.pixels[y + 1][x - 1][0] * sobel_y1[0][2] +
            image.pixels[y + 1][x][0] * sobel_y1[1][2] +
            image.pixels[y + 1][x + 1][0] * sobel_y1[2][2]
    )

    gradient_x2 = (
            image.pixels[y - 1][x - 1][0] * sobel_x2[0][0] +
            image.pixels[y - 1][x][0] * sobel_x2[1][0] +
            image.pixels[y - 1][x + 1][0] * sobel_x2[2][0] +

            image.pixels[y][x - 1][0] * sobel_x2[0][1] +
            image.pixels[y][x][0] * sobel_x2[1][1] +
            image.pixels[y][x + 1][0] * sobel_x2[2][1] +

            image.pixels[y + 1][x - 1][0] * sobel_x2[0][2] +
            image.pixels[y + 1][x][0] * sobel_x2[1][2] +
            image.pixels[y + 1][x + 1][0] * sobel_x2[2][2]
    )

    gradient_y2 = (
            image.pixels[y - 1][x - 1][0] * sobel_y2[0][0] +
            image.pixels[y - 1][x][0] * sobel_y2[1][0] +
            image.pixels[y - 1][x + 1][0] * sobel_y2[2][0] +

            image.pixels[y][x - 1][0] * sobel_y2[0][1] +
            image.pixels[y][x][0] * sobel_y2[1][1] +
            image.pixels[y][x + 1][0] * sobel_y2[2][1] +

            image.pixels[y + 1][x - 1][0] * sobel_y2[0][2] +
            image.pixels[y + 1][x][0] * sobel_y2[1][2] +
            image.pixels[y + 1][x + 1][0] * sobel_y2[2][2]
    )

    g1 = (gradient_x1 ** 2 + gradient_y1 ** 2) ** 0.5
    g2 = (gradient_x2 ** 2 + gradient_y2 ** 2) ** 0.5

    return (
        gain_factor * (g1 * balancing_factor + (1 - balancing_factor) * g2),
        gain_factor * (g1 * balancing_factor + (1 - balancing_factor) * g2),
        gain_factor * (g1 * balancing_factor + (1 - balancing_factor) * g2)
    ) if (g1 * balancing_factor + (1 - balancing_factor) * g2) > threshold else (0, 0, 0)