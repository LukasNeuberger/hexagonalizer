from PyQt5 import QtWidgets, QtCore, QtGui, uic

class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, scene):
        super(GraphicsView, self).__init__(scene)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.fitInView(0,0,self.scene().width(),self.scene().height(),QtCore.Qt.KeepAspectRatio)

        return super().resizeEvent(event)
