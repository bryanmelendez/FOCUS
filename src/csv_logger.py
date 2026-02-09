import csv
import os
from datetime import datetime

from model.stats_window_model import StatsWindowModel

class CSV_Logger:
    def __init__(self) -> None:
        self.filename = "past_sessions"
        self.headers = ['timestamp', 
                   'total_time', 
                   'attentive_percentage', 
                   'inattentive_percentage',
                   'attentive_time',
                   'inattentive_time',
                   'inattentive_count',
                   'qualitative_label'] 
        
    def write_session(self, model: StatsWindowModel):
        data = list()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data.append(timestamp)
        data.append(model.total_time)
        data.append(model.attentive_percentage)
        data.append(model.inattentive_percentage)
        data.append(model.attentive_time)
        data.append(model.inattentive_time)
        data.append(model.inattentive_count)
        data.append(model.qualitative_label)

        # Check if file exists
        file_exists = os.path.isfile(self.filename)
        
        # Open in append mode if exists, write mode if new
        mode = 'a' if file_exists else 'w'
        
        with open(self.filename, mode, newline='') as file:
            writer = csv.writer(file)
            
            # Write headers only if file is new
            if not file_exists:
                writer.writerow(self.headers)
            
            # Write data row
            writer.writerow(data)


    def read_sessions(self) -> list:
        sessions_list = []

        with open(self.filename, 'r', newline='') as file:
            session = dict()
            reader = csv.DictReader(file)
            for row in reader:
                timestamp = row['timestamp']
                session[timestamp] = dict(row)

                sessions_list.append(session)

        return sessions_list

    def get_session(self, session: dict) -> StatsWindowModel:
        model = StatsWindowModel(
                session['total_time'],
                session['attentive_percentage'],
                session['inattentive_percentage'],
                session['attentive_time'],
                session['inattentive_time'],
                session['inattentive_count'],
                session['qualitative_label']
            )

        return model