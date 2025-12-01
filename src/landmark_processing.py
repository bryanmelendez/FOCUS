import cv2
import numpy as np
import time
from collections import deque
from enum import Enum
import matplotlib.pyplot as plt

# Define an enumeration for different states of attention
class state(Enum):
    DROWSY = 1
    DISTRACTED = 2
    ATTENTIVE = 3

class LandmarkProcessor:
    def __init__(self):
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
        pass

    def compute_gaze(self, landmarks):
        # todo
        pass

    def process_frame(self, landmarks):
        PERCLOS = self.compute_PERCLOS(landmarks)
        YF = self.compute_yawn_freq(landmarks)
        #head_pose = self.compute_head_pose(landmarks)
        #gaze = self.compute_gaze(landmarks)

        head_pose = 12 # placeholder value
        gaze = 12 # placeholder value

        results = {PERCLOS, YF, head_pose, gaze}
        currentState = self.estimateSoA(PERCLOS, YF, gaze)
        return results, currentState
    
    def estimateSoA(self, PERCLOS, YF, GD):
        # determine state of attention *** CHANGE THRESHOLDS ***

        if PERCLOS >= 0.35 or YF >= 2:
            self.currentState = state.DROWSY
        # elif GD indicates gaze away for > 2 seconds: # placeholder condition
        #     state = "DISTRACTED"
        else:
            self.currentState = state.ATTENTIVE

        self.SoA_history.append((time.time(), self.currentState)) # should it be every second ?
        return self.currentState
    
    def processSoA(self, landmarks):
        current_time = time.time()
        # update current and prev states
        _, currentSoA = self.process_frame(landmarks)

        # if first run, initialize timer
        if self.state_start_time is None:
            self.state_start_time = current_time

        # DEBUG
        print("current state: {}".format(currentSoA))
        print("prev state: {}".format(self.prevState))

        # if state changed, reset timer
        if currentSoA != self.prevState:
            self.state_start_time = current_time
            self.prevState = currentSoA

        duration = current_time - self.state_start_time

        # Debounce rules
        if currentSoA == state.DROWSY and duration > self.drowsy_alert_time:
            print("\nDROWSY ALERT")
        elif currentSoA == state.DISTRACTED and duration > self.distracted_alert_time:
            print("\nDISTRACTED ALERT")
        return None

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
