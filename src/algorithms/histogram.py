import numpy as np
import matplotlib.pyplot as plt
from src.image import Image


def calculate_histogram(image: np.ndarray):
    hist, bin_edges = np.histogram(image.flatten(), bins=256, range=(0, 1))
    return hist, bin_edges


def calculate_texture_features(image: Image):
    if image.mode != 'grayscale':
        image.to_grayscale()

    new_image = np.array([[pixel[0] for pixel in row] for row in image.pixels])
    new_image = (new_image - np.min(new_image)) / (np.max(new_image) - np.min(new_image))
    hist, bin_edges = calculate_histogram(new_image)

    mean = np.mean(hist)
    variance = np.var(hist)
    skewness = np.mean(((hist - mean) / np.std(hist)) ** 3)
    kurtosis = np.mean(((hist - mean) / np.std(hist)) ** 4) - 3

    plt.hist(hist)
    plt.title('Histogram')
    plt.text(10, 10, f'variance - {variance}\nskewness - {skewness}\nkurtosis - {kurtosis}')
    plt.show()


