import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QRadioButton, QWidget, QHBoxLayout, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Что-то для обработки картинок")

        self.image = QPixmap("./assets/example.jpeg")

        self.label = QLabel('Картинка')
        self.label.setPixmap(self.image)

        self.rgb_button = QRadioButton('RGB')
        self.hls_button = QRadioButton('HLS')
        self.yuv_button = QRadioButton('YCbCr')
        self.rgb_button.setChecked(True)

        color_radio_buttons = QHBoxLayout()
        color_radio_buttons.addWidget(self.rgb_button)
        color_radio_buttons.addWidget(self.hls_button)
        color_radio_buttons.addWidget(self.yuv_button)

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(color_radio_buttons)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
