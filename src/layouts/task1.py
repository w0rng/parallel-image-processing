import json

from PyQt6.QtWidgets import *

from src.algorithms.contours.laplace import laplace_method
from src.algorithms.contours.roberts import roberts_method
from src.algorithms.contours.sobel import sobel_method


def roberts_method_layout(window):
    contours_threshold_value = QLineEdit()
    contours_threshold_value.setPlaceholderText("Пороговое значение")
    contours_gain_factor = QLineEdit()
    contours_gain_factor.setPlaceholderText("Коэффициент усиления")
    contours_save_result = QCheckBox('Сохранить')

    roberts_method_button = QPushButton('Законтурить')

    def button_clicked():
        threshold = float(contours_threshold_value.text())
        gain_factor = float(contours_gain_factor.text())
        need_to_save = contours_save_result.isChecked()
        image = roberts_method(window.current_image, threshold, gain_factor)
        if need_to_save:
            window.current_image = image
        image.show()

    roberts_method_button.clicked.connect(button_clicked)

    layout = QHBoxLayout()
    layout.addWidget(QLabel("Метод Робертса"))
    layout.addWidget(contours_threshold_value)
    layout.addWidget(contours_gain_factor)
    layout.addWidget(contours_save_result)
    layout.addWidget(roberts_method_button)

    return layout


def sobel_method_layout(window):
    contours_threshold_value = QLineEdit()
    contours_threshold_value.setPlaceholderText("Пороговое значение")
    contours_gain_factor = QLineEdit()
    contours_gain_factor.setPlaceholderText("Коэффициент усиления")
    contours_balancing_factor = QLineEdit()
    contours_balancing_factor.setPlaceholderText("Коэффициент балансировки")
    contours_save_result = QCheckBox('Сохранить')

    def button_clicked():
        threshold = float(contours_threshold_value.text())
        gain_factor = float(contours_gain_factor.text())
        balancing_factor = float(contours_balancing_factor.text())
        need_to_save = contours_save_result.isChecked()
        image = sobel_method(window.current_image, threshold, gain_factor, balancing_factor)
        if need_to_save:
            window.current_image = image
        image.show()

    sobel_method_button = QPushButton('Законтурить')
    sobel_method_button.clicked.connect(button_clicked)

    layout = QHBoxLayout()
    layout.addWidget(QLabel("Метод Собела"))
    layout.addWidget(contours_threshold_value)
    layout.addWidget(contours_gain_factor)
    layout.addWidget(contours_balancing_factor)
    layout.addWidget(contours_save_result)
    layout.addWidget(sobel_method_button)

    return layout


def laplace_method_layout(window):
    contours_threshold_value = QLineEdit()
    contours_threshold_value.setPlaceholderText("Пороговое значение")
    contours_gain_factor = QLineEdit()
    contours_gain_factor.setPlaceholderText("Коэффициент усиления")
    contours_laplace_kernel = QLineEdit()
    contours_laplace_kernel.setPlaceholderText('Матрица коэффициентов')
    contours_laplace_kernel.setText('[[0, 1, 0], [1, 4, 1], [0, 1, 0]]')
    contours_save_result = QCheckBox('Сохранить')

    def button_clicked():
        threshold = float(contours_threshold_value.text())
        gain_factor = float(contours_gain_factor.text())
        laplace_kernel = json.loads(contours_laplace_kernel.text())
        need_to_save = contours_save_result.isChecked()
        image = laplace_method(window.current_image, threshold, gain_factor, laplace_kernel)
        if need_to_save:
            window.current_image = image
        image.show()

    sobel_method_button = QPushButton('Законтурить')
    sobel_method_button.clicked.connect(button_clicked)

    layout = QHBoxLayout()
    layout.addWidget(QLabel("Метод Лапласа"))
    layout.addWidget(contours_threshold_value)
    layout.addWidget(contours_gain_factor)
    layout.addWidget(contours_laplace_kernel)
    layout.addWidget(contours_save_result)
    layout.addWidget(sobel_method_button)

    return layout


def make_layout(window):
    layout = QVBoxLayout()
    layout.addLayout(roberts_method_layout(window))
    layout.addLayout(sobel_method_layout(window))
    layout.addLayout(laplace_method_layout(window))

    return layout
