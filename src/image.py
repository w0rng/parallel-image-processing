from dataclasses import dataclass
from typing import Literal, Self, TypeAlias

import PIL.Image

from algorithms.grayscale_convert import rgb_to_grayscale

pixel: TypeAlias = tuple[int, int, int] | tuple[float, float, float]


@dataclass
class Image:
    pixels: list[list[pixel]]
    mode: Literal["rgb", "hls", "yuv", "grayscale"] = "rgb"

    @property
    def size(self) -> tuple[int, int]:
        return len(self.pixels[0]), len(self.pixels)

    def show(self):
        pilow_image = PIL.Image.new("RGB", self.size)
        for y, row in enumerate(self.pixels):
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

    def to_grayscale(self) -> Self:
        return rgb_to_grayscale(self)
