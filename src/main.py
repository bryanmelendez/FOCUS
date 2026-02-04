import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from model.focus_mode_model import FocusModel
from src.model.free_mode_model import FreeModeModel
from src.controller.focus_mode_controller import FocusController
from src.controller.free_mode_controller import FreeModeController
from PySide6.QtGui import QFontDatabase

import sys

app = QApplication(sys.argv)

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