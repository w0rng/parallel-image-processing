from src.image import Image, pixel
from src.utils import Pool
from src.algorithms.utils.adjust_image_by_mode import adjust_image_by_mode


def roberts_method(image: Image, threshold: float, gain_factor: float) -> Image:
    if image.mode != 'grayscale':
        image = image.to_grayscale()

    image_width, image_height = image.size

    res = []
    for count in range(1, 5):
        with Pool("roberts_method", count) as pool:
            res = pool.map(
                _tmp_row_roberts,
                [(image, gain_factor, threshold, y)
                 for y in range(1, image_height - 1)]
            )

    new_image = Image(pixels=res, mode='grayscale')

    adjust_image_by_mode(new_image)

    return new_image


def _tmp_row_roberts(args) -> [pixel]:
    return _row_roberts(*args)


def _row_roberts(image: Image, gain_factor: float, threshold: int, y: int) \
        -> [pixel]:
    image_width, image_height = image.size
    res = []

    for x in range(image_width - 1):
        res.append(_get_roberts_modified_pixel(image, gain_factor, threshold, y, x))
    return res


roberts_x = [[1, 0], [0, -1]]
roberts_y = [[0, 1], [-1, 0]]


def _get_roberts_modified_pixel(image: Image, gain_factor: float, threshold: int, y: int, x: int) -> pixel:
    gx = (roberts_x[0][0] * image.pixels[y - 1][x - 1][0] +
          roberts_x[0][1] * image.pixels[y - 1][x][0] +
          roberts_x[1][0] * image.pixels[y][x - 1][0] +
          roberts_x[1][1] * image.pixels[y][x][0])

    gy = (roberts_y[0][0] * image.pixels[y - 1][x - 1][0] +
          roberts_y[0][1] * image.pixels[y - 1][x][0] +
          roberts_y[1][0] * image.pixels[y][x - 1][0] +
          roberts_y[1][1] * image.pixels[y][x][0])

    g = (gx ** 2 + gy ** 2) ** 0.5

    return (g * gain_factor, g * gain_factor, g * gain_factor) if g > threshold else (0, 0, 0)