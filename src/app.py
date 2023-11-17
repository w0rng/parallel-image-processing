from PyQt6.QtWidgets import *
from image import Image
import json

from src.laba3.contours.roberts import roberts_method
from src.laba3.contours.sobel import sobel_method
from src.laba3.contours.laplace import laplace_method

from src.laba3.binarization.global_binarization import global_binarization
from src.laba3.binarization.local_binarization import local_binarization

from laba3.morphological_processing import dilation, erosion

class MainWindow(QMainWindow):
    current_image: Image

    contours_threshold_value: QLineEdit
    contours_gain_factor: QLineEdit
    contours_balancing_factor: QLineEdit
    contours_laplace_kernel: QLineEdit
    contours_save_result: QCheckBox

    binarization_threshold_value: QLineEdit
    binarization_block_size: QLineEdit


    def __init__(self):
        super().__init__()
        self.setWindowTitle("Что-то для обработки картинок")

        self.start_image = self.current_image = Image.load("../assets/example.jpeg")

        layout = QVBoxLayout()
        layout.addLayout(self._make_color_models_layout())
        layout.addLayout(self._make_contours_layout())
        layout.addLayout(self._make_global_binarization_layout())
        layout.addLayout(self._make_local_binarization_layout())
        layout.addLayout(self._make_morphological_processing_layout())

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

        self.contours_save_result = QCheckBox('Сохранить')

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
        layout.addWidget(self.contours_save_result)
        layout.addWidget(roberts_method_button)
        layout.addWidget(sobel_method_button)
        layout.addWidget(laplace_method_button)

        return layout

    def _roberts_method_button_clicked(self):
        threshold = float(self.contours_threshold_value.text())
        gain_factor = float(self.contours_gain_factor.text())
        need_to_save = self.contours_save_result.isChecked()
        image = roberts_method(self.current_image, threshold, gain_factor)
        if need_to_save:
            self.current_image = image
        image.show()

    def _sobel_method_button_clicked(self):
        threshold = float(self.contours_threshold_value.text())
        gain_factor = float(self.contours_gain_factor.text())
        balancing_factor = float(self.contours_balancing_factor.text())
        need_to_save = self.contours_save_result.isChecked()
        image = sobel_method(self.current_image, threshold, gain_factor, balancing_factor)
        if need_to_save:
            self.current_image = image
        image.show()

    def _laplace_method_button_clicked(self):
        threshold = float(self.contours_threshold_value.text())
        gain_factor = float(self.contours_gain_factor.text())
        laplace_kernel = json.loads(self.contours_laplace_kernel.text())
        need_to_save = self.contours_save_result.isChecked()
        image = laplace_method(self.current_image, threshold, gain_factor, laplace_kernel)
        if need_to_save:
            self.current_image = image
        image.show()

    # -- task 2
    def _make_global_binarization_layout(self):
        self.binarization_threshold_value = QLineEdit()
        self.binarization_threshold_value.setPlaceholderText('Пороговое значение (глоб.)')

        self.global_binarization_save_result = QCheckBox('Сохранить')

        global_binarization_button = QPushButton('Глобальная')
        global_binarization_button.clicked.connect(self._global_binarization_clicked)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Бинаризация (глоб.)"))
        layout.addWidget(self.binarization_threshold_value)
        layout.addWidget(self.global_binarization_save_result)
        layout.addWidget(global_binarization_button)

        return layout

    def _global_binarization_clicked(self):
        threshold = int(self.binarization_threshold_value.text())
        image = global_binarization(self.current_image, threshold)
        if self.global_binarization_save_result.isChecked():
            self.current_image = image
        image.show()

    def _make_local_binarization_layout(self):
        self.binarization_block_size = QLineEdit()
        self.binarization_block_size.setPlaceholderText('Размер блока для расчета локального порога')

        local_binarization_button = QPushButton('Локальная')
        local_binarization_button.clicked.connect(self._local_binarization_clicked)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Бинаризация (лок.)"))
        layout.addWidget(self.binarization_block_size)
        layout.addWidget(local_binarization_button)

        return layout

    def _local_binarization_clicked(self):
        block_size = int(self.binarization_block_size.text())
        image = local_binarization(self.current_image, block_size)
        image.show()

    def _make_morphological_processing_layout(self):
        self.morphological_processing_mask = QLineEdit()
        self.morphological_processing_mask.setPlaceholderText('Маска. В виде [[0, 1], [1, 0]]')

        dilation_button = QPushButton('Расширение')
        dilation_button.clicked.connect(self._morphological_processing_dilation_clicked)

        erosion_button = QPushButton('Сужение')
        erosion_button.clicked.connect(self._morphological_processing_erosion_clicked)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Морфологическая обработка"))
        layout.addWidget(self.morphological_processing_mask)
        layout.addWidget(dilation_button)
        layout.addWidget(erosion_button)

        return layout

    def _morphological_processing_dilation_clicked(self):
        mask = json.loads(self.morphological_processing_mask.text())
        new_image = dilation(self.current_image, mask)
        new_image.show()

    def _morphological_processing_erosion_clicked(self):
        mask = json.loads(self.morphological_processing_mask.text())
        new_image = erosion(self.current_image, mask)
        new_image.show()


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
