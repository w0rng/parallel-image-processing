import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QRadioButton, QWidget, QHBoxLayout, QLabel, QFileDialog, \
    QVBoxLayout, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Что-то для обработки картинок")

        image_picker_layout = QVBoxLayout()
        self.image_path = ''
        self.image_picker_button = QPushButton('Выбрать изображение')
        self.image_picker_button.clicked.connect(self.file_picker_button_clicked)

        self.label = QLabel('Картинка')

        image_picker_layout.addWidget(self.image_picker_button)
        image_picker_layout.addWidget(self.label)

        self.rgb_button = QRadioButton('RGB')
        self.hls_button = QRadioButton('HLS')
        self.yuv_button = QRadioButton('YCbCr')
        self.rgb_button.setChecked(True)


        color_radio_buttons = QHBoxLayout()
        color_radio_buttons.addWidget(self.rgb_button)
        color_radio_buttons.addWidget(self.hls_button)
        color_radio_buttons.addWidget(self.yuv_button)

        layout = QHBoxLayout()
        layout.addLayout(image_picker_layout)
        layout.addLayout(color_radio_buttons)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def file_picker_button_clicked(self):
        self.image_path = QFileDialog.getOpenFileUrl()[0].path()
        self.label.setPixmap(QPixmap)

app = QApplication([])

window = MainWindow()
window.show()

app.exec()
