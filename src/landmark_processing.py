import cv2
import math
import numpy as np

def relative(landmark, frame_shape):
    h, w = frame_shape[:2]
    return (int(landmark.x * w), int(landmark.y * h))

def rotation_matrix_to_angles(rotation_matrix):
    """
    Calculate Euler angles (in degrees) from a 3x3 rotation matrix.
    These correspond to rotations around x (pitch), y (yaw), z (roll) axes.
    """
     # pitch (x-axis rotation)
    x = math.atan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
   
    # yaw (y-axis rotation)
    y = math.atan2(-rotation_matrix[2, 0],
                   math.sqrt(rotation_matrix[0, 0] ** 2 + rotation_matrix[1, 0] ** 2))
    
    # roll (z-axis rotation)
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
         (0.0, 0.0, 0.0),       # Nose tip
        (0, -63.6, -12.5),     # Chin
        (-43.3, 32.7, -26),    # Left eye left corner
        (43.3, 32.7, -26),     # Right eye right corner
        (-28.9, -28.9, -24.1), # Left Mouth corner
        (28.9, -28.9, -24.1)   # Right mouth corner
    ])

       #landmark_indices = [1,9,57,130,287,359]
       # face_coordination_image = np.array(
         #  [[landmarks[i].x * w, landmarks[i].y*h] for i in landmark_indices], dtype=np.float64
       # )
        
    
        face_coordination_image = np.array([
        relative(landmarks[4], frame_shape),    # Nose tip
        relative(landmarks[152], frame_shape),  # Chin
        relative(landmarks[264], frame_shape),  # Left eye left corner
        relative(landmarks[33], frame_shape),   # Right eye right corner
        relative(landmarks[287], frame_shape),  # Left Mouth corner
        relative(landmarks[57], frame_shape)    # Right mouth corner
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

        print("Rotation matrix: ")
        print(rotation_matrix)

        return{
            "pitch": angles[0],
            "yaw": angles[1], 
            "roll": angles[2]
        }

    def compute_gaze(self, landmarks):
        # todo
        pass

    def process_frame(self, landmarks, frame_shape):
        EAR = self.compute_EAR(landmarks)
        MAR = self.compute_MAR(landmarks)
        head_pose = self.compute_head_pose(landmarks, frame_shape)
        gaze = self.compute_gaze(landmarks)

        results = {
            "EAR": EAR, "MAR": MAR, "head_pose": head_pose, "gaze": gaze
        }
        return results

