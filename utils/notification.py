"""
Notification utility for sending system notifications using PySide6
"""
from PySide6.QtWidgets import QSystemTrayIcon, QApplication
from PySide6.QtGui import QIcon


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
    
    def show_notification(self, title, message, duration=3000):
        """
        Show a system notification
        
        Args:
            title (str): Notification title
            message (str): Notification message
            duration (int): Duration in milliseconds (default: 3000ms = 3s)
        """
        if self.tray_icon and self.tray_icon.isSystemTrayAvailable():
            self.tray_icon.showMessage(
                title,
                message,
                QSystemTrayIcon.MessageIcon.Information,
                duration
            )
        else:
            print(f"System tray not available. Notification: {title} - {message}")
