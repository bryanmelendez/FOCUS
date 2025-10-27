import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

IMAGE_PATH = 'images/bryan.png'
model_path = 'models/face_landmarker.task'

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE)

# Load the input image from an image file.
mp_image = mp.Image.create_from_file(IMAGE_PATH)

# The landmarker is initialized. Use it here.
with FaceLandmarker.create_from_options(options) as landmarker:
    face_landmarker_result = landmarker.detect(mp_image)

print(face_landmarker_result)