from face_detection import FaceDetector
from landmark_processing import LandmarkProcessor
import numpy as np
import matplotlib.pyplot as plt
import cv2
from time import time, sleep

def main():
    face_detector = FaceDetector()
    # face_detector.run_detection()
    # face_detector.get_landmarks_looped()
    landmark_processor = LandmarkProcessor()

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

            if current_time - last_plot_time >= 1.0:
                # Create MediaPipe Image from cv2 frame
                mp_image = face_detector.create_mediapipe_image(frame)
                results = face_detector.get_landmarks(mp_image)
                face_landmarks = results.face_landmarks[0]
                # print('face landmarker result: {}'.format(results)) # uncomment this if you want to see the full landmarks data

                # ===================================================
                # NOTE - this is where you would call the algorithms

                # NOTE: Example - remove this later
                nose_tip = face_landmarks[4]
                print(f"Nose tip - x: {nose_tip.x}, y: {nose_tip.y}, z: {nose_tip.z}")
                top_of_forehead = face_landmarks[10]
                print(f"Top of forehead - x: {top_of_forehead.x}, y: {top_of_forehead.y}, z: {top_of_forehead.z}")

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

                landmark_processor.processSoA(face_landmarks)

                # ===================================================

                plt.clf()  # Clear the current figure

                # Annotate the image with the detected landmarks
                annotated_image = face_detector.draw_landmarks_on_image(mp_image.numpy_view(), results)

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