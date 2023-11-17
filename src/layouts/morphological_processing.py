import json

from PyQt6.QtWidgets import *

from src.laba3.morphological_processing import dilation, erosion


def make_layout(window):
    morphological_processing_mask = QLineEdit()
    morphological_processing_mask.setPlaceholderText('Маска. В виде [[0, 1], [1, 0]]')

    dilation_button = QPushButton('Расширение')

    def morphological_processing_dilation_clicked():
        mask = json.loads(morphological_processing_mask.text())
        new_image = dilation(window.current_image, mask)
        new_image.show()

    dilation_button.clicked.connect(morphological_processing_dilation_clicked)

    erosion_button = QPushButton('Сужение')

    def morphological_processing_erosion_clicked():
        mask = json.loads(morphological_processing_mask.text())
        new_image = erosion(window.current_image, mask)
        new_image.show()

    erosion_button.clicked.connect(morphological_processing_erosion_clicked)

    layout = QHBoxLayout()
    layout.addWidget(QLabel("Морфологическая обработка"))
    layout.addWidget(morphological_processing_mask)
    layout.addWidget(dilation_button)
    layout.addWidget(erosion_button)

    return layout
