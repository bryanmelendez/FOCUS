import cv2

from utils.logger import Logger
from face_detection import FaceDetector
from landmark_processing import LandmarkProcessor, state

class FacialImagingModel():
    def __init__(self, notification_manager=None) -> None:
        self.face_detector = FaceDetector()
        self.landmark_processor = LandmarkProcessor(notification_manager)
        self.logger = Logger()
        self.state = state
        self.cap = None
