# TODO - separate the logic in this file

from PySide6.QtCore import QTimer, QObject, Signal
from src.model.model import PomodoroModel


class PomodoroController(QObject):
    time_updated = Signal(int, bool)  # remaining_time, is_work_period
    state_changed = Signal(bool)      # is_running

    def __init__(self, work_duration=25 * 60, break_duration=5 * 60):
        super().__init__()

        self.model = PomodoroModel(work_duration, break_duration)

        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)

        self.image_timer = QTimer()
        self.image_timer.timeout.connect(self.process_image)

    def start(self):
        self.model.start()
        self.timer.start(1000)
        self.state_changed.emit(True)

        self.image_timer.start(33)  # about 30 fps facial imaging

    def stop(self):
        self.model.stop()
        self.timer.stop()
        self.state_changed.emit(False)

    def reset(self):
        self.model.reset()
        self.timer.stop()
        self.state_changed.emit(False)
        self.time_updated.emit(self.model.remaining_time, self.model.is_work_period)

    def _tick(self):
        self.model.tick()
        self.time_updated.emit(self.model.remaining_time, self.model.is_work_period)

    # TODO - separate this code later
    def process_image(self):
        print("hello")
