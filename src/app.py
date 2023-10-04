from PyQt6.QtWidgets import QApplication, QMainWindow, QRadioButton, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, \
    QBoxLayout, QLabel, QCheckBox

from algorithms.yuv_convert import row_to_yuv, rgb_to_yuv
from image import Image

from algorithms.show_color_channel import matrix_pixel_color
from algorithms.histogram import show_histogram


class MainWindow(QMainWindow):
    current_image: Image

    task2_chan1: QCheckBox
    task2_chan2: QCheckBox
    task2_chan3: QCheckBox

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Что-то для обработки картинок")

        self.current_image = Image.load('./assets/example.jpeg')

        layout = QVBoxLayout()
        layout.addLayout(self._make_task1_layout())
        layout.addLayout(self._make_task2_layout())
        layout.addLayout(self._make_task3_layout())

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    # -- task 1
    def _make_task1_layout(self) -> QBoxLayout:
        """преобразование одной цветовой модели в другую (RGB, HLS или HSV, YUV[YCbCr])"""
        rgb_button = QRadioButton('RGB')
        hls_button = QRadioButton('HLS')
        yuv_button = QRadioButton('YUV')

        rgb_button.setChecked(True)
        rgb_button.clicked.connect(self.rgb_button_clicked)
        yuv_button.clicked.connect(self.yuv_button_clicked)

        color_models_layout = QHBoxLayout()
        color_models_layout.addWidget(QLabel("Задание 1"))
        color_models_layout.addWidget(rgb_button)
        color_models_layout.addWidget(hls_button)
        color_models_layout.addWidget(yuv_button)
        color_models_layout.addWidget(self._make_show_image_button(self.show_button_clicked))

        return color_models_layout

    def _make_show_image_button(self, action) -> QPushButton:
        show_image_button = QPushButton('Показать картинку')
        show_image_button.clicked.connect(action)
        return show_image_button

    def rgb_button_clicked(self):
        self.current_image = Image.load('./assets/example.jpeg')

    def yuv_button_clicked(self):
        image = Image.load("assets/example.jpeg")
        image = Image(rgb_to_yuv(image.pixels))
        self.current_image = image

    def show_button_clicked(self):
        self.current_image.show()

    # -- task 2
    def _make_task2_layout(self) -> QBoxLayout:
        """разложение представления изображения в выбранной цветовой модели
        на отдельные каналы с возможностью визуализации выбранного канала для заданной
        цветовой модели"""
        self.task2_chan1 = QCheckBox("chan1")
        self.task2_chan2 = QCheckBox("chan2")
        self.task2_chan3 = QCheckBox("chan3")

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Задание 2"))
        layout.addWidget(self.task2_chan1)
        layout.addWidget(self.task2_chan2)
        layout.addWidget(self.task2_chan3)
        layout.addWidget(self._make_show_image_button(self.show_task2_button_clicked))

        return layout

    def show_task2_button_clicked(self):
        chans: list[int] = []
        if self.task2_chan1.isChecked():
            chans.append(0)
        if self.task2_chan2.isChecked():
            chans.append(1)
        if self.task2_chan3.isChecked():
            chans.append(2)

        new_pixels = matrix_pixel_color(self.current_image.pixels, chans)
        Image(new_pixels).show()

    # -- task 3
    def _make_task3_layout(self) -> QBoxLayout:
        """построение гистограммы для выбранного канала заданной цветовой модели"""
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Задание 3"))
        layout.addWidget(self._make_show_image_button(self.show_task3_button_clicked))

        return layout

    def show_task3_button_clicked(self):
        show_histogram(self.current_image)


if __name__ == '__main__':
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
