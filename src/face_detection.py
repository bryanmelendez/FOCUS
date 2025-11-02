# TODO make sure we actually use all of these imports
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

class FaceDetector: # TODO reanme this because it conflicts with mediapipe FaceDetector
    def __init__(self):
        self.detection_model_path = 'models/blaze_face_short_range.tflite'
        self.landmark_model_path = 'models/face_landmarker.task'

    def run_detection(self): # NOTE: we don't technically need this function since we will just be getting landmarks
        BaseOptions = mp.tasks.BaseOptions
        FaceDetector = mp.tasks.vision.FaceDetector
        FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
        FaceDetectorResult = mp.tasks.vision.FaceDetectorResult
        VisionRunningMode = mp.tasks.vision.RunningMode

        def print_result(result=FaceDetectorResult, output_image=mp.Image, timestamp_ms=int):
            # NOTE: returns result object that contains all data
            if result.detections:
                for detection in result.detections:
                    # Calculate coordinates of center of detected face
                    bbox = detection.bounding_box
                    x = int(bbox.origin_x)
                    y = int(bbox.origin_y)
                    width = int(bbox.width)
                    height = int(bbox.height)

                    center_x = x + (width / 2)
                    center_y = y + (height / 2)
                    print(f'Face center coordinates: ({center_x}, {center_y})')
                    print(f'Face detected with confidence: {detection.categories[0].score}')

        options = FaceDetectorOptions(
            base_options=BaseOptions(model_asset_path=self.detection_model_path),
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

        # Release resources
        cap.release()
        cv2.destroyAllWindows()

    def get_landmarks_looped(self):
        BaseOptions = mp.tasks.BaseOptions
        FaceLandmarker = mp.tasks.vision.FaceLandmarker
        FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
        FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
        VisionRunningMode = mp.tasks.vision.RunningMode

        # Create a face landmarker instance with the live stream mode:
        def print_result(result=FaceLandmarkerResult, output_image=mp.Image, timestamp_ms=int):
            print('face landmarker result: {}'.format(result))

        options = FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=self.landmark_model_path),
            running_mode=VisionRunningMode.LIVE_STREAM,
            result_callback=print_result)

        cap = cv2.VideoCapture(0)  # Initialize webcam

        with FaceLandmarker.create_from_options(options) as landmarker:
            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    print("Failed to read from webcam")
                    break

                # Convert BGR to RGB for MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, 
                                  data=np.array(rgb_frame))

                # Get timestamp for this frame
                frame_timestamp_ms = int(time.time() * 1000)

                # Send live image data for face landmarking
                landmarker.detect_async(mp_image, frame_timestamp_ms)

                # Draw the face landmarks
                if hasattr(landmarker, '_result'):
                    result = landmarker._result
                    if result and result.face_landmarks:
                        for face_landmarks in result.face_landmarks:
                            # Draw the face mesh
                            mp.solutions.drawing_utils.draw_landmarks(
                                image=frame,
                                landmark_list=face_landmarks,
                                connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                                landmark_drawing_spec=None,
                                connection_drawing_spec=mp.solutions.drawing_styles
                                .get_default_face_mesh_tesselation_style())

                            # Draw the face contours
                            mp.solutions.drawing_utils.draw_landmarks(
                                image=frame,
                                landmark_list=face_landmarks,
                                connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
                                landmark_drawing_spec=None,
                                connection_drawing_spec=mp.solutions.drawing_styles
                                .get_default_face_mesh_contours_style())

                # Display the frame
                cv2.imshow('Face Landmarks', frame)

                # Check for 'q' key or Ctrl+C to quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                try:
                    pass
                except KeyboardInterrupt:
                    print("\nStopping face detection...")
                    break

            # Release resources
            cap.release()
            cv2.destroyAllWindows()

    # Takes in an image and returns the landmark data structure
    def get_landmarks(self, mp_image):
        # STEP 2: Create an FaceLandmarker object.
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