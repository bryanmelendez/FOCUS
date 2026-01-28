from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, Signal

class PomodoroView(QWidget):

    toggle_clicked = Signal()
    end_clicked = Signal()
    mode_changed = Signal(str)
    home_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        top_bar = QHBoxLayout()

        self.home_button = QPushButton("Home")
        self.home_button.setFixedSize(80, 40)

        top_bar.addWidget(self.home_button)
        top_bar.addStretch()  # pushes button to the left

        layout.addLayout(top_bar)

        self.title_label = QLabel("Pomodoro Timer")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        layout.addWidget(self.title_label)

        mode_layout = QHBoxLayout()

        self.work_button = QPushButton("Work")
        self.work_button.setFixedSize(200, 60)
        mode_layout.addWidget(self.work_button)

        #short break button
        self.short_button = QPushButton("Short Break")
        self.short_button.setFixedSize(200, 60)
        mode_layout.addWidget(self.short_button)

        #long break button
        self.long_button = QPushButton("Long Break")
        self.long_button.setFixedSize(200, 60)
        mode_layout.addWidget(self.long_button)

        layout.addLayout(mode_layout)

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

        self.end_button = QPushButton("End Session")
        self.end_button.setFixedSize(200, 60)
        layout.addWidget(self.end_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        self.toggle_button.clicked.connect(lambda: self.toggle_clicked.emit())
        self.work_button.clicked.connect(lambda: self.mode_changed.emit("work"))
        self.short_button.clicked.connect(lambda:self.mode_changed.emit("s_break"))
        self.long_button.clicked.connect(lambda: self.mode_changed.emit("l_break"))
        self.end_button.clicked.connect(lambda: self.end_clicked.emit())
        self.home_button.clicked.connect(self.home_clicked)

    def set_running(self, running: bool):
        if running:
            self.toggle_button.setText("Pause")
        else:
            self.toggle_button.setText("Start")
            
    def update_time(self, seconds):
        minutes = seconds // 60
        secs = seconds % 60
        self.timer_label.setText(f"{minutes:02d}:{secs:02d}")

    def toggle_mode(self):
        if self.mode == "work":
            self.mode = "break"
            self.title_label.setText("Break Time")

    def home_clicked(self):
        self.home_clicked.emit()
