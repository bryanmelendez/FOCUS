from model.regular_mode_model import RegularModeModel
from PySide6.QtCore import QTimer

from controller.facial_imaging_controller import FacialImagingController

class RegularModeController:
    def __init__(self, model, view):
        self.face_controller = FacialImagingController()

        self.model = model
        self.view = view

        # QTimer emits a signal every N milliseconds
        # This is how we "tick" once per second
        self.timer = QTimer()
        self.timer.setInterval(1000)  # 1000 ms = 1 second

        # Every second, call self.tick()
        self.timer.timeout.connect(self.tick)

        # Connect view signals → controller logic
        self.view.toggle_clicked.connect(self.handle_start_toggle) 
        self.view.end_clicked.connect(self.handle_end)
        self.sync_view()
    
    def sync_view(self):
        self.view.set_running(self.model.is_running)
        self.view.update_time(self.model.time)

    def handle_start_toggle(self):
        if self.model.is_running:
            self.pause()
        else:
            self.start()
    
    def handle_end(self):
        self.timer.stop()
        self.face_controller.stop()

        self.model.is_running = False
        self.model.time = 0
        self.sync_view()

    def start(self):
        self.model.is_running = True
        self.timer.start()

        self.face_controller.start()

        # Tell the view to update the button text
        self.view.set_running(True)

    def pause(self):
        self.model.is_running = False
        self.timer.stop()

        self.face_controller.stop()

        # Update the view
        self.view.set_running(False)

    def tick(self):
        """
        Called once per second while the timer is running.
        """
        # Increase remaining time
        self.model.time += 1

        # Update the time display
        self.view.update_time(self.model.time)
        


