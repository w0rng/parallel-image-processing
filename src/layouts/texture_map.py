from PyQt6.QtWidgets import *
from src.algorithms.energy_maps import display_energy_maps, generate_laws_energy_maps


def make_layout(window) -> QBoxLayout:
    make_button = QPushButton("Сделать")

    def make_button_clicked():
        energy_maps = generate_laws_energy_maps(window.current_image)
        display_energy_maps(energy_maps)

    make_button.clicked.connect(make_button_clicked)

    color_models_layout = QHBoxLayout()
    color_models_layout.addWidget(QLabel('Текстурная карта'))

    color_models_layout.addWidget(make_button)

    return color_models_layout
