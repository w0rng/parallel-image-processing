from PyQt6.QtWidgets import *

from src.algorithms.corner_detectors import harris_corner_detector


def make_layout(window) -> QBoxLayout:
    harris_button = QPushButton("Харрис")

    def harris_button_clicked():
        image = harris_corner_detector(window.current_image)
        image.show()

    harris_button.clicked.connect(harris_button_clicked)

    harris_layout = QHBoxLayout()
    harris_layout.addWidget(harris_button)

    layout = QHBoxLayout()
    layout.addWidget(QLabel('Corner detector'))
    layout.addLayout(harris_layout)

    return layout
