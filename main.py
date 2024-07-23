# main.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from login_window import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    login = LoginWindow(main_window)
    login.show()
    sys.exit(app.exec_())
