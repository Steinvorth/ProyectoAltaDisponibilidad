import sys
from PyQt5.QtWidgets import QApplication
from gui_handler import GUIHandler

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUIHandler()
    sys.exit(app.exec_())
