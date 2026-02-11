from PySide6.QtWidgets import (QDialog, QLabel, QVBoxLayout, QProgressBar, QWidget, QGridLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class StatsWindowView(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)

        # self.model = StatsWindowModel()
        # self.controller = StatsWindowController()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Session Summary")
        self.setFixedSize(650, 380)
        self.layout = QVBoxLayout(self)
        
        text_font = QFont("Menlo")
        
        # Set dialog background color to match app theme
        self.setStyleSheet("background-color: #262836;")

        # title
        self.title_label = QLabel("")
        self.title_label.setFont(text_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 30px; font-weight: 600; color: #eee6e2;")
        self.layout.addWidget(self.title_label)

        # progress bars
        self.attentive_bar = QProgressBar()
        self.attentive_bar.setFont(text_font)
        self.attentive_bar.setFormat("Attentive %p%")
        self.attentive_bar.setMinimumHeight(35)
        self.attentive_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1a1d28;
                border-radius: 16px;
                text-align: center;
                color: #eee6e2;
                font-weight: 600;
                padding: 2px;
            }
            QProgressBar::chunk {
                background-color: #47ac96;
                border-radius: 14px;
            }
        """)

        self.inattentive_bar = QProgressBar()
        self.inattentive_bar.setFont(text_font)
        self.inattentive_bar.setFormat("Inattentive %p%")
        self.inattentive_bar.setMinimumHeight(35)
        self.inattentive_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1a1d28;
                border-radius: 16px;
                text-align: center;
                color: #eee6e2;
                font-weight: 600;
                padding: 2px;
            }
            QProgressBar::chunk {
                background-color: #f66e60;
                border-radius: 14px;
            }
        """)

        self.layout.addWidget(self.attentive_bar)
        self.layout.addWidget(self.inattentive_bar)

        # stats grid
        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)

    def set_title(self, text, color):
        self.title_label.setText(text)
        self.title_label.setStyleSheet(
            f"font-size: 30px; font-weight: 600; color: {color};"
        )

    def set_progress(self, attentive_pct, inattentive_pct):
        self.attentive_bar.setValue(int(attentive_pct))
        self.inattentive_bar.setValue(int(inattentive_pct))

    def add_stat_box(self, title, value, row, col):
        box = QWidget()
        layout = QVBoxLayout(box)
        
        text_font = QFont("Menlo")

        t = QLabel(title)
        t.setFont(text_font)
        t.setAlignment(Qt.AlignCenter)
        t.setStyleSheet("font-size: 18px; font-weight: 600; color: #eee6e2;")

        v = QLabel(value)
        v.setFont(text_font)
        v.setAlignment(Qt.AlignCenter)
        v.setStyleSheet("font-size: 16px; color: #eee6e2;")

        layout.addWidget(t)
        layout.addWidget(v)

        self.grid.addWidget(box, row, col)

