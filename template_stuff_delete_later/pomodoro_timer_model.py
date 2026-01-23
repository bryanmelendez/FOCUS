from base_timer_model import BaseTimerModel

class PomodoroModel(BaseTimerModel):
    def __init__(self, work_duration, break_duration):
        super().__init__()
        self.work_duration = work_duration
        self.break_duration = break_duration
        self.is_work_period = True
        self.remaining_time = work_duration

    def tick(self):
        if not self.is_running:
            return

        self.remaining_time -= 1
        if self.remaining_time <= 0:
            self.is_work_period = not self.is_work_period
            self.remaining_time = (
                self.work_duration if self.is_work_period else self.break_duration
            )
