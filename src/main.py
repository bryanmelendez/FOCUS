import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui import GUI

if __name__ == "__main__":
    print("Starting app")

    app = GUI()

    app.start_gui()