from image import Image
from .mse import mse
from math import log10


def psnr(a: Image, b: Image) -> float:
    return 10 * log10((255 ** 2) / mse(a, b))
