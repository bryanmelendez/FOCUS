from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class PomodoroView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Pomodoro Timer")
        layout.addWidget(label)
        self.setLayout(layout)