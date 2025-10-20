import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np
import time

model_path = 'models/blaze_face_short_range.tflite'

BaseOptions = mp.tasks.BaseOptions
FaceDetector = mp.tasks.vision.FaceDetector
FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
FaceDetectorResult = mp.tasks.vision.FaceDetectorResult
VisionRunningMode = mp.tasks.vision.RunningMode

def print_result(result: FaceDetectorResult, output_image: mp.Image, timestamp_ms: int):
    if result.detections:
        for detection in result.detections:
            print(f'Face detected with confidence: {detection.categories[0].score}')

options = FaceDetectorOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

# Initialize webcam
cap = cv2.VideoCapture(0)  # 0 is usually the built-in webcam

with FaceDetector.create_from_options(options) as detector:
    while cap.isOpened():
        # Read frame from webcam
        success, frame = cap.read()
        if not success:
            print("Failed to read from webcam")
            break

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Create MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, 
                           data=np.array(rgb_frame))

        # Get timestamp for this frame
        frame_timestamp_ms = int(time.time() * 1000)

        # Detect async
        detector.detect_async(mp_image, frame_timestamp_ms)

        # Display the frame
        cv2.imshow('Face Detection', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()