from PyQt6.QtWidgets import *
from src.algorithms.hough_transform_circle import hough_transform_circle


def make_layout(window) -> QBoxLayout:
    make_button = QPushButton("Сделать")
    count_line = QLineEdit(text="100")

    def make_button_clicked():
        hough_transform_circle(window.current_image, int(count_line.text())).show()

    make_button.clicked.connect(make_button_clicked)

    color_models_layout = QHBoxLayout()
    color_models_layout.addWidget(QLabel('Хаф ищет кружочки'))
    color_models_layout.addWidget(count_line)

    color_models_layout.addWidget(make_button)

    return color_models_layout
