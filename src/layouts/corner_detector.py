from PyQt6.QtWidgets import *

from src.algorithms.corner_detectors import harris_corner_detector, fast_corner_detector


def make_layout(window) -> QBoxLayout:
    harris_button = QPushButton("Харрис")
    fast_button = QPushButton('FAST')

    def harris_button_clicked():
        image = harris_corner_detector(window.current_image)
        image.show()

    harris_button.clicked.connect(harris_button_clicked)

    def fast_button_clicked():
        image = fast_corner_detector(window.current_image)
        image.show()

    fast_button.clicked.connect(fast_button_clicked)

    layout = QHBoxLayout()
    layout.addWidget(QLabel('Corner detector'))
    layout.addWidget(harris_button)
    layout.addWidget(fast_button)

    return layout
