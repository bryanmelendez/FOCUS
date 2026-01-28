from PySide6.QtCore import QTimer

from controller.facial_imaging_controller import FacialImagingController
from utils.notification import NotificationManager

class PomodoroController:
    def __init__(self, model, view):
        self.face_controller = FacialImagingController()
        self.notification_manager = NotificationManager()
        
        # Store references to model and view
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
        self.view.mode_changed.connect(self.change_mode)    

        self.sync_view()
    
    def sync_view(self):
        self.view.set_running(self.model.is_running)
        self.view.update_time(self.model.remaining_time)

    def handle_start_toggle(self):
        if self.model.is_running:
            self.pause()
        else:
            self.start()

    def handle_end(self):
        self.timer.stop()

        self.face_controller.stop()
        
        # Show notification
        mode_name = "Focus" if self.model.current_mode == "focus" else "Break"
        self.notification_manager.show_notification(
            "Session Ended",
            f"Pomodoro {mode_name.lower()} session completed!"
        )

        self.model.is_running = False
        self.model.remaining_time = self.model.modes[self.model.current_mode]
        self.sync_view()

    def start(self):
        self.model.is_running = True
        self.timer.start()

        self.face_controller.start()
        
        # Show notification
        mode_name = "Focus" if self.model.current_mode == "focus" else "Break"
        self.notification_manager.show_notification(
            f"Pomodoro {mode_name} Started",
            f"Your {mode_name.lower()} session has begun!"
        )

        # Tell the view to update the button text
        self.view.set_running(True)

    def pause(self):
        self.model.is_running = False
        self.timer.stop()
        
        self.face_controller.stop()
        
        # Show notification
        mode_name = "Focus" if self.model.current_mode == "focus" else "Break"
        self.notification_manager.show_notification(
            f"Pomodoro {mode_name} Paused",
            f"Your {mode_name.lower()} session has been paused."
        )

        # Update the view
        self.view.set_running(False)

    def tick(self):
        """
        Called once per second while the timer is running.
        """

        # Decrease remaining time
        self.model.remaining_time -= 1

        # Update the time display
        self.view.update_time(self.model.remaining_time)

        # Stop when time reaches zero
        if self.model.remaining_time <= 0:
            self.timer.stop()
            self.model.is_running = False
            self.view.set_running(False)
            
            # Show notification when timer completes
            mode_name = "Focus" if self.model.current_mode == "focus" else "Break"
            self.notification_manager.show_notification(
                f"Pomodoro {mode_name} Complete",
                f"Your {mode_name.lower()} session is finished!"
            )
        
    def change_mode(self, mode: str):
         self.timer.stop()
         self.model.set_mode(mode)
         self.sync_view()
