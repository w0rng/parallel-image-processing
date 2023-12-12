from PyQt6.QtWidgets import *
from src.algorithms.energy_maps import laws_energy_map


def make_layout(window) -> QBoxLayout:
    make_button = QPushButton("Сделать")

    def make_button_clicked():
        laws_energy_map(window.current_image)

    make_button.clicked.connect(make_button_clicked)

    color_models_layout = QHBoxLayout()
    color_models_layout.addWidget(QLabel('Текстурная карта'))

    color_models_layout.addWidget(make_button)

    return color_models_layout
