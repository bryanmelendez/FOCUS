from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
import sys

app = QApplication(sys.argv)

main_window = MainWindow(app_controller=None)
main_window.show()

app.exec()