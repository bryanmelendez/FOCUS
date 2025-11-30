# TODO make sure we actually use all of these imports
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2
import numpy as np

class FaceDetector: # TODO reanme this because it conflicts with mediapipe FaceDetector
    def __init__(self):
        self.detection_model_path = 'models/blaze_face_short_range.tflite'
        self.landmark_model_path = 'models/face_landmarker.task'

    def get_landmarks(self, mp_image):
        # Takes in an image and returns the landmark data structure
        base_options = python.BaseOptions(model_asset_path=self.landmark_model_path)
        options = vision.FaceLandmarkerOptions(base_options=base_options,
                                               output_face_blendshapes=True,
                                               output_facial_transformation_matrixes=True,
                                               num_faces=1)
        detector = vision.FaceLandmarker.create_from_options(options)

        detection_result = detector.detect(mp_image)

        return detection_result 

    def create_mediapipe_image(self, bgr_image):
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB) 
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB,
                           data=np.array(rgb_image))
        return mp_image

    def draw_landmarks_on_image(self, rgb_image, detection_result):
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