from face_detection import FaceDetector
import numpy as np
import matplotlib.pyplot as plt
import cv2
from time import time, sleep

def main():
    face_detector = FaceDetector()
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

            if current_time - last_plot_time >= 1.0:
                # Create MediaPipe Image from cv2 frame
                mp_image = face_detector.create_mediapipe_image(frame)
                results = face_detector.get_landmarks(mp_image)
                print('face landmarker result: {}'.format(results))

                # ===================================================
                # NOTE - this is where you would call the algorithms





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