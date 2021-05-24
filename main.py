import sys
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from utils import *

from graphicsView import GraphicsView

from mainwindow import Ui_MainWindow

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method

        self.ui = Ui_MainWindow()
        
        self.ui.setupUi(self)

        self.ui.FilePickerBtn.clicked.connect(self.onPickFileClick)
        self.ui.CalculateHexBtn.clicked.connect(self.onCalculateHexClick)
        self.ui.SaveHexBtn.clicked.connect(self.onSaveHexClick)
        self.ui.CalculateColorsBtn.clicked.connect(self.onCalculateClusterClick)
        self.ui.SaveClusteredBtn.clicked.connect(self.onSaveClusteredClick)

        self.selectedFile = ''
        self.image = None
        self.hexagonImage = None
        self.segmentedImage = None

        self.show() # Show the GUI

    def onPickFileClick(self):
        self.selectedFile = self.getFile()
        self.ui.FilePickerLbl.setText(self.selectedFile)
        self.image = loadImage(self.selectedFile)
        self.showImage(self.image, self.ui.ImagePlaceHolder)
        self.ui.hexTab.setEnabled(False)
        self.removeImage(self.ui.HexImagePlaceHolder)
        self.ui.clusteredTab.setEnabled(False)
        self.removeImage(self.ui.ClusteredImagePlaceHolder)
        
    def getFile(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        return fileName

    def removeImage(self, placeHolder):
        while(placeHolder.count() > 0):
            placeHolder.removeItem(placeHolder.itemAt(0))
    
    def showImage(self, image, placeHolder):
        qImage = QtGui.QImage(image.data,image.shape[1],image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        pix = QtGui.QPixmap(QtGui.QPixmap.fromImage(qImage))
        item = QtWidgets.QGraphicsPixmapItem(pix)
        scene = QtWidgets.QGraphicsScene(self)
        scene.addItem(item)
        graphics = GraphicsView(scene)

        self.removeImage(placeHolder)
        placeHolder.addWidget(graphics)

    def onCalculateHexClick(self):
        n = self.ui.HorizontalHexSpin.value()
        self.pattern = calcHexagonPattern(self.image, n)
        self.hexagonImage = calcHexagonImage(self.pattern)
        self.ui.hexTab.setEnabled(True)
        self.showImage(self.hexagonImage, self.ui.HexImagePlaceHolder)
        self.ui.clusteredTab.setEnabled(False)
        self.removeImage(self.ui.ClusteredImagePlaceHolder)
        self.ui.tabWidget.setCurrentWidget(self.ui.hexTab)

    def onSaveHexClick(self):
        path = self.selectedFile + '.hex.jpeg'
        saveImage(path, self.hexagonImage) 

    def onCalculateClusterClick(self):
        k = self.ui.ColorSpinBox.value()
        self.clusters = calcColors(self.pattern, k)
        self.clusteredImage = calcHexagonImage(self.clusters)
        self.ui.clusteredTab.setEnabled(True)
        self.showImage(self.clusteredImage, self.ui.ClusteredImagePlaceHolder)
        self.ui.tabWidget.setCurrentWidget(self.ui.clusteredTab)

    def onSaveClusteredClick(self):
        path = self.selectedFile + '.clustered.jpeg'
        saveImage(path, self.clusteredImage) 

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
