import cv2
import numpy as np

class LandmarkProcessor:
    def __init__(self):
        # idk
        pass
    
    def compute_EAR(self, landmarks):
        # define landmarks
        right_eye = [33, 160, 158, 133, 153, 144]
        left_eye = [33, 160, 158, 133, 153, 144]

        # calculate EAR
        def eye_aspect_ratio(eye_landmarks):
            p1, p2, p3, p4, p5, p6 = eye_landmarks
            # formula 
            A = np.linalg.norm(np.array([p2.x, p2.y]) - np.array([p6.x, p6.y]))
            B = np.linalg.norm(np.array([p3.x, p3.y]) - np.array([p5.x, p5.y]))
            C = np.linalg.norm(np.array([p1.x, p1.y]) - np.array([p4.x, p4.y]))
            ear = (A + B) / (2.0 * C)
            return ear

        # get eye landmarks
        right_eye_points = [landmarks[i] for i in right_eye]
        left_eye_points = [landmarks[i] for i in left_eye]
        # perform EAR calculations
        right_EAR = eye_aspect_ratio(right_eye_points)
        left_EAR = eye_aspect_ratio(left_eye_points)
        avg_EAR = (left_EAR + right_EAR) / 2.0

        return left_EAR, right_EAR, avg_EAR
    
    def compute_MAR(self, landmarks): # revisit ?
        # define landmarks
        right_corner = 61
        left_corner = 291
        top_lip = 13
        bottom_lip = 14

        # get coords
        right = np.array([landmarks[right_corner].x, landmarks[right_corner].y])
        left = np.array([landmarks[left_corner].x, landmarks[left_corner].y])
        top = np.array([landmarks[top_lip].x, landmarks[top_lip].y])
        bottom = np.array([landmarks[bottom_lip].x, landmarks[bottom_lip].y])
        # perform MAR calculations
        vertical_dist = np.linalg.norm(top - bottom)
        horizontal_dist = np.linalg.norm(right - left)
        mar = vertical_dist / horizontal_dist

        return mar

    def compute_head_pose(self, landmarks, frame_shape):
        # todo
        pass

    def compute_gaze(self, landmarks):
        # todo
        pass

    def process_frame(self, landmarks):
        EAR = self.compute_EAR(landmarks)
        MAR = self.compute_MAR(landmarks)
        head_pose = self.compute_head_pose(landmarks)
        gaze = self.compute_gaze(landmarks)

        results = {
            "EAR": EAR, "MAR": MAR, "head_pose": head_pose, "gaze": gaze
        }
        return results

