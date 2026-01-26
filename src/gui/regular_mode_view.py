from model.regular_mode_model import RegularModeModel
from controller.regular_mode_controller import RegularModeController

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt

class RegularTimerView(QWidget):
    def __init__(self):
        super().__init__()

        self.model = RegularModeModel()
        self.controller = RegularModeController()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Super Duper Regular Timer View")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

        # Start button
        self.start_button = QPushButton("Start")
        self.start_button.setFixedSize(200, 60)
        self.start_button.clicked.connect(self.controller.start_regular_mode) # connect it to the controller
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        # Stop button
        self.start_button = QPushButton("Stop")
        self.start_button.setFixedSize(200, 60)
        self.start_button.clicked.connect(self.controller.stop_regular_mode) # connect it to the controller
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)