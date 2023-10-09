from typing import TYPE_CHECKING

import matplotlib.pyplot as plt

if TYPE_CHECKING:
    from image import Image


def show_histogram(image: "Image") -> None:
    """построение гистограммы для выбранного канала заданной цветовой модели"""
    r_channel = [0] * 256
    g_channel = [0] * 256
    b_channel = [0] * 256
    for row in image.pixels:
        for pixel in row:
            r_channel[pixel[0]] += 1
            g_channel[pixel[1]] += 1
            b_channel[pixel[2]] += 1
    max_r = max(r_channel)
    max_g = max(g_channel)
    max_b = max(b_channel)
    for i in range(256):
        r_channel[i] = r_channel[i] / max_r * 256
        g_channel[i] = g_channel[i] / max_g * 256
        b_channel[i] = b_channel[i] / max_b * 256

    plt.figure(figsize=(8, 6))
    plt.hist(r_channel, alpha=0.5, label=f"Канал {image.mode[0]}", color="red")
    plt.hist(g_channel, alpha=0.5, label=f"Канал {image.mode[1]}", color="green")
    plt.hist(b_channel, alpha=0.5, label=f"Канал {image.mode[2]}", color="blue")
    plt.xlabel("Интенсивность", size=14)
    plt.ylabel("Количество", size=14)
    plt.title("Разложение картинки по каналам")
    plt.legend(loc="upper right")
    plt.show()
