from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.image import Image, pixel


def to_grayscale(current_pixel: "pixel") -> "pixel":
    r, g, b = current_pixel
    grayscale_value = int((r + g + b) / 3)
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