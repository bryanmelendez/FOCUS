import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from model.focus_mode_model import FocusModel
from src.model.free_mode_model import FreeModeModel
from src.controller.focus_mode_controller import FocusController
from src.controller.free_mode_controller import FreeModeController
from PySide6.QtGui import QFontDatabase, QIcon, QPixmap

import sys

app = QApplication(sys.argv)

# Get absolute path to the logo
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logo_path = os.path.join(base_dir, "assets", "focus_logo.png")

# Set the application icon
app_icon = QIcon(logo_path)
app.setWindowIcon(app_icon)

# For macOS dock icon
try:
    from Cocoa import NSApplication, NSImage
    ns_app = NSApplication.sharedApplication()
    logo_image = NSImage.alloc().initWithContentsOfFile_(logo_path)
    if logo_image:
        ns_app.setApplicationIconImage_(logo_image)
except ImportError:
    # Cocoa not available, icon will only show in window title bar
    pass
except Exception as e:
    print(f"Could not set dock icon: {e}")

# Create the MVC components
main_window = MainWindow(app_controller=None)

p_model = FocusModel()
p_view = main_window.focus_view
p_controller = FocusController(p_model, p_view)

r_model = FreeModeModel()
r_view = main_window.free_view
r_controller = FreeModeController(r_model, r_view)

main_window.show()

app.exec()