import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve

from src.image import Image
from src.utils import Pool


def generate_laws_masks():
    L5 = np.array([1, 4, 6, 4, 1])
    E5 = np.array([-1, -2, 0, 2, 1])
    S5 = np.array([-1, 0, 2, 0, -1])
    W5 = np.array([1, -4, 6, -4, 1])

    L5E5 = np.outer(L5, E5)
    E5L5 = np.outer(E5, L5)
    L5S5 = np.outer(L5, S5)
    S5L5 = np.outer(S5, L5)
    E5S5 = np.outer(E5, S5)
    S5E5 = np.outer(S5, E5)
    E5W5 = np.outer(E5, W5)
    W5E5 = np.outer(W5, E5)
    S5W5 = np.outer(S5, W5)
    W5S5 = np.outer(W5, S5)
    W5W5 = np.outer(W5, W5)
    S5S5 = np.outer(S5, S5)

    L5L5 = np.outer(L5, L5)
    E5E5 = np.outer(E5, E5)

    masks = [L5E5, E5L5, L5S5, S5L5, E5S5, S5E5, E5W5, W5E5, S5W5, W5S5, W5W5, S5S5, E5E5, S5S5, W5W5]

    return masks


def compute_energy_map(image: np.ndarray, mask):
    convolved_image = convolve(image, mask)
    energy_map = np.abs(convolved_image)

    return energy_map


def _tmp_row_convolution (args) -> np.ndarray:
    return compute_energy_map(*args)


def generate_laws_energy_maps(image: Image):
    if image.mode != 'grayscale':
        image.to_grayscale()

    masks = generate_laws_masks()
    new_image = np.array([[pixel[0] for pixel in row] for row in image.pixels])

    energy_maps = []

    for count in range(4, 5):
        with Pool("energy_maps", count) as pool:
            energy_maps = pool.map(
                _tmp_row_convolution,
                [(new_image, mask)
                 for mask in masks]
            )

    return energy_maps


def display_energy_maps(energy_maps):
    fig, axes = plt.subplots(3, 5, figsize=(15, 10))
    fig.suptitle("Laws' Energy Maps")

    for i, ax in enumerate(axes.flatten()):
        ax.imshow(energy_maps[i], cmap='gray')
        ax.set_title(f'Map {i + 1}')

    plt.show()
