"""
Notification utility for sending system notifications using PySide6
"""
from PySide6.QtWidgets import QSystemTrayIcon, QApplication
from PySide6.QtGui import QIcon
import subprocess
import platform


class NotificationManager:
    """
    Manages system notifications using QSystemTrayIcon
    """
    def __init__(self):
        self.app = QApplication.instance()
        self.tray_icon = None
        self._setup_tray_icon()
    
    def _setup_tray_icon(self):
        """Initialize the system tray icon"""
        if self.app is None:
            return
            
        # Create a system tray icon
        self.tray_icon = QSystemTrayIcon(self.app)
        
        # Set an icon if you have one (optional)
        # icon = QIcon("path/to/your/icon.png")
        # self.tray_icon.setIcon(icon)
        
        # Make the tray icon visible
        self.tray_icon.setVisible(True)
    
    def _play_sound(self):
        """Play an alarm notification sound"""
        try:
            if platform.system() == "Darwin":  # macOS
                # Play an alarm-like system sound on macOS (non-blocking)
                subprocess.Popen(["afplay", "/System/Library/Sounds/Funk.aiff"], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            else:
                # For other platforms, use system beep
                print("\a")  # ASCII bell character
        except Exception as e:
            print(f"Could not play notification sound: {e}")
    
    def show_notification(self, title, message, duration=3000):
        """
        Show a system notification with sound
        
        Args:
            title (str): Notification title
            message (str): Notification message
            duration (int): Duration in milliseconds (default: 3000ms = 3s)
        """
        # Play notification sound
        self._play_sound()
        
        if self.tray_icon and self.tray_icon.isSystemTrayAvailable():
            self.tray_icon.showMessage(
                title,
                message,
                QSystemTrayIcon.MessageIcon.Information,
                duration
            )
        else:
            print(f"System tray not available. Notification: {title} - {message}")
