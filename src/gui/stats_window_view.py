from PySide6.QtWidgets import (QDialog, QLabel, QVBoxLayout, QProgressBar, QWidget, QGridLayout)
from PySide6.QtCore import Qt

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

        # title
        self.title_label = QLabel("")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 30px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        # progress bars
        self.attentive_bar = QProgressBar()
        self.attentive_bar.setFormat("Attentive %p%")
        self.attentive_bar.setStyleSheet("QProgressBar::chunk { background-color: #4CAF50;}")

        self.inattentive_bar = QProgressBar()
        self.inattentive_bar.setFormat("Inattentive %p%")
        self.inattentive_bar.setStyleSheet("QProgressBar::chunk { background-color: #F44336;}")

        self.layout.addWidget(self.attentive_bar)
        self.layout.addWidget(self.inattentive_bar)

        # stats grid
        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)

    def set_title(self, text, color):
        self.title_label.setText(text)
        self.title_label.setStyleSheet(
            f"font-size: 30px; font-weight: bold; color: {color};"
        )

    def set_progress(self, attentive_pct, inattentive_pct):
        self.attentive_bar.setValue(int(attentive_pct))
        self.inattentive_bar.setValue(int(inattentive_pct))

    def add_stat_box(self, title, value, row, col):
        box = QWidget()
        layout = QVBoxLayout(box)

        t = QLabel(title)
        t.setAlignment(Qt.AlignCenter)
        t.setStyleSheet("font-size: 18px; font-weight: bold;")

        v = QLabel(value)
        v.setAlignment(Qt.AlignCenter)
        v.setStyleSheet("font-size: 16px;")

        layout.addWidget(t)
        layout.addWidget(v)

        self.grid.addWidget(box, row, col)

