from collections import defaultdict
from copy import deepcopy

from PyQt6.QtWidgets import *

from image import Image
from src.algorithms.watershed_segmentation import water_division


def get_random_color():
    import random
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def make_layout(window):
    contours_threshold_value = QLineEdit()
    contours_threshold_value.setPlaceholderText("Пороговое значение")
    button = QPushButton('Сегментировать')

    def button_clicked():
        level = int(contours_threshold_value.text())
        mask = water_division(deepcopy(window.current_image.pixels), level)
        pixels = []
        colors = defaultdict(get_random_color)
        for row in mask:
            row_ = []
            for p in row:
                if p == 0:
                    row_.append((0, 0, 0))
                    continue
                row_.append(colors[p])
            pixels.append(row_)

        Image(pixels=pixels, mode="rgb").show()

    button.clicked.connect(button_clicked)

    layout = QHBoxLayout()
    layout.addWidget(QLabel("Водораздел"))
    layout.addWidget(contours_threshold_value)
    layout.addWidget(button)

    return layout
