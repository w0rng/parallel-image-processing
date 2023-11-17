from PyQt6.QtWidgets import *

from src.laba3.binarization.local_binarization import local_binarization


def make_layout(window):
    binarization_block_size = QLineEdit()
    binarization_block_size.setPlaceholderText('Размер блока для расчета локального порога')

    local_binarization_button = QPushButton('Локальная')

    def button_clicked():
        block_size = int(binarization_block_size.text())
        image = local_binarization(window.current_image, block_size)
        image.show()

    local_binarization_button.clicked.connect(button_clicked)

    layout = QHBoxLayout()
    layout.addWidget(QLabel("Бинаризация (лок.)"))
    layout.addWidget(binarization_block_size)
    layout.addWidget(local_binarization_button)

    return layout
