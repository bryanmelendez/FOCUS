class MainWindow(QMainWindow):
    def __init__(self, app_controller):
        super().__init__()
        self.controller = app_controller

        self.regular_view = RegularTimerView()
        self.pomodoro_view = PomodoroView()

        self.stacked = QStackedWidget()
        self.stacked.addWidget(self.regular_view)
        self.stacked.addWidget(self.pomodoro_view)
