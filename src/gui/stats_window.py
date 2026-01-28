from PySide6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QProgressBar, QWidget, QGridLayout
)
from PySide6.QtCore import Qt

class StatsWindow(QDialog):
    def __init__(self, total_time, attentive_percentage, inattentive_percentage, attentive_time, inattentive_time, inattentive_count, qualitative_label, parent=None):
        super().__init__()
        self.setWindowTitle("Session Summary")
        self.setFixedSize(600, 350)

        layout = QVBoxLayout(self)
        layout.addSpacing(10)
        # qualitative label
        label = QLabel(qualitative_label)
        label.setAlignment(Qt.AlignCenter)
        label_color = self.label_color(attentive_percentage)
        label.setStyleSheet(f"""font-size: 30px; font-weight: bold; color: {label_color};""")
        layout.addWidget(label)

        layout.addSpacing(10)

        # percentages
        attentive_bar = QProgressBar()
        attentive_bar.setValue(int(attentive_percentage))
        attentive_bar.setFormat("Attentive %p%")
        attentive_bar.setStyleSheet("""QProgressBar::chunk { background-color: #4CAF50; }""")

        inattentive_bar = QProgressBar()
        inattentive_bar.setValue(int(inattentive_percentage))
        inattentive_bar.setFormat("Inattentive %p%")
        inattentive_bar.setStyleSheet("""QProgressBar::chunk { background-color: #F44336; }""")

        layout.addWidget(attentive_bar)
        layout.addWidget(inattentive_bar)

        layout.addSpacing(10)
        # stats
        # stats_layout = QVBoxLayout()
        # stats_layout.setAlignment(Qt.AlignCenter)

        # stats_layout.addWidget(QLabel(f"Total Time Monitored: Hours: {total_time[0]}, Minutes: {total_time[1]}, Seconds: {total_time[2]}"))
        # # stats_layout.addWidget(QLabel(f"Attentive Percentage: {attentive_percentage:.2f}%"))
        # # stats_layout.addWidget(QLabel(f"Inattentive Percentage: {inattentive_percentage:.2f}%"))
       
        # stats_layout.addWidget(QLabel(f"Attentive Time: Hours: {attentive_time[0]}, Minutes: {attentive_time[1]}, Seconds: {attentive_time[2]}"))
        # stats_layout.addWidget(QLabel(f"Inattentive Time: Hours: {inattentive_time[0]}, Minutes: {inattentive_time[1]}, Seconds: {inattentive_time[2]}"))
        # # inattentive count
        # stats_layout.addWidget(QLabel(f"Inattentive Count: {inattentive_count}"))

        stats_grid = QGridLayout()
        stats_grid.setSpacing(12)

        stats_grid.addWidget(self.draw_box("Total Time", f"{total_time[0]}h {total_time[1]}m {total_time[2]}s"), 0, 0)

        # stats_grid.addWidget(self.draw_box("Attentive %", f"{attentive_percentage:.2f}%"), 0, 1)

        # stats_grid.addWidget(self.draw_box("Inattentive %", f"{inattentive_percentage:.2f}%"), 0, 2)

        stats_grid.addWidget(self.draw_box("Attentive Time", f"{attentive_time[0]}h {attentive_time[1]}m {attentive_time[2]}s"), 0, 1)

        stats_grid.addWidget(self.draw_box("Inattentive Time", f"{inattentive_time[0]}h {inattentive_time[1]}m {inattentive_time[2]}s"), 0, 2)

        stats_grid.addWidget(self.draw_box("Inattentive Count", str(inattentive_count)), 1, 1)

        layout.addLayout(stats_grid)


        # layout.addLayout(stats_layout)

    def label_color(self, attentive_pct):
        if attentive_pct >= 90:
            return "#2E7D32"  # green
        elif attentive_pct >= 75:
            return "#F9A825"  # amber
        else:
            return "#C62828"  # red"

    def draw_box(self, title: str, value: str):
        box = QWidget()
        layout = QVBoxLayout(box)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")

        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("font-size: 16px; color: #FFFFFF;")

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        # box.setStyleSheet("""
        #     QWidget {
        #         border: 1px solid #FFFFFF;
        #         border-radius: 8px;
        #         padding: 5px;
        #         background-color: #00000;
        #     }
        # """)

        return box

