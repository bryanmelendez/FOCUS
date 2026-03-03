# STEP 1: Import the necessary modules.
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import matplotlib.pyplot as plt
import cv2

from src.landmark_processing import LandmarkProcessor
from utils.logger import Logger

model_path = 'models/face_landmarker.task'

IMAGE_PATH = 'poster_images/neet4.jpg'

def draw_landmarks_on_image(rgb_image, detection_result):
  face_landmarks_list = detection_result.face_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected faces to visualize.
  for idx in range(len(face_landmarks_list)):
    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    face_landmarks_list = detection_result.face_landmarks
    annotated_image = np.copy(bgr_image)

    face_landmarks = face_landmarks_list[idx]

    # Draw the face landmarks.
    face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    face_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in face_landmarks
    ])

    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_tesselation_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles
        .get_default_face_mesh_contours_style())
    solutions.drawing_utils.draw_landmarks(
        image=annotated_image,
        landmark_list=face_landmarks_proto,
        connections=mp.solutions.face_mesh.FACEMESH_IRISES,
          landmark_drawing_spec=None,
          connection_drawing_spec=mp.solutions.drawing_styles
          .get_default_face_mesh_iris_connections_style())

    return cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)  # Convert back to RGB for matplotlib

# STEP 2: Create an FaceLandmarker object.
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.FaceLandmarkerOptions(base_options=base_options,
                                       output_face_blendshapes=True,
                                       output_facial_transformation_matrixes=True,
                                       num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)

# STEP 3: Load the input image.
image = mp.Image.create_from_file(IMAGE_PATH)
image_shape = image.numpy_view().shape

# STEP 4: Detect face landmarks from the input image.
detection_result = detector.detect(image)
face_landmarks = detection_result.face_landmarks[0]

# STEP 5: Process the detection result. In this case, visualize it.
annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)

# Replace cv2_imshow with matplotlib display
plt.figure(figsize=(10, 10))
plt.imshow(annotated_image)
plt.axis('off')
plt.show()

logger = Logger()
landmark_processor = LandmarkProcessor()
pose_results = landmark_processor.processSoA(face_landmarks, image_shape)
head_pose = pose_results["head_pose"]
gaze = pose_results["gaze"]

# EAR FUNCTION
left_ear, right_ear, ear_avg = landmark_processor.compute_EAR(face_landmarks)
print(f"EAR: L = {left_ear:.3f}, R = {right_ear:.3f}, Avg = {ear_avg:.3f}")

# PERCLOS FUNCTION
perclos = landmark_processor.compute_PERCLOS(face_landmarks)
print(f"PERCLOS: {perclos:.1f}")

# MAR FUNCTION
mar = landmark_processor.compute_MAR(face_landmarks)
print(f"MAR: {mar:.3f}")

# YF FUNCTION
yawn_freq = landmark_processor.compute_yawn_freq(face_landmarks)
print(f"Yawn Frequency: {yawn_freq} yawns/min")

if head_pose:
    print(f"Pitch: {head_pose['pitch']:.2f}, "
          f"Yaw: {head_pose['yaw']:.2f}, "
          f"Roll: {head_pose['roll']:.2f}")
        
if gaze:
    print(f"Left Eye Angle: {gaze[0]:.2f}, "
          f"Right Eye Angle: {gaze[1]:.2f}")
    print(f"Left Eye Gaze Direction: {gaze[2]}, "
          f"Right Eye Gaze Direction: {gaze[3]}")
    