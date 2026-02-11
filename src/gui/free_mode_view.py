from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QIcon

class FreeTimerView(QWidget):

    toggle_clicked = Signal()
    end_clicked = Signal()
    home_clicked = Signal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        
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

        
        layout = QVBoxLayout()
        top_bar = QHBoxLayout()

        self.logo_button = QPushButton()
        self.logo_button.setCursor(Qt.PointingHandCursor)

        pixmap = QPixmap("assets/pokemon.png").scaled(
            48, 48, 
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

        self.title_label = QLabel("Free Study")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(text_font)
        self.title_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        layout.addWidget(self.title_label)

       # Timer label
        self.timer_label = QLabel("25:00")
        self.timer_label.setFont(timer_font)
        self.timer_label.setFixedWidth(300)
        self.timer_label.setFixedHeight(150)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet(
            "font-size: 72px; font-weight: bold; background-color: #54596e; padding: 6px 10px; border-radius: 16px;"
        )
        layout.addWidget(self.timer_label, alignment=Qt.AlignHCenter)

        self.toggle_button = QPushButton("Start")
        self.toggle_button.setCursor(Qt.PointingHandCursor)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setFixedSize(200, 60)
        self.toggle_button.setStyleSheet(toggle_button_style)
        layout.addWidget(self.toggle_button, alignment=Qt.AlignCenter)

        self.stop_button = QPushButton("End Session")
        self.stop_button.setCursor(Qt.PointingHandCursor)
        self.stop_button.setFixedSize(200, 60)
        self.stop_button.setStyleSheet(end_button_style)
        layout.addWidget(self.stop_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        self.toggle_button.clicked.connect(lambda: self.toggle_clicked.emit())
        self.stop_button.clicked.connect(lambda: self.end_clicked.emit())
        self.logo_button.clicked.connect(self.emit_home_clicked)

    def emit_home_clicked(self):
        self.home_clicked.emit()

    def set_running(self, running: bool):
        if running:
            self.toggle_button.setText("Pause")
        else:
            self.toggle_button.setText("Start")
            
    def update_time(self, seconds):
        minutes = seconds // 60
        secs = seconds % 60
        self.timer_label.setText(f"{minutes:02d}:{secs:02d}")
