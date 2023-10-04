from typing import TYPE_CHECKING

import matplotlib.pyplot as plt

if TYPE_CHECKING:
    from image import Image


def show_histogram(image: "Image") -> None:
    """построение гистограммы для выбранного канала заданной цветовой модели"""
    data1 = [pixel[0] for row in image.pixels for pixel in row]
    data2 = [pixel[1] for row in image.pixels for pixel in row]
    data3 = [pixel[2] for row in image.pixels for pixel in row]

    plt.figure(figsize=(8, 6))
    plt.hist(data1, alpha=0.5, label="ch1", color="red")
    plt.hist(data2, alpha=0.5, label="ch2", color="green")
    plt.hist(data3, alpha=0.5, label="ch2", color="blue")
    plt.xlabel("Data", size=14)
    plt.ylabel("Count", size=14)
    plt.title("Разложение картинки по каналам")
    plt.legend(loc="upper right")
    plt.show()
