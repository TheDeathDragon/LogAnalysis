import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication

import Component.MainWindow as MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Microsoft YaHei UI", 10)
    app.setFont(font)
    window = MainWindow.MainWindow()
    window.show()
    sys.exit(app.exec_())
