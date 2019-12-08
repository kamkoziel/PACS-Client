from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QAction, qApp
from app.DPCGui.Dialogs.CtrlUserModal import CtrlUserWidget
from app.DPCGui.Dialogs.CtrlArchiveModal import CtrlArchiveModal
from app.DPCGui.MainWidget import MainWidget

class MenuBar(QMenuBar):
    def __init__(self, mainWidget : MainWidget ):
        QMenuBar.__init__(self)
        self.main_widget = mainWidget

        fileMenu = self.addMenu('&File')
        ctrlMenu = self.addMenu('Controls')
        helpMenu = self.addAction('Help')

        fileMenu.addAction(self.properties())
        fileMenu.addAction(self.exit())

        ctrlMenu.addAction(self.UserAction())
        ctrlMenu.addAction(self.ArchiveAction())

    def exit(self):
        act = QAction(QIcon('exit.png'), '&Exit', self)
        act.setShortcut('Ctrl+Q')
        act.setStatusTip('Exit application')
        act.triggered.connect(qApp.quit)

        return act

    def properties(self):
        act = QAction(QIcon('exit.png'), 'Properties', self)
        act.setStatusTip('Set connecting and other properties')
        act.setDisabled(True)

        return act

    def UserAction(self):
        act = QAction(QIcon('exit.png'), 'Show Users ', self)
        act.setStatusTip('Show widget controlling avaliable users')
        act.setShortcut('Ctrl+U')
        act.triggered.connect(self.showCtrlUser)
        return act

    def ArchiveAction(self):
        act = QAction(QIcon('exit.png'), 'Show Archives ', self)
        act.setStatusTip('Show widget controlling avaliable archives')
        act.setShortcut('Ctrl+U')
        act.triggered.connect(self.showCtrlArchive)
        return act

    def showCtrlArchive(self):
        ok = CtrlArchiveModal(self )
        ok.showWidget()
        if ok:
            self.main_widget.updateArchiveLabel()
            self.main_widget.updateConnectCtrl()
            print("Archive modal close successful")
            return
        else:
            print("Archive modal close wrong")
            return

    def showCtrlUser(self):
        ok = CtrlUserWidget(self)
        ok.showWidget()
        if ok:
            self.main_widget.updateUserLabel()
            self.main_widget.updateConnectCtrl()
            print("User modal close successful")
            return
        else:
            print("User modal close wrong")
            return


