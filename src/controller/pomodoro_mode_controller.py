from PySide6.QtCore import QTimer

from controller.facial_imaging_controller import FacialImagingController
from gui.pomodoro_settings_dialog import PomodoroSettingsDialog
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
        self.view.home_button.clicked.connect(self.handle_end)
        self.view.settings_clicked.connect(self.open_settings)
        self.view.mode_changed.connect(self.change_mode)
        self.view.skip_button.clicked.connect(self.handle_skip)

        self.sync_view()
    
    def sync_view(self):
        self.view.update_controls(self.model.is_running, self.model.has_started)
        self.view.update_time(self.model.remaining_time)

    def change_mode(self, mode):
        # Stop any running timer
        self.timer.stop()
        self.face_controller.stop()


        self.model.is_running = False
        self.model.mode = mode

        self.reset_current_mode()

        self.view.set_mode(mode)
        self.view.update_controls(self.model.is_running, self.model.has_started)

    def handle_start_toggle(self):
        if self.model.is_running:
            self.pause()
        else:
            self.start()

    def handle_end(self):
        self.timer.stop()
        self.face_controller.stop()
        
        # Show notification
        mode_name = "Focus" if self.model.mode == "work" else "Break"
        self.notification_manager.show_notification(
            "Session Ended",
            f"Pomodoro {mode_name.lower()} session completed!"
        )

        self.model.is_running = False
        self.model.has_started = False
        self.reset_current_mode()
        self.sync_view()

    def start(self):
        self.model.is_running = True
        self.model.has_started = True
        self.timer.start()

        self.face_controller.start()
        
        # Show notification
        mode_name = "Focus" if self.model.mode == "work" else "Break"
        self.notification_manager.show_notification(
            f"Pomodoro {mode_name} Started",
            f"Your {mode_name.lower()} session has begun!"
        )

        # Tell the view to update the button text
        self.view.update_controls(self.model.is_running, self.model.has_started)

    def pause(self):
        self.model.is_running = False
        self.timer.stop()
        
        self.face_controller.stop()
        
        # Show notification
        mode_name = "Focus" if self.model.mode == "work" else "Break"
        self.notification_manager.show_notification(
            f"Pomodoro {mode_name} Paused",
            f"Your {mode_name.lower()} session has been paused."
        )

        # Update the view
        self.view.update_controls(self.model.is_running, self.model.has_started)

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
            self.view.update_controls(self.model.is_running, self.model.has_started)
            
            # Show notification when timer completes
            mode_name = "Focus" if self.model.mode == "work" else "Break"
            self.notification_manager.show_notification(
                f"Pomodoro {mode_name} Complete",
                f"Your {mode_name.lower()} session is finished!"
            )
    



    def open_settings(self):
        dialog = PomodoroSettingsDialog(
            work=self.model.modes["work"] // 60,
            break_time =self.model.modes["break"] // 60
        )
        if dialog.exec():
            # Stop running timer
            self.timer.stop()
            self.model.is_running = False

            # Save settings
            self.model.modes["work"] = dialog.work_spin.value() * 60
            self.model.modes["break"] = dialog.break_spin.value() * 60

            # Reset to current mode
            self.reset_current_mode()

            self.view.update_controls(self.model.is_running, self.model.has_started)

    def reset_current_mode(self):
        if self.model.mode == "work":
            self.model.remaining_time = self.model.modes["work"]
        else:
            self.model.remaining_time = self.model.modes["break"]

        self.view.update_time(self.model.remaining_time)
    
    def handle_skip(self):
        self.timer.stop()
        self.face_controller.stop()

        # Toggle mode
        next_mode = "break" if self.model.mode == "work" else "work"
        self.model.mode = next_mode

        # Reset time for new mode
        self.reset_current_mode()

        # Update state
        self.model.is_running = False
        self.model.has_started = False
        self.view.set_mode(next_mode)
        self.view.update_controls(self.model.is_running, self.model.has_started)
