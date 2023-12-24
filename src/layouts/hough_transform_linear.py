from PyQt6.QtWidgets import *
from src.algorithms.hough_transform_linear import hough_transform_linear


def make_layout(window) -> QBoxLayout:
    make_button = QPushButton("Сделать")

    def make_button_clicked():
        hough_transform_linear(window.current_image).show()

    make_button.clicked.connect(make_button_clicked)

    color_models_layout = QHBoxLayout()
    color_models_layout.addWidget(QLabel('Хаф ищет линии'))

    color_models_layout.addWidget(make_button)

    return color_models_layout
