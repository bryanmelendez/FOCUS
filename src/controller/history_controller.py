import csv
import os
from datetime import datetime

from utils.logger import Logger
from controller.stats_window_controller import StatsWindowController
from model.stats_window_model import StatsWindowModel

class HistoryController:
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

        self.view = None

        self.logger = Logger()
    
    def show_stats(self, session):
        # Get the model based on session
        model = self.get_session(session)

        controller = StatsWindowController(model, parent = None)
        controller.show()

        
    def write_session(self, model: StatsWindowModel):
        self.logger.debug("Writing Session")

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
            self.logger.debug(f"Writing row: {data}")
            writer.writerow(data)


    def read_sessions(self) -> list:
        """Read all sessions from the CSV file"""
        sessions_list = []
        
        # Check if file exists
        if not os.path.isfile(self.filename):
            return sessions_list

        # Check if file has headers
        with open(self.filename, 'r', newline='') as file:
            first_line = file.readline().strip()
            if not first_line:
                return sessions_list
            
            # Check if the first line matches headers
            has_headers = first_line.startswith('timestamp')
        
        # If no headers, add them
        if not has_headers:
            with open(self.filename, 'r', newline='') as file:
                content = file.read()
            
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)
                file.write(content)
        
        # Now read the sessions
        with open(self.filename, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                timestamp = row['timestamp']
                # Create a NEW dict for each session (not reuse the same one)
                session = {timestamp: dict(row)}
                sessions_list.append(session)

        return sessions_list

    def get_session(self, session: dict) -> StatsWindowModel:
        """Convert a session dict to a StatsWindowModel"""
        # Parse time strings to tuples (hours, minutes, seconds)
        def parse_time(time_str):
            # Time is stored as tuple string like "(0, 0, 1)"
            if isinstance(time_str, str) and time_str.startswith('('):
                # Remove parentheses and split
                time_str = time_str.strip('()').replace(' ', '')
                parts = time_str.split(',')
                return tuple(int(p) for p in parts)
            elif isinstance(time_str, tuple):
                return time_str
            else:
                # Default fallback
                return (0, 0, 0)
        
        model = StatsWindowModel(
                parse_time(session['total_time']),
                float(session['attentive_percentage']),
                float(session['inattentive_percentage']),
                parse_time(session['attentive_time']),
                parse_time(session['inattentive_time']),
                int(session['inattentive_count']),
                session['qualitative_label']
            )

        return model