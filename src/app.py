from PyQt6.QtWidgets import *

from image import Image
from src.layouts.colors import make_layout as make_layout_colors
from src.layouts.global_binarization import make_layout as make_layout_global_binarization
from src.layouts.local_binarization import make_layout as make_layout_local_binarization
from src.layouts.morphological_processing import make_layout as make_layout_morphological_processing
from src.layouts.task1 import make_layout as make_layout_task1


class MainWindow(QMainWindow):
    current_image: Image

    contours_threshold_value: QLineEdit
    contours_gain_factor: QLineEdit
    contours_balancing_factor: QLineEdit
    contours_laplace_kernel: QLineEdit
    contours_save_result: QCheckBox

    binarization_threshold_value: QLineEdit
    binarization_block_size: QLineEdit

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Что-то для обработки картинок")

        self.start_image = self.current_image = Image.load("assets/example.jpeg")

        layout = QVBoxLayout()
        layout.addLayout(make_layout_colors(self))
        layout.addLayout(make_layout_task1(self))
        layout.addLayout(make_layout_global_binarization(self))
        layout.addLayout(make_layout_local_binarization(self))
        layout.addLayout(make_layout_morphological_processing(self))

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
