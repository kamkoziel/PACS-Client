from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow
from app.DPCGui.MainWidget import MainWidget
from app.DPCGui.Menu.MenuBar import MenuBar


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = 40
        self.top = 80
        self.width=800
        self.height=650
        self.title = 'Dicom PACS Client'

        self.initUI()

    def initUI(self):
        main_widget = MainWidget()
        menu_bar = MenuBar(main_widget)
        self.setWindowIcon(QtGui.QIcon('img/DPC.png'))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMenuBar(menu_bar)
        self.statusBar().showMessage('Ready')
        self.setCentralWidget(main_widget)


        self.show()

