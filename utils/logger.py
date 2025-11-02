from datetime import datetime
import os

class Logger:
    # ANSI color codes
    COLORS = {
        'RESET': '\033[0m',
        'RED': '\033[91m',
        'YELLOW': '\033[93m',
        'GREEN': '\033[92m',
        'BLUE': '\033[94m'
    }

    def __init__(self):
        if not os.path.exists('logs'):
            os.makedirs('logs')

        self.log_file = f"logs/{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_execution.log"
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def log(self, message, color=None):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # terminal output
        colored_message = f"{self.COLORS[color]}{message}{self.COLORS['RESET']}" if color else message
        # log output
        log_entry = f"[{timestamp}] {message}\n"

        print(f"[{timestamp}] {colored_message}")

        with open(self.log_file, 'a') as f:
            f.write(log_entry)

    def info(self, message):
        self.log(f"INFO: {message}", "GREEN")

    def warning(self, message):
        self.log(f"WARNING: {message}", "YELLOW")

    def error(self, message):
        self.log(f"ERROR: {message}", "RED")

    def debug(self, message):
        self.log(f"DEBUG: {message}", "BLUE")
