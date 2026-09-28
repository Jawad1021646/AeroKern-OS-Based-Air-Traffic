import sys
import os
from PyQt6.QtWidgets import QApplication
from gui.dashboard import Dashboard

# Ensure project root is in sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def main():
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
