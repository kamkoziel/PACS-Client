from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QLineEdit, QLabel
from app.DPCModel.DatabaseModel import get_active_archive, add_user

class AddUserDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self,parent=parent)

        self.setModal(True)
        self.setWindowTitle('Add Users')

        self.initUI()

    def initUI(self):
        aecLabel = QLabel('AEC')
        self.aecText = QLineEdit()
        adresLabel = QLabel('IP Adress')
        self.adresText = QLineEdit()
        portLabel = QLabel('Port for Archive')
        self.portText = QLineEdit()

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(aecLabel)
        mainLayout.addWidget(self.aecText)
        mainLayout.addWidget(adresLabel)
        mainLayout.addWidget(self.adresText)
        mainLayout.addWidget(portLabel)
        mainLayout.addWidget(self.portText)
        mainLayout.addWidget(self.buttons)

    @staticmethod
    def getUser(parent = None):
        dialog = AddUserDialog(parent)
        ok = dialog.exec()
        if ok:
            print('Before get active archive')
            archive = get_active_archive()
            print(archive)
            print('Archive is ready...')
            add_user(dialog.aecText.text(), dialog.adresText.text(), dialog.portText.text())
            print('New user added to database.')
            return True
        else:
            return False