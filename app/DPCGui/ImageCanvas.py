import pydicom
import imageio
from PyQt5.QtWidgets import QSizePolicy, QLabel

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class ImageCanvas(object):
    def __init__(self, parent):
        self.figure = plt.figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, parent)
        self.__initPlot()

    def __initPlot(self):
        self.ax = self.figure.add_subplot(111)
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)

        filePath = 'res/img/noImg.png'
        image = imageio.imread(filePath)
        self.ax.imshow(image)

        self.canvas.draw()