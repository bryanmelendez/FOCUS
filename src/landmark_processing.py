import cv2
import math
import numpy as np

# Gaze Landmarks
LEFT_IRIS        = [468, 469, 470, 471, 472]
RIGHT_IRIS       = [473, 474, 475, 476, 477]

LEFT_EYE_CORNERS  = [33, 133]
RIGHT_EYE_CORNERS = [362, 263]

LEFT_EYE_LIDS     = [159, 145]
RIGHT_EYE_LIDS    = [386, 374]

LEFT_EYE_OUTLINE  = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
RIGHT_EYE_OUTLINE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]

# TODO - change these to the new angle classification system
# Angular Thresholds
CENTER_ANGLE   = 30    # ±30° → center
LEFT_ANGLE_MIN = 135   # beyond ±135° → left
LEFT_ANGLE_MAX = 180
RIGHT_ANGLE_MIN = -180 # or +180 
RIGHT_ANGLE_MAX = -135
UP_ANGLE_MIN    = -135
UP_ANGLE_MAX    = -45
DOWN_ANGLE_MIN  = 45
DOWN_ANGLE_MAX  = 135

def relative(landmark, frame_shape):
    h, w = frame_shape[:2]
    return (int(landmark.x * w), int(landmark.y * h))

def rotation_matrix_to_angles(rotation_matrix):
    """
    Calculate Euler angles (in degrees) from a 3x3 rotation matrix.
    These correspond to rotations around x (pitch), y (yaw), z (roll) axes.
    """
    x = math.atan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
    y = math.atan2(-rotation_matrix[2, 0], math.sqrt(rotation_matrix[0, 0] ** 2 + rotation_matrix[1, 0] ** 2))
    z = math.atan2(rotation_matrix[1, 0], rotation_matrix[0, 0])

    # Convert radians → degrees

    x = math.degrees(x)
    y = math.degrees(y)
    z = math.degrees(z)
    return np.array([x, y, z])

class LandmarkProcessor:
    def __init__(self):
        # idk
        pass
    
    def compute_EAR(self, landmarks):
        # todo
        pass
    
    def compute_MAR(self, landmarks):
        # todo
        pass

    def compute_head_pose(self, landmarks, frame_shape):
        # todo
        h, w, _ = frame_shape

        #approximate 3D coordinates of the human head
        face_coordination_real_world = np.array([
        [285, 528, 200], # Nose tip
        [285, 371, 152], # Forehead
        [197, 574, 128], # Mouth left corner
        [173, 425, 108], # Left eye left corner
        [360, 574, 128], # Mouth right corner
        [391, 425, 108] # Right eye right corner
         ], dtype=np.float64)
       #landmark_indices = [1,9,57,130,287,359]
       # face_coordination_image = np.array(
         #  [[landmarks[i].x * w, landmarks[i].y*h] for i in landmark_indices], dtype=np.float64
       # )
        
    
        face_coordination_image = np.array([
        relative(landmarks[1], frame_shape),  # Nose tip
        relative(landmarks[9], frame_shape),  # Forehead
        relative(landmarks[57], frame_shape), # Mouth left corner
        relative(landmarks[130], frame_shape),   # Left eye left corner
        relative(landmarks[287], frame_shape),  # Mouth right corner
        relative(landmarks[359], frame_shape)    # Right eye right corner
    ], dtype="double")

        #camera matrix
        focal_length = w
        camera_matrix = np.array([
            [focal_length, 0, w/2],
            [0, focal_length, h/2],
            [0,0,1]
        ])

        #distance matrix
        dist_matrix = np.zeros((4,1), dtype=np.float64)
    
        success, rotation_vec, translation_vec = cv2.solvePnP(
            face_coordination_real_world,
            face_coordination_image,
            camera_matrix,
            dist_matrix,
            flags=cv2.SOLVEPNP_ITERATIVE
        )

        if not success:
            return None
        
        rotation_matrix, _ = cv2.Rodrigues(rotation_vec)
        angles = rotation_matrix_to_angles(rotation_matrix)

        # print("Rotation matrix: ")
        # print(rotation_matrix)

        return{
            "pitch": angles[0],
            "yaw": angles[1], 
            "roll": angles[2]
        }

    def compute_eye_angle(self, landmarks, corner_idxs, lid_idxs, iris_idxs, frame_width, frame_height) -> tuple:
        # Compute Eye Corners (x,y)
        corners = []
        for i in corner_idxs:
            x = int(landmarks[i].x * frame_width)
            y = int(landmarks[i].y * frame_height)
            corners.append((x, y))
        
        # Compute Eyelid Verticle Center
        y_top = int(landmarks[lid_idxs[0]].y * frame_height)
        y_bottom = int(landmarks[lid_idxs[1]].y * frame_height)
        
        # Compute the Eye Center
        x_center = (corners[0][0] + corners[1][0]) // 2
        y_center = int((y_top+y_bottom) / 2)

        # Compute Iris Points
        iris_pts = []
        for i in iris_idxs:
            x = int(landmarks[i].x * frame_width)
            y = int(landmarks[i].y * frame_height)
            iris_pts.append((x, y))
        
        if not iris_pts:
            return (None, None, None)

        # Find Iris Center
        (cx, cy), _ = cv2.minEnclosingCircle(np.array(iris_pts, dtype=np.int32))
        cx, cy = int(cx), int(cy)

        # Compute the Angle Between Iris Center and Eye Center
        dx = cx - x_center
        dy = cy - y_center # NOTE - this is where the problem is - if you look up y should be positive, if you look down y should be negative (both are negative)

        theta = math.degrees(math.atan2(dy, dx))

        return (theta, dx, dy)

    def classify_gaze_direction(self, eye):
        theta = eye[0]
        dx = eye[1]

        if -7 < dx < 7: # TODO - find the actual threshold
            return "Center"

        if -45 <= theta < 45:
            return "Right"
        if 45 <= theta < 135:
            return "Down"
        if theta >= 135 or theta < -135:
            return "Left"
        if -135 <= theta < -45:
            return "Up"

    def compute_gaze(self, landmarks, frame_shape):
        h, w, _ = frame_shape

        left_eye = self.compute_eye_angle(
            landmarks, LEFT_EYE_CORNERS, LEFT_EYE_LIDS, LEFT_IRIS, w, h 
        )
        right_eye = self.compute_eye_angle(
            landmarks, RIGHT_EYE_CORNERS, RIGHT_EYE_LIDS, RIGHT_IRIS, w, h 
        )

        gaze_left = self.classify_gaze_direction(left_eye)
        gaze_right = self.classify_gaze_direction(right_eye)

        return (left_eye[0], right_eye[0], gaze_left, gaze_right)


    def process_frame(self, landmarks, frame_shape):
        EAR = self.compute_EAR(landmarks)
        MAR = self.compute_MAR(landmarks)
        head_pose = self.compute_head_pose(landmarks, frame_shape)
        gaze = self.compute_gaze(landmarks, frame_shape)

        results = {
            "EAR": EAR, "MAR": MAR, "head_pose": head_pose, "gaze": gaze
        }
        return results
