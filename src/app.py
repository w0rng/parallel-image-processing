from PyQt6.QtWidgets import *

from image import Image


class MainWindow(QMainWindow):
    current_image: Image

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Что-то для обработки картинок")

        self.start_image = self.current_image = Image.load("../assets/example.jpeg")

        layout = QVBoxLayout()

        layout.addLayout(self._make_color_models_layout())

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


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
