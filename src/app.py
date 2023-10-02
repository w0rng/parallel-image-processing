from PyQt6.QtWidgets import QApplication, QMainWindow, QRadioButton, QWidget, QHBoxLayout, QPushButton, QVBoxLayout

from algorithms.yuv_convert import row_to_yuv, rgb_to_yuv
from image import Image


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Что-то для обработки картинок")

        self.current_image = Image.load('./assets/example.jpeg')

        self.rgb_button = QRadioButton('RGB')
        self.hls_button = QRadioButton('HLS')
        self.yuv_button = QRadioButton('YUV')

        self.rgb_button.setChecked(True)
        self.rgb_button.clicked.connect(self.rgb_button_clicked)
        self.yuv_button.clicked.connect(self.yuv_button_clicked)

        color_models_layout = QHBoxLayout()
        color_models_layout.addWidget(self.rgb_button)
        color_models_layout.addWidget(self.hls_button)
        color_models_layout.addWidget(self.yuv_button)

        self.show_image_button = QPushButton('Показать картинку')
        self.show_image_button.clicked.connect(self.show_button_clicked)

        layout = QVBoxLayout()
        layout.addLayout(color_models_layout)
        layout.addWidget(self.show_image_button)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def rgb_button_clicked(self):
        self.current_image = Image.load('./assets/example.jpeg')

    def yuv_button_clicked(self):
        image = Image.load("assets/example.jpeg")
        image = Image(rgb_to_yuv(image.pixels))
        self.current_image = image

    def show_button_clicked(self):
        self.current_image.show()


if __name__ == '__main__':
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
