from dataclasses import dataclass
from typing import Self

import PIL.Image


@dataclass
class Image:
    pixels: list[list[tuple[int, int, int]]]

    @property
    def size(self) -> tuple[int, int]:
        return len(self.pixels[0]), len(self.pixels)

    def show(self, mode: str = "RGB"):
        _image = PIL.Image.new(mode, self.size)
        for y, row in enumerate(self.pixels):
            for x, pixel in enumerate(row):
                _image.putpixel((x, y), pixel)
        _image.show()

    @classmethod
    def load(cls, image_path: str) -> "Self":
        image = PIL.Image.open(image_path)
        pixels: list[list[tuple[int, int, int]]] = []
        for y in range(image.height):
            row = []
            for x in range(image.width):
                row.append(image.getpixel((x, y)))
            pixels.append(row)
        return cls(pixels)
