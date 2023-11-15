from PyQt6.QtWidgets import *
from image import Image
import json

from src.laba3.contours.roberts import roberts_method
from src.laba3.contours.sobel import sobel_method
from src.laba3.contours.laplace import laplace_method

from src.laba3.binarization.global_binarization import global_binarization
from src.laba3.binarization.local_binarization import local_binarization

class MainWindow(QMainWindow):
    current_image: Image

    contours_threshold_value: QLineEdit
    contours_gain_factor: QLineEdit
    contours_balancing_factor: QLineEdit
    contours_laplace_kernel: QLineEdit

    binarization_threshold_value: QLineEdit
    binarization_block_size: QLineEdit

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Что-то для обработки картинок")

        self.start_image = self.current_image = Image.load("../assets/example.jpeg")

        layout = QVBoxLayout()
        layout.addLayout(self._make_color_models_layout())
        layout.addLayout(self._make_contours_layout())
        layout.addLayout(self._make_binarization_layout())

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def _make_color_models_layout(self) -> QBoxLayout:
        """преобразование одной цветовой модели в другую (RGB, HLS или HSV, YUV[YCbCr])"""
        rgb_button = QRadioButton("RGB")
        grayscale_button = QRadioButton("Grayscale")

        rgb_button.setChecked(True)
        rgb_button.clicked.connect(self.rgb_button_clicked)
        grayscale_button.clicked.connect(self.grayscale_button_clicked)

        color_models_layout = QHBoxLayout()
        color_models_layout.addWidget(QLabel("Выбор"))
        color_models_layout.addWidget(rgb_button)
        color_models_layout.addWidget(grayscale_button)
        color_models_layout.addWidget(
            self._make_show_image_button(self.show_button_clicked)
        )

        return color_models_layout

    def _make_show_image_button(
            self, action, title: str = "Показать картинку"
    ) -> QPushButton:
        show_image_button = QPushButton(title)
        show_image_button.clicked.connect(action)
        return show_image_button

    def rgb_button_clicked(self):
        self.start_image = self.current_image = Image.load("../assets/example.jpeg")

    def grayscale_button_clicked(self):
        image = Image.load("../assets/example.jpeg")
        self.start_image = self.current_image = image.to_grayscale()

    def show_button_clicked(self):
        self.current_image.show()

    # -- task 1
    def _make_contours_layout(self):
        self.contours_threshold_value = QLineEdit()
        self.contours_threshold_value.setPlaceholderText("Пороговое значение")

        self.contours_gain_factor = QLineEdit()
        self.contours_gain_factor.setPlaceholderText("Коэффициент усиления")

        self.contours_balancing_factor = QLineEdit()
        self.contours_balancing_factor.setPlaceholderText("Коэффициент балансировки (для Собела)")

        self.contours_laplace_kernel = QLineEdit()
        self.contours_laplace_kernel.setPlaceholderText('Матрица коэффициентов (для Лапласа)')

        roberts_method_button = QPushButton('Метод Робертса')
        sobel_method_button = QPushButton('Метод Собела')
        laplace_method_button = QPushButton('Метод Лапласа')

        roberts_method_button.clicked.connect(self._roberts_method_button_clicked)
        sobel_method_button.clicked.connect(self._sobel_method_button_clicked)
        laplace_method_button.clicked.connect(self._laplace_method_button_clicked)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Законтурить"))
        layout.addWidget(self.contours_threshold_value)
        layout.addWidget(self.contours_gain_factor)
        layout.addWidget(self.contours_balancing_factor)
        layout.addWidget(self.contours_laplace_kernel)
        layout.addWidget(roberts_method_button)
        layout.addWidget(sobel_method_button)
        layout.addWidget(laplace_method_button)

        return layout

    def _roberts_method_button_clicked(self):
        threshold = float(self.contours_threshold_value.text())
        gain_factor = float(self.contours_gain_factor.text())
        image = roberts_method(self.current_image, threshold, gain_factor)
        image.show()

    def _sobel_method_button_clicked(self):
        threshold = float(self.contours_threshold_value.text())
        gain_factor = float(self.contours_gain_factor.text())
        balancing_factor = float(self.contours_balancing_factor.text())
        image = sobel_method(self.current_image, threshold, gain_factor, balancing_factor)
        image.show()

    def _laplace_method_button_clicked(self):
        threshold = float(self.contours_threshold_value.text())
        gain_factor = float(self.contours_gain_factor.text())
        laplace_kernel = json.loads(self.contours_laplace_kernel.text())
        image = laplace_method(self.current_image, threshold, gain_factor, laplace_kernel)
        image.show()

    # -- task 2
    def _make_binarization_layout(self):
        self.binarization_threshold_value = QLineEdit()
        self.binarization_threshold_value.setPlaceholderText('Пороговое значение (глоб.)')

        self.binarization_block_size = QLineEdit()
        self.binarization_block_size.setPlaceholderText('Размер блока для расчета локального порога')

        global_binarization_button = QPushButton('Глобальная')
        local_binarization_button = QPushButton('Локальная')

        global_binarization_button.clicked.connect(self._global_binarization_clicked)
        local_binarization_button.clicked.connect(self._local_binarization_clicked)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Бинаризация"))
        layout.addWidget(self.binarization_threshold_value)
        layout.addWidget(self.binarization_block_size)
        layout.addWidget(global_binarization_button)
        layout.addWidget(local_binarization_button)

        return layout

    def _global_binarization_clicked(self):
        threshold = int(self.binarization_threshold_value.text())
        image = global_binarization(self.current_image, threshold)
        image.show()

    def _local_binarization_clicked(self):
        block_size = int(self.binarization_block_size.text())
        image = local_binarization(self.current_image, block_size)
        image.show()


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
