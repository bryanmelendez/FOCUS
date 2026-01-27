import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
import sys

app = QApplication(sys.argv)

main_window = MainWindow(app_controller=None)
main_window.show()

app.exec()