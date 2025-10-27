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

    def run_detection(self):
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

    def draw_landmarks(self):
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

        # STEP 4: Detect face landmarks from the input image.
        detection_result = detector.detect(image)

        # STEP 5: Process the detection result. In this case, visualize it.
        annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)

        # Replace cv2_imshow with matplotlib display
        plt.figure(figsize=(10, 10))
        plt.imshow(annotated_image)
        plt.axis('off')
        plt.show()