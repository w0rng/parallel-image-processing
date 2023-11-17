from PyQt6.QtWidgets import *

from src.image import Image


def make_layout(window) -> QBoxLayout:
    """преобразование одной цветовой модели в другую (RGB, HLS или HSV, YUV[YCbCr])"""
    rgb_button = QRadioButton("RGB")
    grayscale_button = QRadioButton("Grayscale")

    rgb_button.setChecked(True)

    def rgb_button_clicked():
        window.start_image = window.current_image = Image.load("assets/example.jpeg")

    rgb_button.clicked.connect(rgb_button_clicked)

    def grayscale_button_clicked():
        image = Image.load("assets/example.jpeg")
        window.start_image = window.current_image = image.to_grayscale()

    grayscale_button.clicked.connect(grayscale_button_clicked)

    show_image_button = QPushButton("Показать картинку")
    show_image_button.clicked.connect(lambda: window.current_image.show())

    color_models_layout = QHBoxLayout()
    color_models_layout.addWidget(QLabel("Выбор"))
    color_models_layout.addWidget(rgb_button)
    color_models_layout.addWidget(grayscale_button)

    color_models_layout.addWidget(show_image_button)

    return color_models_layout
