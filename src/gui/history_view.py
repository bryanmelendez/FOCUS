from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, 
                               QScrollArea, QFrame, QHBoxLayout, QSizePolicy)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QIcon, QFont

from controller.history_controller import HistoryController


class HistoryView(QWidget):
    home_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = HistoryController()
        self.init_ui()

    def showEvent(self, event):
        """Refresh sessions list when the view is shown"""
        super().showEvent(event)
        self.refresh_sessions()
    
    def refresh_sessions(self):
        """Clear and reload the sessions list"""
        # Clear existing session buttons
        while self.sessions_layout.count():
            item = self.sessions_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Reload sessions
        self.populate_sessions(self.controller.read_sessions())

    def init_ui(self):
        self.setWindowTitle("Session History")
        
        text_font = QFont("Menlo")
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Top bar with home button
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
        
        self.logo_button.clicked.connect(lambda: self.home_clicked.emit())
        
        top_bar.addWidget(self.logo_button, alignment=Qt.AlignLeft)
        top_bar.addStretch()
        
        main_layout.addLayout(top_bar)
        
        # Title
        title_label = QLabel("Past Sessions")
        title_label.setFont(text_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # Horizontal layout to center scroll area
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)
        
        # Scroll area for sessions
        scroll_area = QScrollArea()
        scroll_area.setFixedWidth(350)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Container widget for sessions
        container = QWidget()
        self.sessions_layout = QVBoxLayout(container)
        self.sessions_layout.setAlignment(Qt.AlignTop)
        self.sessions_layout.setSpacing(10)
        
        scroll_area.setWidget(container)
        h_layout.addWidget(scroll_area)
        h_layout.addStretch(1)
        
        main_layout.addLayout(h_layout)

    def add_session_link(self, timestamp, session_data):
        """Add a clickable link for a session"""
        text_font = QFont("Menlo")
        label = session_data.get('qualitative_label', '')
        button_text = f"{timestamp}\n{label}"
        button = QPushButton(button_text)
        button.setFont(text_font)
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet("""
            QPushButton {
                text-align: center;
                padding: 15px;
                font-size: 16px;
                background-color: #434343;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1F6FE0;
            }
            QPushButton:pressed {
                background-color: #1859B7;
            }
        """)
        
        # Connect button click to show stats
        button.clicked.connect(lambda: self.controller.show_stats(session_data))
        
        self.sessions_layout.addWidget(button)

    def populate_sessions(self, sessions):
        """Populate the view with all sessions"""
        if not sessions:
            no_sessions_label = QLabel("No past sessions found")
            no_sessions_label.setAlignment(Qt.AlignCenter)
            no_sessions_label.setStyleSheet("font-size: 16px; color: #666; margin: 20px;")
            self.sessions_layout.addWidget(no_sessions_label)
            return
        
        for session in sessions:
            # Each session is a dict with timestamp as key
            for timestamp, session_data in session.items():
                self.add_session_link(timestamp, session_data)