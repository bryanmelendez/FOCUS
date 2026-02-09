from utils.logger import Logger
from controller.stats_window_controller import StatsWindowController
from model.stats_window_model import StatsWindowModel
from csv_logger import CSV_Logger

from model.history_model import HistoryModel

class HistoryController:
    def __init__(self) -> None:
        model = HistoryModel()

    def write_session(self):
        # this is a wrapper for the write_session function in the other class
        pass

    def get_sessions(self):
        # this is a wrapper for the other function
        pass
    
    def show_stats(self, session):
        
        # Get the model based on session
        model = self.model.csv_logger.get_session(session)

        controller = StatsWindowController(model, parent = None)
        controller.show()
