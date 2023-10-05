from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from image import Image, pixel


def pixel_color(pixel: "pixel", select_chans: list[int]) -> "pixel":
    return (
        pixel[0] if 0 in select_chans else 0,
        pixel[1] if 1 in select_chans else 0,
        pixel[2] if 2 in select_chans else 0,
    )


def matrix_pixel_color(image: "Image", select_chans: list[int]) -> "Image":
    from image import Image

    pixels: list[list["pixel"]] = []
    for row in image.pixels:
        tmp_row = []
        for pixel_ in row:
            tmp_row.append(pixel_color(pixel_, select_chans))
        pixels.append(tmp_row)

    return Image(pixels=pixels, mode=image.mode)
