import json

from PyQt6.QtWidgets import *

from src.algorithms.diving import diving


def make_layout(window):
    count_levels_edit = QLineEdit()
    count_levels_edit.setPlaceholderText('Количество уровней')

    button = QPushButton('Расширение')

    def button_clicked():
        count_levels = int(count_levels_edit.text())
        new_image = diving(window.current_image, count_levels)
        new_image.show()

    button.clicked.connect(button_clicked)

    layout = QHBoxLayout()
    layout.addWidget(QLabel("Алгоритм «погружения»"))
    layout.addWidget(count_levels_edit)
    layout.addWidget(button)

    return layout
