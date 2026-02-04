from model.free_mode_model import FreeModeModel
from PySide6.QtCore import QTimer

from controller.facial_imaging_controller import FacialImagingController
from utils.notification import NotificationManager

class FreeModeController:
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
        self.view.end_clicked.connect(lambda: self.handle_end(show_stats=True))
        self.view.home_clicked.connect(self.handle_home)
        self.sync_view()
    
    def sync_view(self):
        self.view.set_running(self.model.is_running)
        self.view.update_time(self.model.time)

    def handle_start_toggle(self):
        if self.model.is_running:
            self.pause()
        else:
            self.start()
        
    def handle_home(self):
        """Handle home button click - end session if active, then let view emit home_clicked"""
        if self.model.has_started:
            # Session is active, end it without showing stats
            self.handle_end(show_stats=False)
        # View will emit home_clicked signal which MainWindow listens to
        
    def handle_end(self, show_stats=True):
        self.timer.stop()
        self.face_controller.stop()
        
        # Show notification
        self.notification_manager.show_notification(
            "Session Ended",
            "Focus session completed!"
        )

        self.model.is_running = False
        self.model.has_started = False
        self.model.time = 0
        self.sync_view()

        self.face_controller.end_session(show_stats=show_stats)

    def start(self):
        # Prevent starting if already running
        if self.model.is_running or self.face_controller.worker_thread.isRunning():
            return
            
        self.model.is_running = True
        self.model.has_started = True
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
        


