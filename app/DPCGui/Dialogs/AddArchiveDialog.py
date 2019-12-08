from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QLineEdit, QLabel
import app.DPCModel.DatabaseModel  as db

class AddArchiveDialog(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self,parent=parent)

        self.setModal(True)
        self.setWindowTitle('Add Users')

        self.initUI()

    def initUI(self):
        aecLabel = QLabel('AEC')
        self.aecText = QLineEdit()
        adresLabel = QLabel('Path')
        self.pathText = QLineEdit()
        portLabel = QLabel('Port ')
        self.portText = QLineEdit()
        descriptLabel = QLabel('Description')
        self.descriptText = QLineEdit()

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(aecLabel)
        mainLayout.addWidget(self.aecText)
        mainLayout.addWidget(adresLabel)
        mainLayout.addWidget(self.pathText)
        mainLayout.addWidget(portLabel)
        mainLayout.addWidget(self.portText)
        mainLayout.addWidget(descriptLabel)
        mainLayout.addWidget(self.descriptText)
        mainLayout.addWidget(self.buttons)

    @staticmethod
    def showAndAdd(parent = None):
        dialog = AddArchiveDialog(parent)
        ok = dialog.exec()
        if ok:
            db.add_archive(dialog.aecText.text(), dialog.pathText.text(), dialog.portText.text(), dialog.descriptText.text() )
            print('New user added to database.')
            return True
        else:
            return False