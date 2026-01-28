from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from model.pomodoro_mode_model import PomodoroModel
from model.regular_mode_model import RegularModeModel
from controller.pomodoro_mode_controller import PomodoroController
from controller.regular_mode_controller import RegularModeController
import sys

app = QApplication(sys.argv)

# Create the MVC components
main_window = MainWindow(app_controller=None)

p_model = PomodoroModel()
p_view = main_window.pomodoro_view
p_controller = PomodoroController(p_model, p_view)

r_model = RegularModeModel()
r_view = main_window.regular_view
r_controller = RegularModeController(r_model, r_view)

main_window.show()

app.exec()