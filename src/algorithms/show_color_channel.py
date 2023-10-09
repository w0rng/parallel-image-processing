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


def rgb_pixel_channel(pixel: "pixel", chosen_channel: int) -> "pixel":
    return (
        pixel[0] if chosen_channel == 0 else 0,
        pixel[1] if chosen_channel == 1 else 0,
        pixel[2] if chosen_channel == 2 else 0,
    )


def hls_pixel_channel(pixel: "pixel", chosen_channel: int) -> "pixel":
    if chosen_channel == 0:
        return (pixel[0] + 0.5, 255, 255)
    elif chosen_channel == 1:
        return (0, pixel[1], 0)
    else:
        return (0, 0.5, pixel[2])

def yuv_pixel_channel(pixel: "pixel", chosen_channel: int) -> "pixel":
    if chosen_channel == 0:
        return (pixel[0], 0, 0)
    elif chosen_channel == 1:
        return (125, pixel[1], 0)
    else:
        return (125, 0, pixel[2])


def image_channel_matrix(image: "Image", chosen_channel: int) -> "Image":
    from image import Image

    pixels: list[list["pixel"]] = []

    for row in image.pixels:
        tmp_row = []
        for pixel_ in row:
            if image.mode == 'rgb':
                tmp_row.append(hls_pixel_channel(pixel_, chosen_channel))
            elif image.mode == 'hls':
                tmp_row.append(hls_pixel_channel(pixel_, chosen_channel))
            else:
                tmp_row.append(yuv_pixel_channel(pixel_, chosen_channel))

        pixels.append(tmp_row)

    res_image = Image(pixels=pixels, mode=image.mode)

    return res_image
