# all elements of the gui defined here

import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui


from src.controller.controller import PomodoroController

class PomodoroTimerView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.controller = PomodoroController()

        self.time_label = QtWidgets.QLabel(self._format_time(25*60))
        self.time_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.state_label = QtWidgets.QLabel("Work")
        self.state_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.start_button = QtWidgets.QPushButton("Start")
        self.stop_button = QtWidgets.QPushButton("Stop")
        self.reset_button = QtWidgets.QPushButton("Reset")

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.time_label)
        layout.addWidget(self.state_label)
        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.start_button)
        btn_layout.addWidget(self.stop_button)
        btn_layout.addWidget(self.reset_button)
        layout.addLayout(btn_layout)

        self.start_button.clicked.connect(self.controller.start)
        self.stop_button.clicked.connect(self.controller.stop)
        self.reset_button.clicked.connect(self.controller.reset)

        self.controller.time_updated.connect(self.update_time)
        self.controller.state_changed.connect(self.update_state)

    def _format_time(self, seconds):
        m, s = divmod(seconds, 60)
        return f"{m:02}:{s:02}"

    @QtCore.Slot(int, bool)
    def update_time(self, remaining_time, is_work_period):
        self.time_label.setText(self._format_time(remaining_time))
        self.state_label.setText("Work" if is_work_period else "Break")

    @QtCore.Slot(bool)
    def update_state(self, is_running):
        self.start_button.setEnabled(not is_running)
        self.stop_button.setEnabled(is_running)


