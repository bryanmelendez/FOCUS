from model.regular_mode_model import RegularModeModel
from PySide6.QtCore import QTimer

from controller.facial_imaging_controller import FacialImagingController
from utils.notification import NotificationManager

class RegularModeController:
    def __init__(self, model, view):
        self.face_controller = FacialImagingController()
        self.notification_manager = NotificationManager()

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
        self.view.home_button.clicked.connect(self.handle_end)
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
        
        # Show notification
        self.notification_manager.show_notification(
            "Session Ended",
            "Focus session completed!"
        )

        self.model.is_running = False
        self.model.time = 0
        self.sync_view()

    def start(self):
        # Prevent starting if already running
        if self.model.is_running or self.face_controller.worker_thread.isRunning():
            return
            
        self.model.is_running = True
        self.timer.start()

        self.face_controller.start()
        
        # Show notification
        self.notification_manager.show_notification(
            "Focus Session Started",
            "Your focus session has begun. Stay concentrated!"
        )

        # Tell the view to update the button text
        self.view.set_running(True)

    def pause(self):
        self.model.is_running = False
        self.timer.stop()

        self.face_controller.stop()
        
        # Show notification
        self.notification_manager.show_notification(
            "Session Paused",
            "Your focus session has been paused."
        )

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
        


