from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from image import Image, pixel


def sedate(image: "Image", gamma: float) -> "Image":
    from image import Image

    pixels: list[list["pixel"]] = []
    for row in image.pixels:
        tmp_row = []
        for pixel in row:
            tmp_row.append(
                (
                    int(255 * (pixel[0] / 255) ** gamma),
                    int(255 * (pixel[1] / 255) ** gamma),
                    int(255 * (pixel[2] / 255) ** gamma),
                )
            )
        pixels.append(tmp_row)
    return Image(pixels=pixels, mode=image.mode)
