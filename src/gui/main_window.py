
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from gui.pomodoro_view import PomodoroView

class MainWindow(QMainWindow):
    def __init__(self, app_controller):
        super().__init__()
        self.controller = app_controller

        self.setWindowTitle("custom main window")

        self.pomodoro_view = PomodoroView()

        self.stacked = QStackedWidget()
        self.stacked.addWidget(self.pomodoro_view)

        self.setCentralWidget(self.stacked)



