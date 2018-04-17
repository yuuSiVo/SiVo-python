from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt


class QGraphicsTextItemFixed(QtGui.QGraphicsTextItem):  # need to add fix for enter pressed and escape
    def __init__(self, text, parent=None):
        super(QGraphicsTextItemFixed, self).__init__(text, parent)

        self.forcedSize = QtCore.QRectF(0, 0, 10, 20)

    def boundingRect(self):
        return self.forcedSize

    def forceSize(self, x, y, width):
        self.forcedSize.setCoords(0, 0, width, 20)
        self.setPos(x, y)


class tts(QtGui.QGraphicsView):

    def __init__(self, parent=None):
        super(tts, self).__init__(parent)

        # Select, Pen, Erase
        self.selTool = "Select"

        self.newmeasureCnt = 0
        self.measureCnt = 0

        self.startMousePressX = 0
        self.startMousePressY = 0
        self.endMousePressX = 0
        self.endMousePressY = 0
        self.mouseStartButton = 0

        self.initUI()

    def initUI(self):
        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)


    def mouseReleaseEvent(self, event):
        super(tts, self).mouseReleaseEvent(event)  # Call parent function and do set up
        # when mouse is released, save point


class pianoRoll(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        super(pianoRoll, self).__init__(parent)

        self.initUI()

    def initUI(self):
        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)