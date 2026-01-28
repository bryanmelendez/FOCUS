from PySide6.QtCore import QObject, Signal, QThread
from time import time, sleep
import cv2

from model.facial_imaging_model import FacialImagingModel
from utils.logger import Logger


class FacialImagingWorker(QObject):
    data_ready = Signal(object)
    finished = Signal()

    def __init__(self):
        super().__init__()
        self._running = False

        self.model = FacialImagingModel()
        self.logger = Logger()

    def start(self):
        self._running = True
        self._loop()

    def stop(self):
        self._running = False

    def _loop(self):
        interval = 1 / 30  # 30 Hz

        while self._running:
            result = self.process_facial_image()
            self.data_ready.emit(result)
            sleep(interval)

        self.finished.emit()

    def do_work(self):
        # Your repeated function
        print("hello")

    def initialize_imaging(self):
        # TODO - initialize this properly
        if self.model.cap is None:
            self.model.cap = cv2.VideoCapture(0)

        if not self.model.cap.isOpened():
            self.logger.error("Error: Could not open camera")
            return 1

    def deinitialize_imaging(self):
        if self.model.cap is None:
            return 

        if self.model.cap.isOpened():
            self.model.cap.release()
            self.model.cap = None
        return

    def process_facial_image(self):
        self.logger.info("Processing facial image")

        # Capture frame
        ret, frame = self.model.cap.read()
        
        if not ret:
            self.logger.error("Error: Can't receive frame")
            return 

        # Create MediaPipe Image from cv2 frame
        mp_image = self.model.face_detector.create_mediapipe_image(frame)
        results = self.model.face_detector.get_landmarks(mp_image)
        if results is None or len(results.face_landmarks) == 0:
            self.logger.warning("No face landmarks detected")
            return 1 

        face_landmarks = results.face_landmarks[0]

        pose_results, soa = self.model.landmark_processor.processSoA(face_landmarks, frame.shape)
        self.logger.log(pose_results)

                
class FacialImagingController(QObject):
    def __init__(self):
        super().__init__()

        self.worker_thread = QThread()
        self.worker = FacialImagingWorker()

        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.start)
        self.worker.finished.connect(self.worker_thread.quit)

    def start(self):
        # Call init functions
        ret = self.worker.initialize_imaging()
        if ret:
            self.worker.logger.error("Failed to initialize imaging")
            return

        if not self.worker_thread.isRunning():
            self.worker.logger.info("Starting imaging worker")
            self.worker_thread.start()
        else:
            self.worker.logger.error("Imaging worker already running")

    def stop(self):
        ret = self.worker.deinitialize_imaging()
        if ret:
            self.worker.logger.error("Failed to deinitialze imaging")

        self.worker.logger.info("Stopping imaging worker")
        self.worker.stop()