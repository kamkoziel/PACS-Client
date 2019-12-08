from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QTableView
from app.DPCCtrl.PACS_Action import PACS_Action


class WidgetsCommunications(QObject):
    showImage = pyqtSignal()

class PACSView(QTableView):
    def __init__(self, parent = None):
        QTableView.__init__(self, parent = parent)
        self.activeImage: str = None

        self.setEditTriggers(QTableView.NoEditTriggers)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.communicate = WidgetsCommunications()
        self.doubleClicked.connect(self.get_path_image)

    def getPathToLoadedImages(self):
        index = self.selectedIndexes()
        patient_id = self.model().itemData(index[0])
        dcm_path = PACS_Action.moveSeries(str(patient_id[0]))
        self.communicate.showImage.emit()
        return dcm_path

    def get_path_image(self):
        self.activeImage = self.getPathToLoadedImages()
        print(self.activeImage)
