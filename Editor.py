from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt

class QGraphicsTextItemFixed(QtGui.QGraphicsTextItem): #need to add fix for enter pressed and escape
    def __init__(self, text, parent = None):
        super(QGraphicsTextItemFixed, self).__init__(text, parent)

        self.forcedSize = QtCore.QRectF(0, 0, 10, 20)

    def boundingRect(self):
        return self.forcedSize
    def forceSize(self, x, y, width):
        self.forcedSize.setCoords(0,0,width, 20)
        self.setPos(x, y)

class noteEditor(QtGui.QGraphicsView):

    def __init__(self, parent = None):
        super(noteEditor, self).__init__(parent)

        #Select, Pen, Erase
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

        self.noteList=[]
        self.currentDraw = QtGui.QGraphicsRectItem()

        self.mouseDown = False
        self.isDrag = False
        
    
        self.quantize=4
        self.grid=4
        self.selTool = "Select"
#color space of smell
        #edit x setting to look better
        
        #setting height to 10 per row/ changeing to 20
        #77 notes (c1-b7) ------------ 770 total
        #ADD ZOOM TO X!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #Gen first 50 cells, 120.0 qt note, 480.0 whole (conversion function needed to 480 qt note in utau)
        self.drawMeasure(0, 50)

        
    #Add X Scale combat!!!
    def drawMeasure(self, measureOffNo, measureCnt = 1):
        self.newmeasureCnt += measureCnt
        brush = QtGui.QBrush(QtGui.QColor(90, 90, 90))
        pen = QtGui.QPen(QtGui.QColor(45, 45, 45))
        pen.setWidth(2)

        brush2 = QtGui.QBrush(QtGui.QColor(60, 60, 60))
        pen2 = QtGui.QPen(QtGui.QColor(75, 75, 75))
        pen2.setWidth(2)

        brush3 = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        pen3 = QtGui.QPen(QtGui.QColor(105, 105, 105))
        pen3.setWidth(2)

        
        measureXDraw = measureCnt * 480
        offset = measureOffNo * 480
        for i in range(0, 7):
            self.scene.addRect(offset, 0.0 + (240 * i), measureXDraw, 20, pen, brush)
            self.scene.addRect(offset, 20.0 + (240 * i), measureXDraw, 20, pen2, brush2)
            self.scene.addRect(offset, 40.0 + (240 * i), measureXDraw, 20, pen, brush)
            self.scene.addRect(offset, 60.0 + (240 * i), measureXDraw, 20, pen2, brush2)
            self.scene.addRect(offset, 80.0 + (240 * i), measureXDraw, 20, pen, brush)
            self.scene.addRect(offset, 100.0 + (240 * i), measureXDraw, 20, pen2, brush2)
            self.scene.addRect(offset, 120.0 + (240 * i), measureXDraw, 20, pen, brush)
            self.scene.addRect(offset, 140.0 + (240 * i), measureXDraw, 20, pen, brush)
            self.scene.addRect(offset, 160.0 + (240 * i), measureXDraw, 20, pen2, brush2)
            self.scene.addRect(offset, 180.0 + (240 * i), measureXDraw, 20, pen, brush)
            self.scene.addRect(offset, 200.0 + (240 * i), measureXDraw, 20, pen2, brush2)
            self.scene.addRect(offset, 220.0 + (240 * i), measureXDraw, 20, pen3, brush3)

        lineP = QtGui.QPen(QtGui.QColor(150, 150, 150))
        lineP.setWidth(3)
            
        lineP2 = QtGui.QPen(QtGui.QColor(255, 255, 255))
        lineP2.setWidth(3)
        for i in range(0, measureCnt):
            self.scene.addLine(offset + (480 * i), 0, 0 + (480 * i),1680, lineP2)
            self.scene.addLine(offset + 120 + (480 * i), 0, 120 + (480 * i),1680, lineP)
            self.scene.addLine(offset + 240 + (480 * i), 0, 240 + (480 * i),1680, lineP)
            self.scene.addLine(offset + 360 + (480 * i), 0, 360 + (480 * i),1680, lineP)

    
    def mousePressEvent(self, event):
        super(noteEditor, self).mousePressEvent(event) #Call parent function and do set up
        #when mouse is pressed, save point
        self.startMousePressX = self.mapToScene(QtCore.QPoint(event.x(), event.y())).x()
        self.startMousePressY = self.mapToScene(QtCore.QPoint(event.x(), event.y())).y()

        self.mouseDown = True
        self.mouseStartButton = event.button()

        print ("Start Press")

        print ("( " + str(self.startMousePressX) + ", " + str(self.startMousePressY) + " )")
        if self.selTool == "Pen" and self.mouseStartButton==1:
            self.drawNoteStart()
            

    def mouseMoveEvent(self, event):
        super(noteEditor, self).mouseMoveEvent(event)
        if self.mouseDown:
            self.isDrag = True

        #when mouse is moved, save point
        self.endMousePressX = self.mapToScene(QtCore.QPoint(event.x(), event.y())).x()
        self.endMousePressY = self.mapToScene(QtCore.QPoint(event.x(), event.y())).y()
        if self.selTool == "Pen" and self.mouseStartButton==1:
            self.drawNote(event)

    def mouseReleaseEvent(self, event):
        super(noteEditor, self).mouseReleaseEvent(event) #Call parent function and do set up
        #when mouse is released, save point
        self.endMousePressX = self.mapToScene(QtCore.QPoint(event.x(), event.y())).x()
        self.endMousePressY = self.mapToScene(QtCore.QPoint(event.x(), event.y())).y()


        print ("End Press")

        print ("( " + str(self.endMousePressX) + ", " + str(self.endMousePressY) + " )")

        if self.selTool == "Pen" and self.mouseStartButton==1:
            self.drawNoteEnd()

        self.mouseDown = False
        self.isDrag = False
        self.mouseStartButton = 0

    def drawNoteStart(self):
        print ("DRAWING START")

        pen = QtGui.QPen(QtGui.QColor(192, 231, 218)) # create a rectangle where click (new note)
        brush = QtGui.QBrush(QtGui.QColor(163, 229, 207))

        calcGridX = (int(self.startMousePressX)/(480/self.grid))*(480.0/self.grid)
        if calcGridX < 0:
            calcGridX = 0

        self.startMousePressX = calcGridX

        self.startMousePressY = (int(self.startMousePressY)/20) * 20
        
        self.currentDraw = QtGui.QGraphicsRectItem(calcGridX, self.startMousePressY, 480.0/self.quantize, 20)
        self.currentDraw.setPen(pen)
        print (dir(self.currentDraw))
        self.currentDraw.setBrush(brush)
        self.scene.addItem(self.currentDraw)

    def drawNote(self, event):
        print ("DRAWING MOVE")

        #print "Move Press"

        #print "( " + str(self.endMousePressX) + ", " + str(self.endMousePressY) + " )"

        
        #                   #take the width between start and end, divide by standard quantize length, this will leave how many
        #                           --quant units there are, then multiply by the quant size
        quantizedValue = (int(self.endMousePressX-self.startMousePressX)/(480/self.quantize) + 1)*(480.0/self.quantize)
        #make sure note is not 0 length
        if quantizedValue < 1:
            quantizedValue = (480.0/self.quantize)

        self.startMousePressY = (int(self.mapToScene(QtCore.QPoint(event.x(), event.y())).y())/20) * 20    
        self.currentDraw.setRect(self.startMousePressX, self.startMousePressY, quantizedValue, 20)

    def drawNoteEnd(self):
        lyric = QGraphicsTextItemFixed("Ooh")
        lyric.forceSize(self.currentDraw.rect().x(), self.currentDraw.rect().y(), self.currentDraw.rect().width()/2.0)
        #lyric.setPos(self.currentDraw.rect().x(), self.currentDraw.rect().y())
        lyric.setTextInteractionFlags(QtCore.Qt.TextEditable)
        #lyric.setWidth = -1
        phon = QtGui.QGraphicsTextItem("[ow]")
        phon.setPos(self.currentDraw.rect().x() + self.currentDraw.rect().width() - phon.boundingRect().width() , self.currentDraw.rect().y())
        if self.currentDraw.rect().width() > phon.boundingRect().width() + lyric.boundingRect().width():
            self.scene.addItem(lyric)
            self.scene.addItem(phon)
        elif self.currentDraw.rect().width() > lyric.boundingRect().width():
            self.scene.addItem(lyric)

        #print dir(lyric)
        print (lyric.x())
        print (lyric.y())
        
        #self.noteList.append( (self.currentDraw,  ) )
        print ("DRAWING END")

        

    def contextMenuEvent(self, event):

        menu = QtGui.QMenu()
        quitAction = menu.addAction("Quit")
        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == quitAction:
            print ("I quit")
            



class measureDraw(QtGui.QGraphicsView):
    def __init__(self, parent = None):
        super(measureDraw, self).__init__(parent)

        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)

    def drawMeasures(self, measureOffNo, measureCnt):
        offset = measureOffNo * 480

        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        line = QtGui.QPen(QtGui.QColor(207, 207, 207))
        
        for i in range(0, measureCnt):
            self.scene.addRect(offset + (i * 480), 0, 480, 20)
            self.scene.addText(str(measureOffNo + i + 1)).setPos(offset + 235 + (i * 480), 0)
    

            

class pianoRoll(QtGui.QGraphicsView):
    def __init__(self, parent = None):
        super(pianoRoll, self).__init__(parent)

        self.initUI()

    def initUI(self):
        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)

        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0))

        brush2 = QtGui.QBrush(QtGui.QColor(10, 10, 10))
        pen2 = QtGui.QPen(QtGui.QColor(0, 0, 0))

        #manually place 1 octave of keyboard manually, and place the rest automatically
        for i in range(0, 7):
            self.scene.addRect(0, 0.0 + (240 * i), 120, 30, pen, brush)
            self.scene.addRect(0, 30.0 + (240 * i), 120, 40, pen, brush)
            self.scene.addRect(0, 70.0 + (240 * i), 120, 40, pen, brush)
            self.scene.addRect(0, 110.0 + (240 * i), 120, 30, pen, brush)
            self.scene.addRect(0, 140.0 + (240 * i), 120, 30, pen, brush)
            self.scene.addRect(0, 170.0 + (240 * i), 120, 40, pen, brush)
            self.scene.addRect(0, 210.0 + (240 * i), 120, 30, pen, brush)

            self.scene.addRect(0, 20.0 + (240 * i), 60, 20, pen2, brush2)
            self.scene.addRect(0, 60.0 + (240 * i), 60, 20, pen2, brush2)
            self.scene.addRect(0, 100.0 + (240 * i), 60, 20, pen2, brush2)
            self.scene.addRect(0, 160.0 + (240 * i), 60, 20, pen2, brush2)
            self.scene.addRect(0, 200.0 + (240 * i), 60, 20, pen2, brush2)

            self.scene.addText("C" + str(7-i)).setPos(95, 215 + (240 * i))
            
            

            
            
        
        
