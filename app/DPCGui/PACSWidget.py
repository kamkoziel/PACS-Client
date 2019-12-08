from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QFileSystemModel, QTreeView, QMessageBox, QAbstractScrollArea, QHeaderView
from PyQt5.QtWidgets import QHBoxLayout, QSplitter
from app.DPCCtrl.PACS_Action import *
from app.DPCGui.PACSView import PACSView
from app.DPCModel.PacsItemsModel import PacsItemModel


class PACSWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 650
        self.leftPanelWidth = 250
        self.imageToView = pyqtSignal()


        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.model = QFileSystemModel()
        self.model.setRootPath(r'C:\dcmtk')
        self.model.setReadOnly(True)

        self.files_view = self.__initFileTreeView(self.model)
        self.files_view.doubleClicked.connect(self.storeItem)

        self.pacs_model = PacsItemModel(["ID", "Name", "Birth"])

        if PACS_Action.isConnect():
            try:
                patients = PACS_Action.find_patients()
                self.pacs_model.update(patients)
            except:
                print('Error on loading patients list')

        self.pacs_view = PACSView()
        self.pacs_view.setModel(self.pacs_model)
        self.pacs_view.setMinimumWidth(200)
        self.pacs_view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.pacs_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.pacs_view.resizeColumnsToContents()
        self.pacs_view.doubleClicked.connect(self.showImage)

        splitter = QSplitter()
        splitter.addWidget(self.files_view)
        splitter.addWidget(self.pacs_view)

        layout = QHBoxLayout()
        layout.addWidget(splitter)

        self.setLayout(layout)

    def storeItem(self, index):
        path = self.model.filePath(index)
        response = PACS_Action.storeDICOM(str(path))
        if response:
            self.pacs_model.update(PACS_Action.find_patients())
            self.pacs_model.layoutChanged.emit()
            self.pacs_view.setModel(self.pacs_model)
            QMessageBox.information(self,
                                 'Store Success',
                                 'File {0} stored succesful to PACS'.format(str(path)),
                                 QMessageBox.Ok)

            return response
        else:
            QMessageBox.critical(self,
                                    'Store failed',
                                    'File {0} is not stored to PACS'.format(str(path)),
                                    QMessageBox.Ok)
            return response

    def showImage(self):
        path =self.pacs_view.get_path_image()

    def __initFileTreeView(self, model):
        treeView = QTreeView()
        treeView.setModel(model)
        treeView.setRootIndex(model.index(r'C:'))
        treeView.hideColumn(1)
        treeView.hideColumn(3)
        treeView.setAnimated(True)
        treeView.setIndentation(20)
        treeView.setSortingEnabled(True)
        treeView.setMinimumWidth(100)

        return treeView

    def updataPatients(self):
        if PACS_Action.isConnect():
            try:
                patients = PACS_Action.find_patients()
                self.pacs_model.update(patients)
                self.pacs_view.update()
            except:
                print('Error on loading patients list')

