from PyQt6.QtWidgets import *
from src.algorithms.histogram import calculate_texture_features


def make_layout(window) -> QBoxLayout:
    make_button = QPushButton("Сделать")

    def make_button_clicked():
        calculate_texture_features(window.current_image)

    make_button.clicked.connect(make_button_clicked)

    color_models_layout = QHBoxLayout()
    color_models_layout.addWidget(QLabel('Гистограмма'))

    color_models_layout.addWidget(make_button)

    return color_models_layout
