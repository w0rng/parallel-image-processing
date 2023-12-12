from src.image import Image
import matplotlib.pyplot as plt
import numpy as np


def generate_laws_masks():
    masks = np.array([
        [1, 4, 6, 4, 1],
        [-1, -2, 0, 2, 1],
        [-1, 0, 2, 0, -1],
        [-1, 2, 0, -2, 1],
        [1, -4, 6, -4, 1]
    ])

    laws_masks = []
    for i in range(5):
        for j in range(5):
            laws_masks.append(np.outer(masks[i], masks[j]))

    return laws_masks


def convolution(image: np.ndarray, kernel: np.ndarray):
    kernel = np.flipud(np.fliplr(kernel))
    output = np.zeros_like(image, dtype=float)

    # Iterate over the image with the kernel
    for i in range(2, image.shape[0] - 2):
        for j in range(2, image.shape[1] - 2):
            output[i, j] = np.sum(image[i - 2:i + 3, j - 2:j + 3] * kernel)

    return output


def laws_energy_map(image: Image) -> Image:
    new_image = np.array([[float(pixel[0]) / 255 for pixel in row] for row in image.pixels], dtype=float)
    laws_masks = generate_laws_masks()
    energy_map = np.array([[0 for _ in row] for row in image.pixels], dtype=float)

    for mask in laws_masks:
        filtered_image = convolution(new_image, mask)
        energy_map += filtered_image**2

    plt.imshow(energy_map, cmap='hot')
    plt.show()
