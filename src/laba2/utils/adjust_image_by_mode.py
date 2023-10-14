from image import Image
from laba2.utils.clip import clip


def adjust_image_by_mode(image: Image):
    if image.mode == "rgb":
        _rbg_adjust_image(image)
    elif image.mode == "hls":
        _hls_adjust_image(image)
    elif image.mode == "yuv":
        # В разных изображениях выдают разные минимумы и максимумы каналов, я хз как это подгонять
        # (0 255) (-21 56) (-120 39)
        # (5 253) (-98 43) (-75 142)
        pass


def _rbg_adjust_image(image: Image):
    for y, row in enumerate(image.pixels):
        for x, p in enumerate(row):
            image.pixels[y][x] = (
                int(clip(p[0], 0, 255)),
                int(clip(p[1], 0, 255)),
                int(clip(p[2], 0, 255)),
            )


def _hls_adjust_image(image: Image):
    for y, row in enumerate(image.pixels):
        for x, p in enumerate(row):
            image.pixels[y][x] = (
                clip(p[0], 0, 1),
                clip(p[1], 0, 1),
                clip(p[2], 0, 1),
            )