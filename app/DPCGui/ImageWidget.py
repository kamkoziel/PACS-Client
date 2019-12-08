import imageio
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from app.DPCGui.ImageCanvas import ImageCanvas
import matplotlib.pyplot as plt
import pydicom


class ImageWidget(QWidget):
    def __init__(self,parent = None):
        QWidget.__init__(self, parent)
        self.initUI()

    def initUI(self):
        self.image = ImageCanvas(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.image.toolbar)
        layout.addWidget(self.image.canvas)

    def set_image(self, path):
        try:
            image = pydicom.dcmread(path)
            self.image.ax.imshow(image.pixel_array, cmap=plt.cm.bone)
            self.image.canvas.draw()
        except:
            QMessageBox.warning(
                self, 'File extension Error',
                '''This file extension is not supported. Try with DICOM files''', QMessageBox.Ok)

    def resetImage(self):
        filePath = 'img/noImg.png'
        image = imageio.imread(filePath)
        self.image.ax.imshow(image)
        self.image.canvas.draw()