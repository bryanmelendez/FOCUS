from PySide6.QtWidgets import QMainWindow, QStackedWidget
from src.gui.focus_view import FocusView
from gui.free_mode_view import FreeTimerView
from src.gui.history_view import HistoryView
from gui.home_window import HomePage  # import your new home page widget

class MainWindow(QMainWindow):
    def __init__(self, app_controller):
        super().__init__()
        self.controller = app_controller

        self.setWindowTitle("FOCUS")

        self.home_page = HomePage()
        self.focus_view = FocusView()
        self.free_view = FreeTimerView()
        self.history_view = HistoryView()

        self.stacked = QStackedWidget()
        self.stacked.setStyleSheet("background-color: #262836;")

        self.stacked.addWidget(self.home_page)   # index 0
        self.stacked.addWidget(self.focus_view)  # index 1
        self.stacked.addWidget(self.free_view)   # index 2
        self.stacked.addWidget(self.history_view)

        self.setCentralWidget(self.stacked)
        

        self.resize(1000, 600)

        # Connect button click to switch view
        self.home_page.focus_button.clicked.connect(self.show_focus)
        self.home_page.free_button.clicked.connect(self.show_free)
        self.home_page.history_button.clicked.connect(self.show_history)
        self.free_view.home_clicked.connect(self.show_home)
        self.focus_view.home_clicked.connect(self.show_home)
        self.history_view.home_clicked.connect(self.show_home)

    def show_home(self):
        self.stacked.setCurrentIndex(0)  # Show HomePage

    def show_focus(self):
        self.stacked.setCurrentIndex(1)  # Show FocusView

    def show_free(self):
        self.stacked.setCurrentIndex(2)  # Show FreeTimerView
    
    def show_history(self):
        self.stacked.setCurrentIndex(3) # Show HistoryView
