import cv2
import numpy as np
import time
from collections import deque
from enum import Enum
import matplotlib.pyplot as plt
import math
from utils.logger import Logger

# Define an enumeration for different states of attention
class state(Enum):
    DROWSY = 1
    DISTRACTED = 2
    ATTENTIVE = 3

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
        self.logger = Logger()
        self.funct_time = 60 # second *** REMEMBER TO CHANGE !!! ***
        # EAR values
        self.closed_start_time = None
        self.isClosed = False
        self.closed_time_minumum = 4 # minimum of 4 seconds to be drowsy
        # PERCLOS values
        self.avg_EAR_history = deque() # holds timestamp and avg EAR value
        self.closed_maximum = 0.25 # EAR is less than this -> eye closed
        # MAR/YF values
        self.MAR_minimum = 0.2 # MAR higher than this -> mouth open
        self.MAR_history = deque() # holds timestamp and MAR value
        self.yawn_history = deque() # holds yawns 
        self.yawn_minimum = 3 # minimum of 4 seconds for an open mouth to be consired a yawn
        self.isYawning = False
        self.yawn_start_time = None
        # HP values
        self.yaw_threshold = 30 # degrees
        self.pitch_threshold = 20 # degrees
        self.roll_threshold = 35 # degrees
        self.distracted_time = 3.0 # seconds
        self.head_pose_start_time = None
        # Gaze values
        self.gaze_direction_start_time = None
        # SoA
        self.currentState = self.prevState = state.ATTENTIVE
        self.state_start_time = None
        self.drowsy_alert_time = 5 # seconds
        self.distracted_alert_time = 5 # seconds
        # if want to see trend at end or in email summary or something :p
        self.SoA_history = []
    
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
    
    def compute_MAR(self, landmarks):
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
    
    def compute_PERCLOS(self, landmarks):
        current_time = time.time()
        closed_frames = 0
        total_frames = 0

        _, _, avg_EAR = self.compute_EAR(landmarks)
        self.avg_EAR_history.append((current_time, avg_EAR))
        # past 60 seconds, start cycling
        while current_time - self.avg_EAR_history[0][0] > self.funct_time:
            self.avg_EAR_history.popleft()
        total_frames = len(self.avg_EAR_history)
        # compute PERCLOS for current samples
        for (_, ear_value) in self.avg_EAR_history:
            if ear_value <= self.closed_maximum:
                closed_frames += 1

        if total_frames < self.funct_time:
            return 0 # wait for full time to start - CHANGE ?
        else:
            PERCLOS = (closed_frames/total_frames)

        return PERCLOS

    def compute_yawn_freq(self, landmarks):
        current_time = time.time()

        MAR = self.compute_MAR(landmarks)
        self.MAR_history.append((current_time, MAR))

        # past 60 seconds, start cycling
        while current_time - self.MAR_history[0][0] > self.funct_time:
            self.MAR_history.popleft()

        if MAR > self.MAR_minimum:
            if not self.isYawning:
                self.yawn_start_time = time.time()
                self.isYawning = True
        else:
            if self.isYawning:
                # check mouth open time
                duration = current_time - self.yawn_start_time
                if duration >= self.yawn_minimum: # longer than 4 seconds
                    self.yawn_history.append(current_time)
                self.isYawning = False
        # remove old yawns after 60s
        while self.yawn_history and current_time - self.yawn_history[0] > self.funct_time:
            self.yawn_history.popleft()
        
        yawn_freq = len(self.yawn_history)
        return yawn_freq

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
        dy = cy - y_center

        theta = math.degrees(math.atan2(dy, dx))

        return (theta, dx, dy)

    def classify_gaze_direction(self, eye):
        theta = eye[0]
        dx = eye[1]
        dy = eye[2]

        if -7 < dx < 7 and -3 < dy < 3: # TODO - find the actual threshold
            return "Center"

        if 135 <= theta <= 180 or -180 <= theta <= -135:
            return "Right"
        if -135 < theta <= -45:
            return "Up"
        if 0 <= theta < 45 or 0 > theta > -45:
            return "Left"
        if 45 <= theta < 135:
            return "Down"

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
        PERCLOS = self.compute_PERCLOS(landmarks)
        YF = self.compute_yawn_freq(landmarks)
        head_pose = self.compute_head_pose(landmarks, frame_shape)
        gaze = self.compute_gaze(landmarks, frame_shape)
        #head_pose = 12 # placeholder value
        #gaze = 12 # placeholder value

        results = {
            "EAR": EAR, "MAR": MAR, "PERCLOS": PERCLOS, "YF": YF, "head_pose": head_pose, "gaze": gaze
        }
        currentState = self.estimateSoA(PERCLOS, YF, gaze, head_pose)
        return results, currentState

    def estimateSoA(self, PERCLOS, YF, GD, head_pose):
        # determine state of attention *** CHANGE THRESHOLDS ***

        soa = None

        current_time = time.time()
        # DROWSY condition
        if PERCLOS >= 0.35 or YF >= 2:
            self.currentState = state.DROWSY
        # DISTRACTED condition
        # head pose
        yaw = abs(head_pose["yaw"])
        pitch = abs(head_pose["pitch"])
        roll = abs(head_pose["roll"])
        if yaw > self.yaw_threshold or pitch > self.pitch_threshold or roll > self.roll_threshold:
            if self.head_pose_start_time is None:
                self.head_pose_start_time = current_time
            elif current_time - self.head_pose_start_time > self.distracted_time:
                soa = state.DISTRACTED
        else:
            soa = state.ATTENTIVE
            self.head_pose_start_time = None
        # gaze direction
        gaze_left = GD[2]
        gaze_right = GD[3]
        if gaze_left != "Center" and gaze_right != "Center":
            if self.gaze_direction_start_time is None:
                self.gaze_direction_start_time = current_time
            elif current_time - self.gaze_direction_start_time > self.distracted_time:
                soa = state.DISTRACTED
        else:
            soa = state.ATTENTIVE
            self.gaze_direction_start_time = None

        if soa is not None: 
            self.currentState = soa 
        
        if self.currentState == None:
            self.logger.error("there is no current state!")

        self.SoA_history.append((time.time(), self.currentState)) # should it be every second ?
        return self.currentState
    
        
    
    def processSoA(self, landmarks, frame_shape):
        current_time = time.time()
        # update current and prev states
        results, currentSoA = self.process_frame(landmarks, frame_shape)

        # if first run, initialize timer
        if self.state_start_time is None:
            self.state_start_time = current_time

        # DEBUG
        # print("current state: {}".format(currentSoA))
        # print("prev state: {}".format(self.prevState))

        # if state changed, reset timer
        if currentSoA != self.prevState:
            self.state_start_time = current_time
            self.prevState = currentSoA

        duration = current_time - self.state_start_time

        if currentSoA == state.DROWSY and duration > self.drowsy_alert_time:
            self.logger.info("DROWSY ALERT")
        elif currentSoA == state.DISTRACTED and duration > self.distracted_alert_time:
            self.logger.info("DISTRACTED ALERT")

        return results, currentSoA

    def graph_SoA_history(self):
        if not self.SoA_history:
            print("No state history to graph.")
            return
    
        # Convert enum to numeric for graphing
        state_to_value = {
            state.DROWSY: 0,
            state.DISTRACTED: 1,
            state.ATTENTIVE: 2
        }

        times = [t - self.SoA_history[0][0] for (t, s) in self.SoA_history]
        values = [state_to_value[s] for (_, s) in self.SoA_history]

        plt.figure(figsize=(10, 4))
        plt.plot(times, values, linewidth=2)

        plt.yticks([0, 1, 2], ["DROWSY", "DISTRACTED", "ATTENTIVE"])
        plt.xlabel("Time (s)")
        plt.ylabel("State of Attention")
        plt.title("Attention State Timeline")
        plt.grid(True)

        plt.show(block=True)