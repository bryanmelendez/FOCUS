class FaceWorker(QObject):
    frame_processed = Signal(dict)
    finished = Signal()

    def __init__(self, face_model):
        super().__init__()
        self.model = face_model
        self.running = False

    def start(self):
        self.running = True
        self._loop()

    def stop(self):
        self.running = False

    def _loop(self):
        while self.running:
            frame = self._capture_frame()
            data = self.model.process_frame(frame)
            self.frame_processed.emit(data)
            QThread.msleep(33)

        self.finished.emit()



class FaceController(QObject):
    face_data_updated = Signal(dict)

    def __init__(self, face_model):
        super().__init__()

        self.thread = QThread()
        self.worker = FaceWorker(face_model)

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.start)
        self.worker.frame_processed.connect(self.face_data_updated)
        self.worker.finished.connect(self.thread.quit)

    def start(self):
        if not self.thread.isRunning():
            self.thread.start()

    def stop(self):
        self.worker.stop()
