import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from PIL import Image

from src.image import Image


def hough_line_transform(image: Image, theta_res=1, rho_res=1):
    if image.mode != 'grayscale':
        image.to_grayscale()
    width, height = image.size
    max_rho = int(np.sqrt(height ** 2 + width ** 2))

    thetas = np.deg2rad(np.arange(-90, 90, theta_res))
    rhos = np.arange(-max_rho, max_rho, rho_res)

    cos_thetas = np.cos(thetas)
    sin_thetas = np.sin(thetas)

    accumulator = np.zeros((len(rhos), len(thetas)), dtype=np.uint64)

    edges_y, edges_x = np.nonzero(np.array([[pixel[0] for pixel in row] for row in image.pixels]))
    print(edges_x)
    print(edges_y)
    print(len(thetas))
    for i in range(len(edges_x)):
        x = edges_x[i]
        y = edges_y[i]

        for j in range(len(thetas)):
            rho = int(x * cos_thetas[j] + y * sin_thetas[j])
            rho_index = np.argmin(np.abs(rhos - rho))
            accumulator[rho_index, j] += 1

    # print('Accumulator', accumulator)


    return accumulator, thetas, rhos


def hough_circle_transform(image, radius=20, acc_threshold=100):
    height, width = image.shape
    accumulator = np.zeros((height, width), dtype=np.uint64)

    edge_points = np.column_stack(np.nonzero(image))

    for point in edge_points:
        x, y = point
        for theta in np.linspace(0, 2 * np.pi, 100):
            a = int(x - radius * np.cos(theta))
            b = int(y - radius * np.sin(theta))
            if 0 <= a < height and 0 <= b < width:
                accumulator[a, b] += 1

    circle_points = np.column_stack(np.where(accumulator > acc_threshold))

    return circle_points