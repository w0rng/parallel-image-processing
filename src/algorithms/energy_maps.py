from src.image import Image
from src.utils import Pool
import matplotlib.pyplot as plt
import numpy as np

'''
    Оставил реализацию на np, т.к. и с ним получилось норм распараллелить
    
    1;56,975768089294434
    2;29,430114030838013
    3;21,12345314025879
    4;17,068299055099487
    
    А если еще и цифры подшаманить, вообще красота будет
'''


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


def _tmp_row_convolution (args) -> np.ndarray:
    return convolution(*args)


def convolution(image: np.ndarray, kernel: np.ndarray):
    kernel = np.flipud(np.fliplr(kernel))
    output = np.zeros_like(image, dtype=float)

    # Iterate over the image with the kernel
    for i in range(2, image.shape[0] - 2):
        for j in range(2, image.shape[1] - 2):
            output[i, j] = np.sum(image[i - 2:i + 3, j - 2:j + 3] * kernel)

    return output


def laws_energy_map(image: Image):
    new_image = np.array([[float(pixel[0]) / 255 for pixel in row] for row in image.pixels], dtype=float)
    laws_masks = generate_laws_masks()
    energy_map = np.array([[0 for _ in row] for row in image.pixels], dtype=float)

    res = []
    for count in range(1, 5):
        with Pool("energy_maps", count) as pool:
            res = pool.map(
                _tmp_row_convolution,
                [(new_image, mask)
                 for mask in laws_masks]
            )


    for image in res:
        energy_map += image**2

    plt.imshow(energy_map, cmap='hot')
    plt.show()
