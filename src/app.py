from PyQt6.QtWidgets import *

from laba2.make_noise.make_noise_multiplicatively import make_noize_multiplicatively
from laba2.make_noise.make_noise_additive import make_noise_additive
from laba2.make_noise.make_noise_pulse import make_noise_pulse
from laba2.metrics.calc import calc

from laba2.filters.linear import linear_filter
from laba2.filters.local_histogram_filter import local_histogram_filter
from laba2.filters.average_filter import average_filter_recursive, average_filter
from laba2.filters.medina import median
import time

from image import Image
from laba2.models.kernel import Kernel


class MainWindow(QMainWindow):
    current_image: Image

    laba2_make_noise_percent: QSlider
    laba2_make_noise_params_input: QLineEdit
    laba2_button_chan1: QRadioButton
    laba2_button_chan2: QRadioButton
    laba2_button_chan3: QRadioButton

    laba2_linear_gradient_params: QLineEdit
    laba2_average_filter_params: QLineEdit
    laba2_task_b_params: QLineEdit
    laba2_task_k_params: QLineEdit

    laba2_local_histogram_params: QLineEdit

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Абрамов МПИ22-01")

        self.start_image = self.current_image = Image.load("../assets/example.jpeg")

        layout = QVBoxLayout()

        layout.addLayout(self._make_task1_layout())

        layout.addLayout(self._make_noise_layout())

        layout.addLayout(self._make_task2_layout())

        layout.addLayout(self._make_task3_layout())

        layout.addLayout(self._make_task4_layout())

        layout.addLayout(self._make_taskB_layout())
        layout.addLayout(self._make_taskE_layout())

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    # -- task 1
    def _make_noise_layout(self) -> QBoxLayout:
        impl_button = QPushButton("Импульсный")
        impl_button.setToolTip("Процент черных пикселей")
        add_button = QPushButton("Аддитивный")
        add_button.setToolTip("range_start, range_end")
        mul_button = QPushButton("Мультипликативный")
        mul_button.setToolTip("range_start, range_end")

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
        start_time = time.time()
        self.current_image = make_noise_pulse(
            self.current_image,
            percent,
            chosen_chan,
            params[0],
        )
        end_time = time.time() - start_time
        calc(f"impulse[{percent}, {params[0]}]", end_time, self.start_image, self.current_image)

    def _make_noise_additionally(self):
        percent, chosen_chan, params = self._get_laba2_make_noise_all_params()
        start_time = time.time()
        self.current_image = make_noise_additive(
            self.current_image,
            percent,
            chosen_chan,
            params[0],
            params[1],
        )
        end_time = time.time() - start_time
        calc(f"additive[{percent}, {params[0]}, {params[1]}]", end_time, self.start_image, self.current_image)


    def _make_noise_multiplicatively(self):
        percent, chosen_chan, params = self._get_laba2_make_noise_all_params()
        start_time = time.time()
        self.current_image = make_noize_multiplicatively(
            self.current_image,
            percent,
            chosen_chan,
            params[0],
            params[1],
        )
        end_time = time.time() - start_time
        calc(f"multiplicatively[{percent}, {params[0]}, {params[1]}]", end_time, self.start_image, self.current_image)


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

    # -- task 2
    def _make_task2_layout(self):
        layout = QHBoxLayout()

        label = QLabel('Задание 2')

        self.laba2_linear_gradient_params = QLineEdit()
        self.laba2_linear_gradient_params.setPlaceholderText("Высота, ширина, коэфф-ты ядра")

        linear_button = QPushButton('Линейный фильтр')
        linear_button.clicked.connect(self.linear_button_clicked)

        layout.addWidget(label)
        layout.addWidget(self.laba2_linear_gradient_params)
        layout.addWidget(linear_button)

        return layout

    def linear_button_clicked(self):
        [height, width, coef] = self._get_laba2_linear_filter_params_as_arr()
        start = time.time()
        image = linear_filter(self.current_image, Kernel(height, width, coef))
        end_time = time.time() - start
        calc(f"linear[{height}x{width}x{coef}]", end_time, self.start_image, image)
        image.show()

    def _get_laba2_linear_filter_params_as_arr(self) -> list[float]:
        text = self.laba2_linear_gradient_params.text()
        if not text:
            return []
        return [int(num) for num in text.replace(" ", "").split(",")]

    # -- task 3
    def _make_task3_layout(self):
        layout = QHBoxLayout()

        label = QLabel('Задание 3')

        self.laba2_average_filter_params = QLineEdit()
        self.laba2_average_filter_params.setPlaceholderText("radius_x, radius_y маски")

        average_filter_button = QPushButton('Среднеарифметический фильтра (рекурс.)')
        average_filter_button.clicked.connect(self.average_filter_button_clicked)

        layout.addWidget(label)
        layout.addWidget(self.laba2_average_filter_params)
        layout.addWidget(average_filter_button)

        return layout

    def _get_laba2_average_filter_params_as_arr(self) -> list[float]:
        text = self.laba2_average_filter_params.text()
        if not text:
            return []
        return [int(num) for num in text.replace(" ", "").split(",")]

    def average_filter_button_clicked(self):
        [radius_x, radius_y] = self._get_laba2_average_filter_params_as_arr()
        start = time.time()
        image = average_filter_recursive(self.current_image, radius_x, radius_y)
        end_time = time.time() - start
        calc(f"average_recursive[{radius_x}x{radius_y}]", end_time, self.start_image, image)
        image.show()

    # -- task b
    def _make_taskB_layout(self):
        layout = QHBoxLayout()

        label = QLabel('Задание B')

        self.laba2_task_b_params = QLineEdit()
        self.laba2_task_b_params.setPlaceholderText("Ширина, Высота окна")

        task_b_button = QPushButton('Лин. усредняющий (сред. арифметическое)')
        task_b_button.clicked.connect(self.task_b_button_clicked)

        layout.addWidget(label)
        layout.addWidget(self.laba2_task_b_params)
        layout.addWidget(task_b_button)

        return layout

    # -- task E
    def _make_taskE_layout(self):
        layout = QHBoxLayout()

        label = QLabel('Задание B')

        self.laba2_task_b_params = QLineEdit()
        self.laba2_task_b_params.setPlaceholderText("Ширина, Высота окна")

        task_b_button = QPushButton('Медианный фильтр')
        task_b_button.clicked.connect(self.task_e_button_clicked)

        layout.addWidget(label)
        layout.addWidget(self.laba2_task_b_params)
        layout.addWidget(task_b_button)

        return layout

    def _get_laba2_task_b_params_as_arr(self) -> list[float]:
        text = self.laba2_task_b_params.text()
        if not text:
            return []
        return [int(num) for num in text.replace(" ", "").split(",")]

    def task_b_button_clicked(self):
        [radius_x, radius_y] = self._get_laba2_task_b_params_as_arr()
        start = time.time()
        image = average_filter(self.current_image, radius_x, radius_y)
        end_time = time.time() - start
        calc(f"average[{radius_x}x{radius_y}]", end_time, self.start_image, image)
        image.show()


    def task_e_button_clicked(self):
        [radius_x, radius_y] = self._get_laba2_task_b_params_as_arr()
        start = time.time()
        image = median(self.current_image, radius_x, radius_y)
        end_time = time.time() - start
        calc(f"average[{radius_x}x{radius_y}]", end_time, self.start_image, image)
        image.show()

    def _get_laba2_task_k_params_as_arr(self) -> list[float]:
        text = self.laba2_task_k_params.text()
        if not text:
            return []
        return [int(num) for num in text.replace(" ", "").split(",")]

    # -- task 4
    def _make_task4_layout(self):
        layout = QHBoxLayout()

        label = QLabel('Задание 4')

        self.laba2_local_histogram_params = QLineEdit()
        self.laba2_local_histogram_params.setPlaceholderText("размер окна")

        button = QPushButton('Медианный фильтр (лок. гистограмма)')
        button.clicked.connect(self._local_histogram_filter_clicked)

        layout.addWidget(label)
        layout.addWidget(self.laba2_local_histogram_params)
        layout.addWidget(button)

        return layout

    def _local_histogram_filter_clicked(self):
        window_size = int(self.laba2_local_histogram_params.text())
        start = time.time()
        new_image = local_histogram_filter(self.current_image, window_size)
        end_time = time.time() - start
        calc(f"local_histogram_filter[{window_size}]", end_time, self.start_image, new_image)
        new_image.show()

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
        self.start_image = self.current_image = Image.load("../assets/example.jpeg")

    def yuv_button_clicked(self):
        image = Image.load("../assets/example.jpeg")
        self.start_image = self.current_image = image.to_yuv()

    def hls_button_clicked(self):
        image = Image.load("../assets/example.jpeg")
        self.start_image = self.current_image = image.to_hls()


    def show_button_clicked(self):
        self.current_image.show()


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
