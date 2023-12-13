from PyQt6.QtWidgets import *
from src.algorithms.hough_detection import hough_line_transform


def make_layout(window) -> QBoxLayout:
    search_target = QLineEdit()
    search_target.setPlaceholderText('Объект поиска (line/circle)')
    search_button = QPushButton("Найти")

    def search_button_clicked():
        hough_line_transform(window.current_image)
        # image = harris_corner_detector(window.current_image)
        # image.show()
        return

    search_button.clicked.connect(search_button_clicked)

    layout = QHBoxLayout()
    layout.addWidget(QLabel('Hough detection'))
    layout.addWidget(search_target)
    layout.addWidget(search_button)

    return layout
