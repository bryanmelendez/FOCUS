from model.stats_window_model import StatsWindowModel
from gui.stats_window_view import StatsWindowView

class StatsWindowController:
    def __init__(self, model, parent=None):
        self.model = model
        self.view = StatsWindowView(parent)
        self.populate_view()

    def populate_view(self):
        label_color = self.label_color(self.model.attentive_percentage)
        # title
        self.view.set_title(self.model.qualitative_label, label_color)
        # attentive/inattentive progress bars
        self.view.set_progress(self.model.attentive_percentage, self.model.inattentive_percentage)
        # stats
        self.view.add_stat_box("Total Time", self.format_time(self.model.total_time), 0, 0 )
        self.view.add_stat_box("Attentive Time", self.format_time(self.model.attentive_time), 0, 1 )
        self.view.add_stat_box("Inattentive Time", self.format_time(self.model.inattentive_time), 0, 2 )
        self.view.add_stat_box("Inattentive Count", str(self.model.inattentive_count), 1, 1 )

    def show(self):
        self.view.exec()

    def format_time(self, time):
        hours, minutes, seconds = time
        return f"{hours}h {minutes}m {seconds}s"

    def label_color(self, percentage):
        if percentage >= 90:
            return "#4CAF50"
        elif percentage >= 75:
            return "#F9A825"
        else:
            return "#F44336"