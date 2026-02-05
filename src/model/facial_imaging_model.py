import cv2

from utils.logger import Logger
from face_detection import FaceDetector
from landmark_processing import LandmarkProcessor, state

class FacialImagingModel():
    def __init__(self) -> None:
        self.face_detector = FaceDetector()
        self.landmark_processor = LandmarkProcessor()
        self.logger = Logger()
        self.state = state
        self.cap = None
