from src.utils import Pool
from src.algorithms.utils.adjust_image_by_mode import adjust_image_by_mode
from src.image import Image, pixel


def laplace_method(image: Image, threshold: float, gain_factor: float, laplace_kernel: list[list[int]]) -> Image:
    if image.mode != 'grayscale':
        image = image.to_grayscale()

    image_width, image_height = image.size

    res = []
    for count in range(1, 5):
        with Pool("laplace_method", count) as pool:
            res = pool.map(
                _tmp_row_laplace,
                [(image, gain_factor, threshold, laplace_kernel, y)
                 for y in range(1, image_height - 1)]
            )

    new_image = Image(pixels=res, mode='grayscale')

    adjust_image_by_mode(new_image)

    return new_image


def _tmp_row_laplace(args) -> [pixel]:
    return _row_laplace(*args)


def _row_laplace(image: Image, gain_factor: float, threshold: int, laplace_kernel: list[list[int]], y: int) \
        -> [pixel]:
    image_width, image_height = image.size
    res = []

    for x in range(image_width - 1):
        res.append(_get_laplace_modified_pixel(image, gain_factor, threshold, laplace_kernel, y, x))
    return res


def _get_laplace_modified_pixel(image: Image, gain_factor: float, threshold: int, laplace_kernel: list[list[int]], y: int, x: int) -> pixel:
    g = (
            image.pixels[y - 1][x - 1][0] * laplace_kernel[0][0] +
            image.pixels[y - 1][x][0] * laplace_kernel[1][0] +
            image.pixels[y - 1][x + 1][0] * laplace_kernel[2][0] +

            image.pixels[y][x - 1][0] * laplace_kernel[0][1] +
            image.pixels[y][x][0] * laplace_kernel[1][1] +
            image.pixels[y][x + 1][0] * laplace_kernel[2][1] +

            image.pixels[y + 1][x - 1][0] * laplace_kernel[0][2] +
            image.pixels[y + 1][x][0] * laplace_kernel[1][2] +
            image.pixels[y + 1][x + 1][0] * laplace_kernel[2][2]
    )

    return (
        gain_factor * g,
        gain_factor * g,
        gain_factor * g
    ) if g > threshold else (0, 0, 0)