from copy import deepcopy

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from image import Image, pixel


def rgb_piecewise_linear_histogram_correction(image: "Image", correcting_points: list[(int, int)]):
    from image import Image

    prepared_correcting_points: list[(int, int)] = [(0, 0)] + correcting_points + [(255, 255)]
    xs = [point[0] for point in prepared_correcting_points]
    ys = [point[1] for point in prepared_correcting_points]

    spline = make_interp_spline(xs, ys)

    res = deepcopy(image.pixels)
    for y, row in enumerate(res):
        for x, pixel_ in enumerate(row):
            res[y][x] = (
                int(spline(int(pixel_[0]))),
                int(spline(int(pixel_[1]))),
                int(spline(int(pixel_[2]))),
            )

    _show_chart(spline, xs, ys)

    Image(pixels=res, mode=image.mode).show()


def hls_piecewise_linear_histogram_correction(image: "Image", correcting_points: list[(int, int)]):
    from image import Image

    prepared_correcting_points: list[(int, int)] = [(0, 0)] + correcting_points + [(1, 1)]
    xs = [point[0] for point in prepared_correcting_points]
    ys = [point[1] for point in prepared_correcting_points]

    spline = make_interp_spline(xs, ys)

    res = deepcopy(image.pixels)
    for y, row in enumerate(res):
        for x, pixel_ in enumerate(row):
            res[y][x] = (
                spline(pixel_[0]),
                spline(pixel_[1]),
                spline(pixel_[2]),
            )

    _show_chart(spline, xs, ys)

    Image(pixels=res, mode=image.mode).show()


def parse_points_string(string: str) -> list[(float, float)]:
    def string_point_to_point(string_point: str) -> (float, float):
        string = string_point.replace(")", "").replace("(", "")
        nums = string.split(",")
        return float(nums[0]), float(nums[1])

    string_points = string.split(" ")
    points = [string_point_to_point(string_point) for string_point in string_points]
    return points


def _show_chart(spline: BSpline, x: list[int], y: list[int]):
    x_smooth = np.linspace(min(x), max(x), 300)
    y_smooth = spline(x_smooth)

    plt.plot(x_smooth, y_smooth, label='Smooth Curve', color='blue')
    plt.scatter(x, y, marker='o', label='Data Points', color='red')

    # Add labels and a legend
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    plt.title('Plotting a Smooth Curve Through Given Points')
    plt.legend()

    plt.show()