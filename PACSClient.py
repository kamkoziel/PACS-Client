# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtWidgets import QApplication
from app.DPCGui.MainWindow import App
from app.DPCModel.DatabaseModel import connectAndLoad

if __name__ == '__main__':
    app = QApplication(sys.argv)
    connectAndLoad()
    ex = App()
    sys.exit(app.exec_())