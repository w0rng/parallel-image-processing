from image import Image
from .delta import delta
from .mse import mse


def calc(name: str, time: float, noise_image: Image, filtered_image: Image):
    delta_ = delta(noise_image, filtered_image)
    mse_ = mse(filtered_image, noise_image)
    print(name, time, delta_, mse_)
