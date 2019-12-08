from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout


class ButtonsBarWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent=parent)
        self.setMaximumHeight(60)

        self.initUI()

    def initUI(self):
        self.pacs_btn = self.__initButton('PACS Module')
        self.dcm_btn = self.__initButton('Dicom Browser')

        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.pacs_btn)
        layout.addWidget(self.dcm_btn)

    def __initButton(self, text :str):
        button = QPushButton(text)
        button.setMaximumWidth(200)
        button.setMinimumHeight(50)

        return button