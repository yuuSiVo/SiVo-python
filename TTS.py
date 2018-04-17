# -*- codeing: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QWidget
import TTSEditor
import pyttsx3


class mainUI(QtGui.QMainWindow):

    # use the parent to set up the minute details
    def __init__(self):
        super(mainUI, self).__init__()

        self.resize = QtCore.QTimer(self)
        self.connect(self.resize, QtCore.SIGNAL("timeout()"), self.rsz)
        self.resize.start()

        self.showFlg = True

        self.initUI()

    # set up basic UI elements
    def initUI(self):
        # Set up menubar
        ##Set Up menu actions

        newAction = QtGui.QAction('&New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New file')

        fileAction = QtGui.QAction('&Open', self)
        fileAction.setShortcut('Ctrl+O')
        fileAction.setStatusTip('Open File')
        self.connect(fileAction, QtCore.SIGNAL('triggered()'), self.showOpenDialog)

        NameFileAction = QtGui.QAction('&名前を付けて保存', self)
        NameFileAction.setShortcut('Ctrl+A')
        NameFileAction.setStatusTip('名前を付けて保存')
        self.connect(NameFileAction, QtCore.SIGNAL('triggered()'), self.showSaveDialog)

        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        ##Menubar Menus setup
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(fileAction)
        fileMenu.addAction(NameFileAction)
        fileMenu.addAction(exitAction)

        ModeMenu = menubar.addMenu('&Mode')

        helpMenu = menubar.addMenu('&Help')
        savemeMenu = helpMenu.addMenu('&Save me from this hell')
        nopeLabel = savemeMenu.addMenu('&There is no salvation')

        # Set Up Tool Bar? yeah
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        # Status bar message
        self.statusBar().showMessage('This is the status bar message :D')

        self.track= TTSEditor.tts(self)
        self.track.show()

        # hide scroll bars and hide their bg bars
        self.tts = TTSEditor.tts(self)
        self.tts.show()
        self.tts.verticalScrollBar().hide()
        self.tts.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")
        self.tts.horizontalScrollBar().hide()
        self.tts.horizontalScrollBar().setStyleSheet("QScrollBar {height:0px;}")

        # Show Window
        self.text = QtGui.QTextEdit(self)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('SiVo Talk')
        self.show()

        button = QtGui.QPushButton('合成', self)
        self.connect(synth, QtCore.SIGNAL('triggered()'), self.synth)
        button.resize(button.sizeHint())
        button.move(300, 500)

    def flgviewToggle(self):
        self.showFlg = not self.showFlg

    def rsz(self):
        # Starting at 20 because menu bar is 20 px
        # 120 is px for keyboard role
        # -60 because bottom scrollbar will cut off and measure is on top
        # extra  200 off for flag editor
        # Make it so the flag editor is toggleable
        if self.showFlg:
            self.text.setGeometry(120, 40, self.width() - 120, self.height() - 60 - 200)
        else:
            self.track.setGeometry(120, 40, self.width() - 120, self.height() - 60)

        if self.showFlg:
            self.track.setGeometry(0, 40, 120, self.height() - 60 - 200)
        else:
            self.track.setGeometry(0, 40, 120, self.height() - 60)

        if self.track.newmeasureCnt != 0:
            self.measure.drawMeasures(self.track.measureCnt, self.track.newmeasureCnt)
            self.track.measureCnt += self.track.newmeasureCnt
            self.track.newmeasureCnt = 0
        # set scroll of piano role to the track
        self.tts.verticalScrollBar().setValue(self.track.verticalScrollBar().value())

    def synth(self):
        engine = pyttsx3.init()


    def showOpenDialog(self):

        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open', '')
        from os.path import isfile
        if isfile(self.filename):
            import codecs
            fname = codecs.open(self.filename, 'r', 'utf-8')
            data = fname.read()
            self.NoteEdit.setNote(data)

    def showSaveDialog(self):

        savename = QtGui.QFileDialog.getSaveFileName(self, '名前を付けて保存', '')
        fname = open(savename, 'w')
        fname.write(self.textEdit.toPlainText())

    def showwavDialog(self):

        savename = QtGui.QFileDialog.getSaveFileName(self, 'Wavの書き出し', '.wav')
        fname = open(savename, 'w')

    def MonoDialog(self):
        savename = QtGui.QFileDialog.getSaveFileName(self, 'Monoラベルの書き出し', '.lab')

    def trimSpace(st):
        while len(st) > 0 and (st[0] == " " or st[0] == "\n"):
            st = st[1:]
        while len(st) > 0 and (st[-1] == " " or st[-1] == "\n"):
            st = st[:-1]
        return st

def main():
    app = QtGui.QApplication(sys.argv)

    mui = mainUI()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
