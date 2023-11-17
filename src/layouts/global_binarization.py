from PyQt6.QtWidgets import *

from src.laba3.binarization.global_binarization import global_binarization


def make_layout(window):
    binarization_threshold_value = QLineEdit()
    binarization_threshold_value.setPlaceholderText('Пороговое значение (глоб.)')

    global_binarization_save_result = QCheckBox('Сохранить')

    global_binarization_button = QPushButton('Глобальная')

    def button_clicked():
        threshold = int(binarization_threshold_value.text())
        image = global_binarization(window.current_image, threshold)
        if global_binarization_save_result.isChecked():
            window.current_image = image
        image.show()

    global_binarization_button.clicked.connect(button_clicked)

    layout = QHBoxLayout()
    layout.addWidget(QLabel("Бинаризация (глоб.)"))
    layout.addWidget(binarization_threshold_value)
    layout.addWidget(global_binarization_save_result)
    layout.addWidget(global_binarization_button)

    return layout
