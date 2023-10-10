from PyQt6.QtWidgets import *

from laba2.make_noise.make_noise_multiplicatively import make_noize_multiplicatively
from laba2.make_noise.make_noise_additive import make_noise_additive

from image import Image


class MainWindow(QMainWindow):
    current_image: Image

    task2_chan1: QPushButton
    task2_chan2: QPushButton
    task2_chan3: QPushButton

    task4_slider_brightnes: QSlider
    task4_slider_contrast: QSlider

    taskC_input: QLineEdit

    laba2_make_noise_percent: QSlider
    laba2_make_noise_params_input: QLineEdit
    laba2_button_chan1: QRadioButton
    laba2_button_chan2: QRadioButton
    laba2_button_chan3: QRadioButton

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Что-то для обработки картинок")

        self.current_image = Image.load("../assets/example.jpeg")

        layout = QVBoxLayout()

        layout.addLayout(self._make_task1_layout())

        layout.addLayout(self._make_noise_layout())

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    # -- task 1
    def _make_noise_layout(self) -> QBoxLayout:
        impl_button = QPushButton("Импульсный")
        add_button = QPushButton("Аддитивный")
        mul_button = QPushButton("Мультипликативный")

        self.laba2_make_noise_percent = QSlider()
        self.laba2_make_noise_percent.setRange(0, 100)
        self.laba2_make_noise_percent.setValue(30)

        self.laba2_make_noise_params_input = QLineEdit()
        self.laba2_make_noise_params_input.setPlaceholderText("Параметры")

        self.laba2_button_chan1 = QRadioButton("chan1")
        self.laba2_button_chan2 = QRadioButton("chan2")
        self.laba2_button_chan3 = QRadioButton("chan3")
        self.laba2_button_chan1.setChecked(True)

        button_group = QButtonGroup(parent=self)
        button_group.addButton(self.laba2_button_chan1)
        button_group.addButton(self.laba2_button_chan2)
        button_group.addButton(self.laba2_button_chan3)

        impl_button.clicked.connect(self._make_noise_impulslly)
        add_button.clicked.connect(self._make_noise_additionally)
        mul_button.clicked.connect(self._make_noise_multiplicatively)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Зашумить"))
        layout.addWidget(self.laba2_make_noise_percent)
        layout.addWidget(self.laba2_button_chan1)
        layout.addWidget(self.laba2_button_chan2)
        layout.addWidget(self.laba2_button_chan3)
        layout.addWidget(self.laba2_make_noise_params_input)
        layout.addWidget(impl_button)
        layout.addWidget(add_button)
        layout.addWidget(mul_button)

        return layout

    def _make_noise_impulslly(self):
        percent, chosen_chan, params = self._get_laba2_make_noise_all_params()
        print("kek impuls")

    def _make_noise_additionally(self):
        percent, chosen_chan, params = self._get_laba2_make_noise_all_params()
        self.current_image = make_noise_additive(
            self.current_image,
            percent,
            chosen_chan,
            params[0],
            params[1],
        )

    def _make_noise_multiplicatively(self):
        percent, chosen_chan, params = self._get_laba2_make_noise_all_params()

        # c1_min = 99999
        # c1_max = -99999
        # c2_min = 99999
        # c2_max = -99999
        # c3_min = 99999
        # c3_max = -99999
        # for row in self.current_image.pixels:
        #     for p in row:
        #         if p[0] > c1_max:
        #             c1_max = p[0]
        #         if p[0] < c1_min:
        #             c1_min = p[0]
        #         if p[1] > c2_max:
        #             c2_max = p[1]
        #         if p[1] < c2_min:
        #             c2_min = p[1]
        #         if p[2] > c3_max:
        #             c3_max = p[2]
        #         if p[2] < c3_min:
        #             c3_min = p[2]
        # print(c1_min, c1_max, c2_min, c2_max, c3_min, c3_max)

        self.current_image = make_noize_multiplicatively(
            self.current_image,
            percent,
            chosen_chan,
            params[0],
            params[1],
        )

    def _get_laba2_make_noise_all_params(self) -> tuple[float, int, list[float]]:
        return (
            self._get_laba2_make_noise_percent(),
            self._get_laba2_make_noise_chosen_chan(),
            self._get_laba2_make_noise_params_as_arr()
        )

    def _get_laba2_make_noise_params_as_arr(self) -> list[float]:
        text = self.laba2_make_noise_params_input.text()
        if not text:
            return []
        return [float(num) for num in text.replace(" ", "").split(",")]

    def _get_laba2_make_noise_percent(self) -> float:
        return self.laba2_make_noise_percent.value() / 100

    def _get_laba2_make_noise_chosen_chan(self) -> int:
        chan = 0
        if self.laba2_button_chan1.isChecked():
            chan = 0
        elif self.laba2_button_chan2.isChecked():
            chan = 1
        elif self.laba2_button_chan3.isChecked():
            chan = 2
        return chan

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
        color_models_layout.addWidget(QLabel("Выбор"))
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


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
