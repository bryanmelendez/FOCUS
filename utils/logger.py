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
        pass

    def log(self, message, color=None):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # terminal output
        colored_message = f"{self.COLORS[color]}{message}{self.COLORS['RESET']}" if color else message

        print(f"[{timestamp}] {colored_message}")

    def info(self, message):
        self.log(f"INFO: {message}", "GREEN")

    def warning(self, message):
        self.log(f"WARNING: {message}", "YELLOW")

    def error(self, message):
        self.log(f"ERROR: {message}", "RED")

    def debug(self, message):
        self.log(f"DEBUG: {message}", "BLUE")
