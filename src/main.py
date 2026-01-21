import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.main_window import MainWindow
from controller.app_controller import AppController

if __name__ == "__main__":
    print("Starting app")

    app_controller = AppController()

    app = MainWindow(app_controller)

    app.start_gui()