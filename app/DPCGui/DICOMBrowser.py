from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSplitter, QHBoxLayout, QFileSystemModel, QTreeView, QVBoxLayout, QPushButton
from app.DPCGui.ImageWidget import ImageWidget

class DICOMBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 650
        self.leftPanelWidth = 250
        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.imageView = ImageWidget()

        self.filesModel = self.__initFilesModel()
        self.filesView = self.__initFilesView(self.filesModel)
        self.filesView.doubleClicked.connect(self.load_image)

        self.resetBtn = QPushButton('Reset browser')
        self.resetBtn.clicked.connect(self.resetBrowser)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.filesView)
        splitter.addWidget(self.imageView)

        middleLayout = QHBoxLayout()
        middleLayout.addWidget(splitter)

        layout = QVBoxLayout(self)
        layout.addLayout(middleLayout)
        layout.addWidget(self.resetBtn)

    def load_image(self, index):
        path = self.filesModel.filePath(index)
        self.imageView.set_image(path)

    def updatModel(self,path):
        self.filesModel.setRootPath(path)
        self.filesView.setRootIndex(self.filesModel.index(path))

    def resetBrowser(self):
        self.filesModel.setRootPath('C:/')
        self.filesView.setRootIndex(self.filesModel.index(str(self.filesModel.rootDirectory())))
        self.filesView.update()
        self.imageView.resetImage()

    def __initFilesView(self, model: QFileSystemModel):
        view = QTreeView()
        view.setEditTriggers(QTreeView.NoEditTriggers)
        view.hideColumn(1)
        view.hideColumn(3)
        view.setGeometry(0, 0, 10, 10)
        view.setModel(model)
        view.setRootIndex(model.index(str(model.rootDirectory())))

        return view

    def __initFilesModel(self):
        model = QFileSystemModel()
        model.setReadOnly(True)
        model.setRootPath('C:/')

        return model