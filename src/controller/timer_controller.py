class TimerController(QObject):
    time_updated = Signal(int)
    running_changed = Signal(bool)

    def __init__(self, model):
        super().__init__()
        self.model = model

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._tick)

    def start(self):
        self.model.start()
        self.timer.start()
        self.running_changed.emit(True)

    def stop(self):
        self.model.stop()
        self.timer.stop()
        self.running_changed.emit(False)

    def reset(self):
        self.model.reset()
        self.time_updated.emit(self.model.elapsed)

    def _tick(self):
        self.model.tick()
        self.time_updated.emit(
            getattr(self.model, "remaining_time", self.model.elapsed)
        )
