from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stderr = open(os.devnull, "w")
from face_detection import FaceDetector
from landmark_processing import LandmarkProcessor
import numpy as np
import matplotlib.pyplot as plt
import cv2
from time import time, sleep
from datetime import datetime
from utils.logger import Logger

app = QApplication(sys.argv)

main_window = MainWindow(app_controller=None)
main_window.show()

app.exec()