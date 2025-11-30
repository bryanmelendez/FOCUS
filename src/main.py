from face_detection import FaceDetector
from landmark_processing import LandmarkProcessor
import numpy as np
import matplotlib.pyplot as plt
import cv2
from time import time, sleep
from datetime import datetime
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import Logger

def main():
    face_detector = FaceDetector()
    logger = Logger()
    frames_dir = f"{logger.log_path}/frames"
    os.makedirs(frames_dir, exist_ok=True)
    # NOTE - for now either mark this true or false
    save_frames = True 

    landmark_processor = LandmarkProcessor()
    # face_detector.run_detection()
    # face_detector.get_landmarks_looped()

    cap = cv2.VideoCapture(0)  # 0 is usually the built-in webcam
        
    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera")
        return

    last_plot_time = time()
    plt.ion() # interactive plotting mode on
    fig = plt.figure(figsize=(10, 10))

    try:
        while True:
            current_time = time()

            # Capture frame
            ret, frame = cap.read()
            
            if not ret:
                print("Error: Can't receive frame")
                break

            # Display the frame
            cv2.imshow('FOCUS Camera Feed', frame)
            # Break if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if current_time - last_plot_time >= 1.0: # ~30 FPS
                # Create MediaPipe Image from cv2 frame
                mp_image = face_detector.create_mediapipe_image(frame)
                results = face_detector.get_landmarks(mp_image)
                if results is None or len(results.face_landmarks) == 0:
                    logger.warning("No face landmarks detected")
                    continue

                face_landmarks = results.face_landmarks[0]

                # print('face landmarker result: {}'.format(results)) # uncomment this if you want to see the full landmarks data

                # ===================================================
                # NOTE - this is where you would call the algorithms
                pose_results = landmark_processor.process_frame(face_landmarks, frame.shape)
                head_pose = pose_results["head_pose"]

                if head_pose:
                    print(f"Pitch: {head_pose['pitch']:.2f}, "
                          f"Yaw: {head_pose['yaw']:.2f}, "
                          f"Roll: {head_pose['roll']:.2f}, "
                          f"Left Eye Angle: {head_pose['left_eye_angle']:.2f}, Right Eye Angle: {head_pose['right_eye_angle']:.2f}")
                    
                # NOTE: Example - remove this later

                #nose_tip = face_landmarks[4]
                #print(f"Nose tip - x: {nose_tip.x}, y: {nose_tip.y}, z: {nose_tip.z}")
                #top_of_forehead = face_landmarks[10]
                #print(f"Top of forehead - x: {top_of_forehead.x}, y: {top_of_forehead.y}, z: {top_of_forehead.z}")

                # ===================================================

                plt.clf()  # Clear the current figure

                # Annotate the image with the detected landmarks
                annotated_image = face_detector.draw_landmarks_on_image(mp_image.numpy_view(), results)

                # save the image to logs
                if save_frames:
                    frame_filename = f"{frames_dir}/{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.jpg"
                    cv2.imwrite(frame_filename, frame)

                plt.imshow(annotated_image)
                plt.axis('off')
                plt.draw()
                plt.pause(0.001)

                last_plot_time = current_time
            
    except KeyboardInterrupt:
        print("\nStopping camera feed...")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        plt.close('all')
        print("Camera released")

if __name__ == "__main__":
    print("FOCUS: Facial-Orientation and Concentration Understanding System")
    print("Starting testing...")
    print("Press ctrl+c to stop")

    main()