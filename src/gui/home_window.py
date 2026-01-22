from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()

        # Welcome label at the top, centered
        self.welcome_label = QLabel("Welcome back uh insert name !")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.welcome_label)

        # Regular mode button
        self.regular_button = QPushButton("Regular Mode")
        self.regular_button.setFixedSize(200, 60)
        layout.addWidget(self.regular_button, alignment=Qt.AlignCenter)

        # Pomodoro button
        self.pomodoro_button = QPushButton("Pomodoro")
        self.pomodoro_button.setFixedSize(200, 60)
        self.pomodoro_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.pomodoro_button, alignment=Qt.AlignCenter)

        # History button
        self.history_button = QPushButton("History")
        self.history_button.setFixedSize(200, 60)
        self.history_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.history_button, alignment=Qt.AlignCenter)

        layout.setSpacing(10)  # space between widgets
        self.setLayout(layout)

