from PyQt6.QtWidgets import *

from src.algorithms.regional_sprawl import regional_sprawl


def make_layout(window):
    delta_edit = QLineEdit()
    delta_edit.setPlaceholderText('Дельта')

    button = QPushButton('Сделать')

    def button_clicked():
        delta = int(delta_edit.text())
        new_image = regional_sprawl(window.current_image, delta)
        new_image.show()

    button.clicked.connect(button_clicked)

    layout = QHBoxLayout()
    layout.addWidget(QLabel("Алгоритм разрастания регионов"))
    layout.addWidget(delta_edit)
    layout.addWidget(button)

    return layout
