import sys
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from utils import *

from mainwindow import Ui_MainWindow

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method

        self.ui = Ui_MainWindow()
        
        self.ui.setupUi(self)

        self.ui.FilePickerBtn.clicked.connect(self.onPickFileClick)
        self.ui.CalculateBtn.clicked.connect(self.onCalculateClick)
        self.ui.CalculateHexBtn.clicked.connect(self.onCalculateHexClick)
        self.ui.SaveBtn.clicked.connect(self.onSaveClick)
        self.selectedFile = ''
        self.image = None
        self.segmentedImage = None
        self.hexagonImage = None

        self.show() # Show the GUI

    def onPickFileClick(self):
        self.selectedFile = self.getFile()
        self.ui.FilePickerLbl.setText(self.selectedFile)
        self.image = loadImage(self.selectedFile)
        self.showImage(self.image)

    def onCalculateClick(self):
        k = self.ui.ColorsSpin.value()
        self.segmentedImage = calcKMeansImage(self.hexagonImage,k)
        self.showImage(self.segmentedImage)

    def onCalculateHexClick(self):
        innerR = self.ui.HorizontalHexSpin.value()
        k = self.ui.ColorsSpin.value()
        self.hexagonImage = calcHexagonImage(self.image, innerR,k)
        self.showImage(self.hexagonImage)

    def onSaveClick(self):
        path = self.selectedFile + '.hex.jpeg'
        saveImage(path, self.segmentedImage)
        
    
    def getFile(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        return fileName
    
    def showImage(self, image):
        qImage = QtGui.QImage(image.data,image.shape[1],image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        pix = QtGui.QPixmap(QtGui.QPixmap.fromImage(qImage))
        item = QtWidgets.QGraphicsPixmapItem(pix)
        scene = QtWidgets.QGraphicsScene(self)
        scene.addItem(item)
        originalGraphics = QtWidgets.QGraphicsView(scene)
        
        while(self.ui.ImagePlaceHolder.count() > 0):
            self.ui.ImagePlaceHolder.removeItem(self.ui.ImagePlaceHolder.itemAt(0))
        self.ui.ImagePlaceHolder.addWidget(originalGraphics)

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
