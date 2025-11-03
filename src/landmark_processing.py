import cv2
import math
import numpy as np

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
    return np.array([x, y, z]) * 180. / math.pi

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
            [285, 528, 200], #nose tip
            [285, 371, 152], #chin
            [197, 574, 128], #left eye left corner
            [173, 425, 108], #right eye right corner
            [360, 574, 128], #left mouth corner
            [391, 425, 108] #right mouth corner
        ], dtype=np.float64)

        landmark_indices = [1,9,57,130,287,359]
        face_coordination_image = np.array(
            [[landmarks[i].x * w, landmarks[i].y*h] for i in landmark_indices], dtype=np.float64
        )

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

