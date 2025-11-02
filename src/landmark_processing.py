# todo: imports

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

