from matplotlib import pyplot as plt

from algorithms.utils.find_t import find_t
from algorithms.utils.rolling_median import rolling_median
from src.algorithms.utils.histogram import histogram
from src.image import Image


def threshold_segmentation(image):
    array = histogram(image)
    rolling_array = rolling_median(array, 3)
    t = find_t(rolling_array)

    for i, e in enumerate(rolling_array):
        plt.bar(i, e, color="black", alpha=0.3)

    plt.axvline(x=t, color='red', linestyle='--')
    plt.show()

    pixels = []
    for row in image.pixels:
        row_ = []
        for pixel in row:
            if pixel[0] > t:
                row_.append((255, 255, 255))
            else:
                row_.append((0, 0, 0))
        pixels.append(row_)

    return Image(pixels=pixels, mode="grayscale")
