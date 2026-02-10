from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QPushButton, 
                               QScrollArea, QFrame, QHBoxLayout)
from PySide6.QtCore import Qt, Signal

from controller.history_controller import HistoryController


class HistoryView(QWidget):
    home_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = HistoryController()
        self.init_ui()

        self.populate_sessions(self.controller.read_sessions())

    def init_ui(self):
        self.setWindowTitle("Session History")
        self.setFixedSize(500, 600)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Top bar with home button
        top_bar = QHBoxLayout()
        
        self.home_button = QPushButton("Home")
        self.home_button.setFixedSize(80, 40)
        self.home_button.clicked.connect(lambda: self.home_clicked.emit())
        
        top_bar.addWidget(self.home_button)
        top_bar.addStretch()
        
        main_layout.addLayout(top_bar)
        
        # Title
        title_label = QLabel("Past Sessions")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # Scroll area for sessions
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Container widget for sessions
        container = QWidget()
        self.sessions_layout = QVBoxLayout(container)
        self.sessions_layout.setAlignment(Qt.AlignTop)
        self.sessions_layout.setSpacing(10)
        
        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

    def add_session_link(self, timestamp, session_data):
        """Add a clickable link for a session"""
        button = QPushButton(timestamp)
        button.setStyleSheet("""
            QPushButton {
                text-align: left;
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