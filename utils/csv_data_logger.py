# Class for writing algorithm outputs to CSV file
import csv
from datetime import datetime

class CSVDataLogger:
    def __init__(self):
        self.filename = f"logs/{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}/data_log.csv"  # TODO make this OS.join
        self.fieldnames = ['image_path', ] # TODO finish this 
        # Create CSV file and write header
        with open(self.filename, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()

    def log(self, data):
        # Write a row of data to the CSV file
        with open(self.filename, mode='a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writerow(data)