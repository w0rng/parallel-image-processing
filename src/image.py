from dataclasses import dataclass
from typing import Literal, Self, TypeAlias

import PIL.Image

from src.algorithms.grayscale_convert import rgb_to_grayscale, hls_to_grayscale, yuv_to_grayscale
from src.algorithms.hls_convert import rgb_to_hls, hls_to_rgb, normalize
from src.algorithms.yuv_convert import rgb_to_yuv, yuv_to_rgb, change_yuv_brightness_and_contrast

pixel: TypeAlias = tuple[int, int, int] | tuple[float, float, float]


@dataclass
class Image:
    pixels: list[list[pixel]]
    mode: Literal["rgb", "hls", "yuv", "grayscale"] = "rgb"

    @property
    def size(self) -> tuple[int, int]:
        return len(self.pixels[0]), len(self.pixels)

    def show(self, *, convert_to_rgb: bool = False):
        pilow_image = PIL.Image.new("RGB", self.size)
        image = self.to_rgb() if convert_to_rgb else self.stupid_normalize()
        for y, row in enumerate(image.pixels):
            for x, pixel in enumerate(row):
                pilow_image.putpixel((x, y), pixel)
        pilow_image.show()

    @classmethod
    def load(cls, image_path: str) -> "Self":
        image = PIL.Image.open(image_path)
        pixels: list[list[pixel]] = []
        for y in range(image.height):
            row = []
            for x in range(image.width):
                row.append(image.getpixel((x, y)))
            pixels.append(row)
        return cls(pixels)

    def to_hls(self) -> Self:
        return rgb_to_hls(self)

    def to_yuv(self) -> Self:
        return rgb_to_yuv(self)

    def change_yuv_brightness_and_contrast(
            self, brightness: int, contrast: float
    ) -> Self:
        image = self
        if image.mode != "yuv":
            image = image.to_yuv()
        return change_yuv_brightness_and_contrast(image, brightness, contrast)

    def to_rgb(self) -> Self:
        if self.mode == "hls":
            image = hls_to_rgb(self)
            return image
        if self.mode == "yuv":
            return yuv_to_rgb(self)
        return self

    def stupid_normalize(self) -> Self:
        if self.mode == "hls":
            return normalize(self)
        return self

    def to_grayscale(self) -> Self:
        if self.mode == 'rgb':
            return rgb_to_grayscale(self)
        if self.mode == 'hls':
            return hls_to_grayscale(self)
        if self.mode == 'yuv':
            return yuv_to_grayscale(self)

        return  self
