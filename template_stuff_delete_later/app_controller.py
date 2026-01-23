from face_controller import FaceController
from timer_controller import TimerController
from model.face_model import FaceModel 
from model.pomodoro_timer_model import PomodoroModel
from model.regular_mode_timer_model import RegularTimerModel

from PySide6 import QtCore, QtWidgets, QtGui

class AppController(QtCore.QObject):
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
