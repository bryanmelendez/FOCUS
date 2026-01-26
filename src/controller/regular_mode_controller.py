from model.regular_mode_model import RegularModeModel

class RegularModeController:
    def __init__(self) -> None:
        self.model = RegularModeModel()

    def start_regular_mode(self):
        print(self.model.test)

    def stop_regular_mode(self):
        print("Stopping the session")