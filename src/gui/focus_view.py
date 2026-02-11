from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QIcon

class FocusView(QWidget):

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

        text_font = QFont("Menlo")
        timer_font = QFont("Courier New")

        end_button_style = """
        QPushButton {
            background-color: #f66e60;
            color: #eee6e2;
            font-weight: 600;
            border-radius: 16px;
            border: none;
        }

        QPushButton:hover {
            background-color: #da5e55;
        }

        QPushButton:pressed {
            background-color: #a84a44;
        }
        """

        toggle_button_style = """
        QPushButton {
            background-color: #47ac96;   /* Start */
            color: #eee6e2;
            font-weight: 600;
            border-radius: 16px;
            border: none;
            padding: 10px 18px;
        }

        QPushButton:hover {
            background-color: #3aa18c;
        }

        QPushButton:pressed {
            background-color: #2f8f7a;
        }

        /* PAUSED STATE */
        QPushButton:checked {
            background-color: #f3b14d;   /* Amber = paused */
            color: #1E293B;
        }

        QPushButton:checked:hover {
            background-color: #da9630;
        }

        QPushButton:checked:pressed {
            background-color: #c78420;
        }
        """

        work_button_style = """
        QPushButton {
            background-color: #434343;
            color: #eee6e2;
            font-weight: 600;
            border-radius: 16px;
            border: none;
            padding: 10px 18px;
        }

        QPushButton:hover {
            background-color: #bd7070;
        }

        QPushButton:pressed {
            background-color: #8b5151;
        }

        /* SELECTED STATE */
        QPushButton:checked {
            background-color: #e28686;   /* Amber = paused */
            color: #1E293B;
        }

        QPushButton:checked:hover {
            background-color: #e28686;
        }

        QPushButton:checked:pressed {
            background-color: #e28686;
        }
        """

        top_bar = QHBoxLayout()

        self.logo_button = QPushButton()
        self.logo_button.setCursor(Qt.PointingHandCursor)

        pixmap = QPixmap("assets/focus_logo.png").scaled(
            80, 80, 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
            )

        
        self.logo_button.setIcon(QIcon(pixmap))
        self.logo_button.setIconSize(pixmap.size())
        self.logo_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.logo_button.setStyleSheet("""
        QPushButton {
            border: none;
            background: transparent;
            padding: 0px;
        }

        QPushButton:hover {
            background: transparent;
        }

        QPushButton:pressed {
            background: transparent;
        }

        QPushButton:focus {
            outline: none;
        }
        """)


        top_bar.addWidget(self.logo_button, alignment=Qt.AlignLeft)
        top_bar.addStretch()

        layout.addLayout(top_bar)

        self.settings_button = QPushButton()
        self.settings_button.setCursor(Qt.PointingHandCursor)

        s_pixmap = QPixmap("assets/settings.png").scaled(
            48, 48, 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
            )

        
        self.settings_button.setIcon(QIcon(s_pixmap))
        self.settings_button.setIconSize(s_pixmap.size())
        self.settings_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.settings_button.setStyleSheet("""
        QPushButton {
            border: none;
            background: transparent;
            padding: 0px;
        }

        QPushButton:hover {
            background: transparent;
        }

        QPushButton:pressed {
            background: transparent;
        }

        QPushButton:focus {
            outline: none;
        }
        """)

        top_bar.addWidget(self.settings_button)

        layout.addLayout(top_bar)

        self.title_label = QLabel("FOCUS Mode")
        self.title_label.setFont(text_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        layout.addWidget(self.title_label)

        self.mode_label = QLabel("Work")
        self.mode_label.setFont(text_font)
        self.mode_label.setAlignment(Qt.AlignCenter)
        self.mode_label.setStyleSheet("font-size: 36px; font-weight: bold;")
        layout.addWidget(self.mode_label)

        mode_layout = QHBoxLayout()

        self.work_button = QPushButton("Work")
        self.work_button.setCheckable(True)
        self.work_button.setChecked(True)
        self.work_button.setFixedSize(200, 60)
        self.work_button.setStyleSheet(work_button_style)
        self.work_button.setCursor(Qt.PointingHandCursor)
        mode_layout.addWidget(self.work_button)

        #short break button
        self.break_button = QPushButton("Break")
        self.break_button.setCheckable(True)
        self.break_button.setFixedSize(200, 60)
        self.break_button.setStyleSheet(work_button_style)
        self.break_button.setCursor(Qt.PointingHandCursor)
        mode_layout.addWidget(self.break_button)

        layout.addLayout(mode_layout)

        timer_layout = QHBoxLayout()

        timer_widget = QWidget()
        timer_layout = QHBoxLayout(timer_widget)
        timer_layout.setContentsMargins(100, 0, 0, 0)
        timer_layout.setSpacing(12)

        # Timer label
        self.timer_label = QLabel("25:00")
        self.timer_label.setFont(timer_font)
        self.timer_label.setFixedWidth(300)
        self.timer_label.setFixedHeight(150)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet(
            "font-size: 72px; font-weight: bold; background-color: #54596e; padding: 6px 10px; border-radius: 16px;"
        )

        # Skip button
        self.skip_button = QPushButton()
        self.skip_button.setCursor(Qt.PointingHandCursor)

        pixmap = QPixmap("assets/skip.png").scaled(
            75, 75, 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
            )

        
        self.skip_button.setIcon(QIcon(pixmap))
        self.skip_button.setIconSize(pixmap.size())
        self.skip_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.skip_button.setStyleSheet("""
        QPushButton {
            border: none;
            background: transparent;
            padding: 0px;
        }

        QPushButton:hover {
            background: transparent;
        }

        QPushButton:pressed {
            background: transparent;
        }

        QPushButton:focus {
            outline: none;
        }
        """)

        #Skip spacer
        self.skip_spacer = QSpacerItem(80, 40, QSizePolicy.Fixed, QSizePolicy.Minimum)

        timer_layout.addWidget(self.timer_label)
        timer_layout.addWidget(self.skip_button)
        timer_layout.addItem(self.skip_spacer)

        # Center the *widget* in the parent layout
        layout.addWidget(timer_widget, alignment=Qt.AlignCenter)

        self.toggle_button = QPushButton("Start")
        self.toggle_button.setCheckable(True)
        self.toggle_button.setCursor(Qt.PointingHandCursor)
        self.toggle_button.setStyleSheet(toggle_button_style)
        self.toggle_button.setFixedSize(200, 60)
        layout.addWidget(self.toggle_button, alignment=Qt.AlignCenter)

        self.end_button = QPushButton("End Session")
        self.end_button.setCursor(Qt.PointingHandCursor)
        self.end_button.setStyleSheet(end_button_style)
        self.end_button.setFixedSize(200, 60)
        layout.addWidget(self.end_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        self.toggle_button.clicked.connect(lambda: self.toggle_clicked.emit())
        self.work_button.clicked.connect(lambda: self.mode_changed.emit("work"))
        self.break_button.clicked.connect(lambda:self.mode_changed.emit("break"))
        self.end_button.clicked.connect(lambda: self.end_clicked.emit())
        self.logo_button.clicked.connect(self.emit_home_clicked)
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
    
    def emit_home_clicked(self):
        self.home_clicked.emit()
    
    def update_controls(self, is_running: bool, has_started: bool):
        # Start / Pause button
        if is_running:
            self.toggle_button.setText("Pause")
        else:
            self.toggle_button.setText("Start")

        # Skip button visibility
        self.skip_button.setVisible(has_started)
