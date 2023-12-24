from PyQt6.QtWidgets import *

from image import Image
from src.layouts.colors import make_layout as make_layout_colors
from src.layouts.texture_map import make_layout as make_layout_texture_map
from src.layouts.histogram import make_layout as make_layout_histogram
from src.layouts.corner_detector import make_layout as make_layout_corner_detector
from src.layouts.hough_transform_linear import make_layout as make_hough_transform_linear


class MainWindow(QMainWindow):
    current_image: Image

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Что-то для обработки картинок")

        self.start_image = self.current_image = Image.load("assets/example.jpeg")

        layout = QVBoxLayout()
        layout.addLayout(make_layout_colors(self))
        layout.addLayout(make_layout_texture_map(self))
        layout.addLayout(make_layout_histogram(self))
        layout.addLayout(make_layout_corner_detector(self))
        layout.addLayout(make_hough_transform_linear(self))

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
