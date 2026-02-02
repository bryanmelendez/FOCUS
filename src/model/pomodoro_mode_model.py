# model.py

class PomodoroModel:

    def __init__(self):
        self.modes = {
            "work": 25 * 60,       # 25 minutes
            "break": 5 * 60,       # 5 minutes
        }

        self.mode = "work"  # can be "work" or "break"
        self.remaining_time = self.modes[self.mode]
        self.is_running = False
        self.has_started = False

    

