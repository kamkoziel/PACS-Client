from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import  QWidget, QLabel, QHBoxLayout, QVBoxLayout,  QDockWidget, QMessageBox


from app.DPCGui.ButtonsBarWidget import ButtonsBarWidget
from app.DPCGui.DICOMBrowser import DICOMBrowser
import app.DPCModel.DatabaseModel as db
from app.DPCGui.PACSWidget import PACSWidget

from app.DPCCtrl.PACS_Action import PACS_Action

class MainWidget(QWidget):
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
        self.archive_label = self.__initArchiveLabel()
        self.user_label = self.__initUserLabel()
        self.button_bar = self.__initBtnBar()

        self.pacs_widget = PACSWidget()
        self.dicom_widget = DICOMBrowser()

        self.connect_ctrl = self.__initCtrlIcon()
        self.updateConnectCtrl()

        labelsLayout = QHBoxLayout()
        labelsLayout.addWidget(self.archive_label)
        labelsLayout.addWidget(self.user_label)
        labelsLayout.addWidget(self.connect_ctrl)

        self.mainWidget=QDockWidget()
        self.mainWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.mainWidget.setTitleBarWidget(QWidget())
        self.mainWidget.setWidget(self.dicom_widget)

        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(labelsLayout)
        mainLayout.addWidget(self.button_bar)
        mainLayout.addWidget(self.mainWidget)

    def show_PACSWidget(self):
        connect = PACS_Action.isConnect()
        if connect:
            self.mainWidget.setWidget(self.pacs_widget)
            self.pacs_widget.pacs_view.communicate.showImage.connect(self.img_to_browser)
            self.button_bar.pacs_btn.setDisabled(1)
            self.button_bar.dcm_btn.setDisabled(0)
        else:
            QMessageBox.warning(
                    self, 'Connect Error',
                    '''Application is not able to connect with PACS Server 
                     
        Check Klient and Archive data ''', QMessageBox.Ok)

    def show_DICOMBrowser(self):
        self.mainWidget.setWidget(self.dicom_widget)
        self.button_bar.dcm_btn.setDisabled(1)
        self.button_bar.pacs_btn.setDisabled(0)

    def updateConnectCtrl(self):
        isConnect = PACS_Action.isConnect()
        if isConnect:
            self.connect_icon = QPixmap('res/img/icons/isConnect_64.png')
            self.connect_ctrl.setPixmap(self.connect_icon)
        else:
            self.connect_icon = QPixmap('res/img/icons/noConnect_64.png')
            self.connect_ctrl.setPixmap(self.connect_icon)

    def __initArchiveLabel(self):
        archive_label =  QLabel('''Active Archive:
                            AEC:      {0}
                            Path:   {2}
                            Port:      {1}'''.format(str(db.get_active_archive()[1]),
                                                    str(db.get_active_archive()[2]),
                                                    str(db.get_active_archive()[3])))

        archive_label.setMaximumHeight(60)

        return archive_label

    def __initUserLabel(self):
        user_label =  QLabel('''Active User:
                        AET:      {0}
                        Adres IP:   {1}
                        Port:      {2}'''.format(str(db.get_active_user()[1]),
                                                str(db.get_active_user()[2]),
                                                str(db.get_active_user()[3])))
        user_label.setMaximumHeight(60)

        return user_label

    def __initCtrlIcon(self):
        connect_ctrl = QLabel()
        return connect_ctrl

    def __initBtnBar(self):
        button_bar = ButtonsBarWidget()
        button_bar.pacs_btn.clicked.connect(self.show_PACSWidget)
        button_bar.dcm_btn.clicked.connect(self.show_DICOMBrowser)
        button_bar.dcm_btn.setDisabled(1)

        return button_bar

    def updateArchiveLabel(self):
        self.archive_label.setText('''Active Archive:
                                AEC:      {0}
                                Path:   {2}
                                Port:      {1}'''.format(str(db.get_active_archive()[1]),
                                                         str(db.get_active_archive()[2]),
                                                         str(db.get_active_archive()[3])))

    def updateUserLabel(self):
        self.user_label.setText('''Active User:
                        AET:      {0}
                        Adres IP:   {1}
                        Port:      {2}'''.format(str(db.get_active_user()[1]),
                                                str(db.get_active_user()[2]),
                                                str(db.get_active_user()[3])))

    @pyqtSlot()
    def img_to_browser(self):
        self.mainWidget.setWidget(self.dicom_widget)
        self.dicom_widget.updatModel(str(self.pacs_widget.pacs_view.activeImage))
        self.button_bar.dcm_btn.setDisabled(1)
        self.button_bar.pacs_btn.setDisabled(0)