# model.py

class PomodoroModel:
    """
    Stores application state and business logic.
    """

    def __init__(self):
        self.modes = {
            "work": 25 * 60,
            "s_break": 5 * 60,
            "l_break": 15 * 60
        }

        self.current_mode = "work" 
        self.remaining_time = self.modes["work"]
        self.is_running = False

    def set_mode(self, mode: str):
        self.current_mode = mode
        self.remaining_time = self.modes[mode]
        self.is_running = False

    

