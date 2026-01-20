class BaseTimerModel:
    def __init__(self):
        self.is_running = False
        self.elapsed = 0

    def start(self):
        self.is_running = True

    def stop(self):
        self.is_running = False

    def reset(self):
        self.elapsed = 0

    def tick(self):
        if self.is_running:
            self.elapsed += 1