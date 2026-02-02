from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, Signal

class PomodoroView(QWidget):

    toggle_clicked = Signal()
    end_clicked = Signal()
    mode_changed = Signal(str)
    home_clicked = Signal()
    settings_clicked = Signal()

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

        self.settings_button = QPushButton("Settings")
        self.settings_button.setFixedSize(80, 40)
        top_bar.addWidget(self.settings_button)

        layout.addLayout(top_bar)

        self.title_label = QLabel("Pomodoro Timer")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        layout.addWidget(self.title_label)

        self.mode_label = QLabel("Work")
        self.mode_label.setAlignment(Qt.AlignCenter)
        self.mode_label.setStyleSheet("font-size: 36px; font-weight: bold;")
        layout.addWidget(self.mode_label)

        mode_layout = QHBoxLayout()

        self.work_button = QPushButton("Work")
        self.work_button.setFixedSize(200, 60)
        mode_layout.addWidget(self.work_button)

        #short break button
        self.break_button = QPushButton("Break")
        self.break_button.setFixedSize(200, 60)
        mode_layout.addWidget(self.break_button)

        layout.addLayout(mode_layout)

        timer_layout = QHBoxLayout()

        timer_widget = QWidget()
        timer_layout = QHBoxLayout(timer_widget)
        timer_layout.setContentsMargins(100, 0, 0, 0)
        timer_layout.setSpacing(12)

        # Timer label
        self.timer_label = QLabel("25:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 56px; font-weight: bold;")

        # Skip button
        self.skip_button = QPushButton("Skip")
        self.skip_button.setFixedSize(80, 40)
        self.skip_button.setVisible(False)  

        #Skip spacer
        self.skip_spacer = QSpacerItem(80, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)

        timer_layout.addWidget(self.timer_label)
        timer_layout.addWidget(self.skip_button)
        timer_layout.addItem(self.skip_spacer)

        # Center the *widget* in the parent layout
        layout.addWidget(timer_widget, alignment=Qt.AlignCenter)

        self.toggle_button = QPushButton("Start")
        self.toggle_button.setFixedSize(200, 60)
        layout.addWidget(self.toggle_button, alignment=Qt.AlignCenter)

        self.end_button = QPushButton("End Session")
        self.end_button.setFixedSize(200, 60)
        layout.addWidget(self.end_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        self.toggle_button.clicked.connect(lambda: self.toggle_clicked.emit())
        self.work_button.clicked.connect(lambda: self.mode_changed.emit("work"))
        self.break_button.clicked.connect(lambda:self.mode_changed.emit("break"))
        self.end_button.clicked.connect(lambda: self.end_clicked.emit())
        self.home_button.clicked.connect(self.home_clicked)
        self.settings_button.clicked.connect(lambda: self.settings_clicked.emit())

    def set_running(self, running: bool):
        if running:
            self.toggle_button.setText("Pause")
            self.skip_button.setVisible(True)
            self.skip_spacer.changeSize(0,0)
        else:
            self.toggle_button.setText("Start")
            self.skip_button.setVisible(False)
            self.skip_spacer.changeSize(80,40)
            
    def update_time(self, seconds):
        minutes = seconds // 60
        secs = seconds % 60
        self.timer_label.setText(f"{minutes:02d}:{secs:02d}")

    def set_mode(self, mode: str):
        if mode == "work":
            self.work_button.setChecked(True)
            self.break_button.setChecked(False)
            self.mode_label.setText("Work")
        else:
            self.work_button.setChecked(False)
            self.break_button.setChecked(True)
            self.mode_label.setText("Break")
    def home_clicked(self):
        self.home_clicked.emit()
    
    def update_controls(self, is_running: bool, has_started: bool):
        # Start / Pause button
        if is_running:
            self.toggle_button.setText("Pause")
        else:
            self.toggle_button.setText("Start")

        # Skip button visibility
        self.skip_button.setVisible(has_started)
