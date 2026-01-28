from PySide6.QtWidgets import QMainWindow, QStackedWidget
from gui.pomodoro_view import PomodoroView
from gui.regular_mode_view import RegularTimerView
from gui.home_window import HomePage  # import your new home page widget

class MainWindow(QMainWindow):
    def __init__(self, app_controller):
        super().__init__()
        self.controller = app_controller

        self.setWindowTitle("FOCUS")

        self.home_page = HomePage()
        self.pomodoro_view = PomodoroView()
        self.regular_view = RegularTimerView()

        self.stacked = QStackedWidget()
        self.stacked.addWidget(self.home_page)      # index 0
        self.stacked.addWidget(self.pomodoro_view)  # index 1
        self.stacked.addWidget(self.regular_view)   # index 2

        self.setCentralWidget(self.stacked)
        
        self.resize(1000, 600)

        # Connect button click to switch view
        self.home_page.pomodoro_button.clicked.connect(self.show_pomodoro)
        self.home_page.regular_button.clicked.connect(self.show_regular)
        self.regular_view.home_button.clicked.connect(self.show_home)
        self.pomodoro_view.home_button.clicked.connect(self.show_home)

    def show_home(self):
        self.stacked.setCurrentIndex(0)  # Show HomePage

    def show_pomodoro(self):
        self.stacked.setCurrentIndex(1)  # Show PomodoroView

    def show_regular(self):
        self.stacked.setCurrentIndex(2)  # Show RegularTimerView
