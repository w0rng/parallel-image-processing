from PyQt6.QtWidgets import *

from image import Image
from src.layouts.colors import make_layout as make_layout_colors


class MainWindow(QMainWindow):
    current_image: Image

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Что-то для обработки картинок")

        self.start_image = self.current_image = Image.load("assets/example.jpeg")

        layout = QVBoxLayout()
        layout.addLayout(make_layout_colors(self))

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
