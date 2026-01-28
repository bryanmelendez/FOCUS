from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal

class RegularTimerView(QWidget):

    toggle_clicked = Signal()
    end_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_label = QLabel("Regular Session")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        layout.addWidget(self.title_label)

       # Timer label
        self.timer_label = QLabel("25:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet(
            "font-size: 56px; font-weight: bold;"
        )
        layout.addWidget(self.timer_label)

        self.toggle_button = QPushButton("Start")
        self.toggle_button.setFixedSize(200, 60)
        layout.addWidget(self.toggle_button, alignment=Qt.AlignCenter)

        self.stop_button = QPushButton("End Session")
        self.stop_button.setFixedSize(200, 60)
        layout.addWidget(self.stop_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        self.toggle_button.clicked.connect(lambda: self.toggle_clicked.emit())
        self.stop_button.clicked.connect(lambda: self.end_clicked.emit())

    def set_running(self, running: bool):
        if running:
            self.toggle_button.setText("Pause")
        else:
            self.toggle_button.setText("Start")
            
    def update_time(self, seconds):
        minutes = seconds // 60
        secs = seconds % 60
        self.timer_label.setText(f"{minutes:02d}:{secs:02d}")
