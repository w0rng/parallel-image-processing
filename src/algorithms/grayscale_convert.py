from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.image import Image, pixel


def to_grayscale(current_pixel: "pixel") -> "pixel":
    grayscale_value = int((current_pixel[0] + current_pixel[1] + current_pixel[2]) / 3)
    return grayscale_value, grayscale_value, grayscale_value


def rgb_to_grayscale(image: "Image") -> "Image":
    from image import Image

    pixels = []
    for row in image.pixels:
        tmp_row = []
        for row_pixel in row:
            tmp_row.append(to_grayscale(row_pixel))
        pixels.append(tmp_row)

    return Image(pixels=pixels, mode="grayscale")