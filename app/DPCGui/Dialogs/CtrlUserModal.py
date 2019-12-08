from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QListView, QPushButton, QDialogButtonBox, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QAbstractItemView
from app.DPCGui.Dialogs.AddUserDialog import AddUserDialog
from app.DPCModel.UsersListModel import UsersListModel
import app.DPCModel.DatabaseModel as db

class CtrlUserWidget(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self,parent=parent)

        self.model = UsersListModel()
        self.model.update(db.load_users())
        self.setModal(True)
        self.setWindowTitle('Users')
        self.initUI()

    def initUI(self):
        self.addBtn = QPushButton('Add user')
        self.addBtn.setIcon(QIcon('res/img/icons/plus_32.png'))
        self.editBtn = QPushButton('Edit user')
        self.editBtn.setIcon(QIcon('res/img/icons/edit_32.png'))
        self.editBtn.setDisabled(True)
        self.delBtn = QPushButton('Delete user')
        self.delBtn.setIcon(QIcon('res/img/icons/minus_32.png'))

        self.userView = QListView()
        self.userView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.userView.setGeometry(0,0,100,400)
        self.userView.setModel(self.model)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Save ,
            Qt.Horizontal, self)

        self.buttons.accepted.connect(self.accept)

        self.addBtn.clicked.connect(self.addUser)
        self.delBtn.clicked.connect(self.deleteUser)
        self.userView.doubleClicked.connect(self.activate_user)

        btnLayout = QVBoxLayout()
        btnLayout.addWidget(self.addBtn)
        btnLayout.addWidget(self.editBtn)
        btnLayout.addWidget(self.delBtn)

        upLayout = QHBoxLayout()
        upLayout.addWidget(self.userView)
        upLayout.addLayout(btnLayout)

        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(upLayout)
        mainLayout.addWidget(self.buttons)

    def showWidget(self, parent=None):
        dialog = CtrlUserWidget(parent)
        ok = dialog.exec_()
        return ok

    def addUser(self):
        dialog = AddUserDialog.getUser()
        if dialog:
            self.model.update(db.load_users())
            self.model.layoutChanged.emit()
            self._update_view()
        return True

    def _update_view(self):
        self.userView.setModel(self.model)

    def deleteUser(self):
        indexes = self.userView.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            db_response = db.del_user(self.model.data[index.row()][0])
            if db_response:
                del self.model.data[index.row()]
                self.model.layoutChanged.emit()
                # Clear the selection (as it is no longer valid).
                self.userView.clearSelection()
            else:
                QMessageBox.warning(self, 'User is active', 'User is active. Change active User before delete',
                                    QMessageBox.Ok)

    def activate_user(self):
        indexes = self.userView.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            db.set_active_user(self.model.data[index.row()][0])
            self.model.update(db.load_users())
            self.model.layoutChanged.emit()
        return True