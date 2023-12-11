from PyQt6.QtWidgets import *

from src.algorithms.threshold_segmentation import threshold_segmentation


def make_layout(window):
    button = QPushButton('Сегментировать')

    def button_clicked():
        image = threshold_segmentation(window.current_image)
        image.show()

    button.clicked.connect(button_clicked)

    layout = QHBoxLayout()
    layout.addWidget(QLabel("Адаптивная пороговая сегментация"))
    layout.addWidget(button)

    return layout
