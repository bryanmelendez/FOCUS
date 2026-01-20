class AppController(QObject):
    def __init__(self):
        super().__init__()

        self.face_controller = FaceController(FaceModel())

        self.regular_timer = TimerController(RegularTimerModel())
        self.pomodoro_timer = TimerController(
            PomodoroModel(25 * 60, 5 * 60)
        )

    def start_regular_mode(self):
        self.pomodoro_timer.stop()
        self.regular_timer.start()
        self.face_controller.start()

    def start_pomodoro_mode(self):
        self.regular_timer.stop()
        self.pomodoro_timer.start()
        self.face_controller.start()

    def stop_all(self):
        self.regular_timer.stop()
        self.pomodoro_timer.stop()
        self.face_controller.stop()
