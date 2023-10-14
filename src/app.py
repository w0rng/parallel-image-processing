from PyQt6.QtWidgets import *

from algorithms.autolevels import rgb_autolevels
from algorithms.equalization import equalization
from algorithms.grey_world import grey_world_correction
from algorithms.histogram import show_histogram
from algorithms.piecewise_linear_histogram_correction import (
    hls_piecewise_linear_histogram_correction, parse_points_string,
    rgb_piecewise_linear_histogram_correction)
from algorithms.sedate import sedate
from image import Image


class MainWindow(QMainWindow):
    current_image: Image

    task2_chan1: QPushButton
    task2_chan2: QPushButton
    task2_chan3: QPushButton

    task4_slider_brightnes: QSlider
    task4_slider_contrast: QSlider

    taskC_input: QLineEdit

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Абрамов МПИ22-01")

        self.current_image = Image.load("../assets/example.jpeg")

        layout = QVBoxLayout()
        layout.addLayout(self._make_task1_layout())
        layout.addLayout(self._make_task2_layout())
        layout.addLayout(self._make_task3_layout())
        layout.addLayout(self._make_task4_layout())

        layout.addLayout(self._make_taksB_layout())
        layout.addLayout(self._make_taksE_layout())
        # layout.addLayout(self._make_task_k_layout())

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    # -- task 1
    def _make_task1_layout(self) -> QBoxLayout:
        """преобразование одной цветовой модели в другую (RGB, HLS или HSV, YUV[YCbCr])"""
        rgb_button = QRadioButton("RGB")
        hls_button = QRadioButton("HLS")
        yuv_button = QRadioButton("YUV")

        rgb_button.setChecked(True)
        rgb_button.clicked.connect(self.rgb_button_clicked)
        hls_button.clicked.connect(self.hls_button_clicked)
        yuv_button.clicked.connect(self.yuv_button_clicked)

        color_models_layout = QHBoxLayout()
        color_models_layout.addWidget(QLabel("Задание 1"))
        color_models_layout.addWidget(rgb_button)
        color_models_layout.addWidget(hls_button)
        color_models_layout.addWidget(yuv_button)
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
        self.current_image = Image.load("../assets/example.jpeg")

    def yuv_button_clicked(self):
        image = Image.load("../assets/example.jpeg")
        self.current_image = image.to_yuv()

    def hls_button_clicked(self):
        image = Image.load("../assets/example.jpeg")
        self.current_image = image.to_hls()

    def show_button_clicked(self):
        self.current_image.show()

    # -- task 2
    def _make_task2_layout(self) -> QBoxLayout:
        """разложение представления изображения в выбранной цветовой модели
        на отдельные каналы с возможностью визуализации выбранного канала для заданной
        цветовой модели"""
        self.task2_chan1 = QPushButton("chan1")
        self.task2_chan2 = QPushButton("chan2")
        self.task2_chan3 = QPushButton("chan3")

        self.task2_chan1.clicked.connect(self.task_2_channel_1_clicked)
        self.task2_chan2.clicked.connect(self.task_2_channel_2_clicked)
        self.task2_chan3.clicked.connect(self.task_2_channel_3_clicked)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Задание 2"))
        layout.addWidget(self.task2_chan1)
        layout.addWidget(self.task2_chan2)
        layout.addWidget(self.task2_chan3)

        return layout

    def task_2_channel_1_clicked(self):
        image = self.current_image.show_channel(0)
        image.show(convert_to_rgb=True)

    def task_2_channel_2_clicked(self):
        image = self.current_image.show_channel(1)
        image.show(convert_to_rgb=True)

    def task_2_channel_3_clicked(self):
        image = self.current_image.show_channel(2)
        image.show(convert_to_rgb=True)

    # -- task 3
    def _make_task3_layout(self) -> QBoxLayout:
        """построение гистограммы для выбранного канала заданной цветовой модели"""
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Задание 3"))
        layout.addWidget(
            self._make_show_image_button(
                self.show_task3_button_clicked, "Показать гистограмму"
            )
        )

        return layout

    def show_task3_button_clicked(self):
        show_histogram(self.current_image)

    # -- task 4
    def _make_task4_layout(self) -> QBoxLayout:
        """построение гистограммы для выбранного канала заданной цветовой модели"""
        self.task4_slider_brightnes = QSlider()
        self.task4_slider_contrast = QSlider()
        self.task4_slider_brightnes.setRange(-100, 100)
        self.task4_slider_contrast.setRange(0, 100)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Задание 4"))
        layout.addWidget(QLabel("Яркость"))
        layout.addWidget(self.task4_slider_brightnes)
        layout.addWidget(QLabel("Контраст"))
        layout.addWidget(self.task4_slider_contrast)
        layout.addWidget(self._make_show_image_button(self.show_task4_button_clicked))

        return layout

    def show_task4_button_clicked(self):
        brightnes = self.task4_slider_brightnes.value()
        contrast = self.task4_slider_contrast.value() / 50
        image = self.current_image.change_yuv_brightnes_and_contrast(
            brightnes, contrast
        )
        image.show(convert_to_rgb=True)

    def _make_taskC_layout(self) -> QBoxLayout:
        self.taskC_input = QLineEdit()
        self.taskC_input.setText("(100,150) (200,250)")
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Задание C"))
        layout.addWidget(self.taskC_input)
        layout.addWidget(
            self._make_show_image_button(self.show_taskC_button_clicked, "Коррекция")
        )
        return layout

    def show_taskC_button_clicked(self):
        correcting_points = parse_points_string(self.taskC_input.text())
        print(correcting_points)
        if self.current_image.mode == "rgb":
            rgb_piecewise_linear_histogram_correction(
                self.current_image, correcting_points
            )
        elif self.current_image.mode == "hls":
            hls_piecewise_linear_histogram_correction(
                self.current_image, correcting_points
            )

    # -- task J
    def _make_taskJ_layout(self) -> QBoxLayout:
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Задание J"))
        layout.addWidget(
            self._make_show_image_button(self.show_taskJ_button_clicked, "«Autolevels»")
        )

    def _make_taksB_layout(self) -> QBoxLayout:
        def tmp():
            self.current_image = equalization(self.current_image)
            self.current_image.show()

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Индивидуальное задание 1"))
        layout.addWidget(self._make_show_image_button(tmp, "Нормализация гистограммы"))
        return layout

    def _make_taksE_layout(self) -> QBoxLayout:
        slider = QSlider()

        def tmp():
            gamma = (slider.value() + 1) / 20
            sedate(self.current_image, gamma).show()

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Индивидуальное задание 2"))
        layout.addWidget(slider)
        layout.addWidget(self._make_show_image_button(tmp, "Степенная коррекция"))
        return layout

    def show_taskJ_button_clicked(self):
        image = self.current_image
        image = rgb_autolevels(image)
        image.show()

    # -- task K
    def _make_task_k_layout(self) -> QBoxLayout:
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Задание K"))
        layout.addWidget(
            self._make_show_image_button(self.show_task_k_button_clicked, "«Серый мир»")
        )
        return layout

    def show_task_k_button_clicked(self):
        image = self.current_image
        image = grey_world_correction(image)
        image.show()


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
