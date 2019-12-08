from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QListView, QPushButton, QDialogButtonBox, QMessageBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QAbstractItemView
from PyQt5.QtGui import QIcon

from app.DPCGui.Dialogs.AddArchiveDialog import AddArchiveDialog
from app.DPCModel.ArchiveListModel import ArchiveListModel

import app.DPCModel.DatabaseModel as db

class CtrlArchiveModal(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self,parent=parent)

        self.model = ArchiveListModel()
        self.model.update(db.load_archives())
        self.setModal(True)
        self.setWindowTitle('Users')
        self.initUI()

    def initUI(self):
        self.addBtn = QPushButton('Add archive')
        self.addBtn.setIcon(QIcon('res/img/icons/plus_64.png'))
        self.editBtn = QPushButton('Edit archive')
        self.editBtn.setIcon(QIcon('res/img/icons/edit_32.png'))
        self.editBtn.setDisabled(True)
        self.delBtn = QPushButton('Delete archive')
        self.delBtn.setIcon(QIcon('res/img/icons/minus_32.png'))

        self.view = QListView()
        self.view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.view.setGeometry(0, 0, 100, 400)
        self.view.setModel(self.model)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Save,
            Qt.Horizontal, self)

        self.buttons.accepted.connect(self.accept)

        self.addBtn.clicked.connect(self.add_archive)
        self.delBtn.clicked.connect(self.delete_archive)
        self.view.doubleClicked.connect(self.set_active_archive)

        btnLayout = QVBoxLayout()
        btnLayout.addWidget(self.addBtn)
        btnLayout.addWidget(self.editBtn)
        btnLayout.addWidget(self.delBtn)

        upLayout = QHBoxLayout()
        upLayout.addWidget(self.view)
        upLayout.addLayout(btnLayout)

        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(upLayout)
        mainLayout.addWidget(self.buttons)

    def showWidget(self, parent=None):
        dialog = CtrlArchiveModal(parent)
        ok = dialog.exec_()
        return ok

    def add_archive(self):
        dialog = AddArchiveDialog.showAndAdd()
        if dialog:
            self.model.update(db.load_archives())
            self.model.layoutChanged.emit()
            self._update_view()
        return True

    def delete_archive(self):
        indexes = self.view.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            db_response = db.del_archive(self.model.data[index.row()][0])
            if db_response:
                del self.model.data[index.row()]
                self.model.layoutChanged.emit()
                # Clear the selection (as it is no longer valid).
                self.view.clearSelection()
            else:
                QMessageBox.warning(self, 'Archive is active', 'Archive is active. Change active archive before delete', QMessageBox.Ok)

    def set_active_archive(self):
        indexes = self.view.selectedIndexes()
        if indexes:
            # Indexes is a list of a single item in single-select mode.
            index = indexes[0]
            # Remove the item and refresh.
            db.set_active_archive(self.model.data[index.row()][0])
            self.model.update(db.load_archives())
            self.model.layoutChanged.emit()
        return True

    def _update_view(self):
        self.view.setModel(self.model)