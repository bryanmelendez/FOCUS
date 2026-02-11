from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QIcon

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):

        button_font = QFont("Menlo", 30)
        label_font = QFont("Menlo")
        button_font.setWeight(QFont.Medium)

        

        free_button_style = """
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
            background-color: #803d39;
        }
        """

        focus_button_style = """
        QPushButton {
            background-color: #47ac96;
            color: #eee6e2;
            font-weight: 600;
            border-radius: 16px;
            border: none;
        }

        QPushButton:hover {
            background-color: #3aa18c;
        }

        QPushButton:pressed {
            background-color: #2f8f7a;
        }
        """

        history_button_style = """
        QPushButton {
            background-color: #434343;
            color: #eee6e2;
            font-weight: 600;
            border-radius: 16px;
            border: none;
        }

        QPushButton:hover {
            background-color: #343434;
        }

        QPushButton:pressed {
            background-color: #232222;
            }
        """

        layout = QVBoxLayout()


        self.logo_button = QPushButton()

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


        layout.addWidget(self.logo_button)

        # Welcome label at the top, centered
        self.welcome_label = QLabel("Time to FOCUS ...")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setFont(label_font)

        self.welcome_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(self.welcome_label)

        layout.addStretch(1)

        button_layout = QHBoxLayout()

        # Free mode button
        self.free_button = QPushButton("Free Study")
        self.free_button.setCursor(Qt.PointingHandCursor)
        self.free_button.setFixedSize(250, 250)
        self.free_button.setFont(button_font)
        self.free_button.setStyleSheet(free_button_style)
        button_layout.addWidget(self.free_button)

        # FOCUS button
        self.focus_button = QPushButton("FOCUS Mode")
        self.focus_button.setCursor(Qt.PointingHandCursor)
        self.focus_button.setFixedSize(250, 250)
        self.focus_button.setFont(button_font)
        self.focus_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.focus_button.setStyleSheet(focus_button_style)
        button_layout.addWidget(self.focus_button)

        # History button
        self.history_button = QPushButton("History")
        self.history_button.setCursor(Qt.PointingHandCursor)
        self.history_button.setFixedSize(250, 250)
        self.history_button.setFont(button_font)
        self.history_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.history_button.setStyleSheet(history_button_style)
        button_layout.addWidget(self.history_button)

        layout.addLayout(button_layout)

        layout.addStretch(1)

        self.setLayout(layout)

