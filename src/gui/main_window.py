from pomodoro_view import PomodoroTimerView 
from regular_mode_view import RegularTimerView 

from PySide6 import QtCore, QtWidgets, QtGui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app_controller):
        super().__init__()
        self.controller = app_controller

        # self.regular_view = RegularTimerView()
        self.pomodoro_view = PomodoroTimerView()

        self.stacked = QtWidgets.QStackedWidget()
        # self.stacked.addWidget(self.regular_view)
        self.stacked.addWidget(self.pomodoro_view)
