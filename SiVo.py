# -*- codeing: utf-8 -*-

import sys
from xml.etree.ElementTree import Element, SubElement, tostring, XML
from xml.etree import ElementTree
from xml.dom import minidom
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox
from PyQt4.QtGui import QWidget
import Editor
import xml.etree.ElementTree as ET
import argparse
import array
from numpy import *


class mainUI(QtGui.QMainWindow):

    #use the parent to set up the minute details
    def __init__(self):
        super(mainUI, self).__init__()

        self.resize = QtCore.QTimer(self)
        self.connect(self.resize, QtCore.SIGNAL("timeout()"), self.rsz)
        self.resize.start()        

        self.showFlg = True
        
        self.initUI()

    #set up basic UI elements
    def initUI(self):
        #Set up menubar
        ##Set Up menu actions


        newAction = QtGui.QAction('&New',self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New file')

        fileAction = QtGui.QAction('&Open',self)
        fileAction.setShortcut('Ctrl+O')
        fileAction.setStatusTip('Open File')
        self.connect(fileAction, QtCore.SIGNAL('triggered()'), self.showOpenDialog)

        NameFileAction = QtGui.QAction('&名前を付けて保存',self)
        NameFileAction.setShortcut('Ctrl+A')
        NameFileAction.setStatusTip('名前を付けて保存')
        self.connect(NameFileAction, QtCore.SIGNAL('triggered()'), self.showSaveDialog)

        xmlAction = QtGui.QAction('&XMLの書き出し',self)
        xmlAction.setShortcut('Ctrl+L')
        xmlAction.setStatusTip('XMLの書き出し')
        self.connect(xmlAction,QtCore.SIGNAL('triggered()'), self.showxmlDialog)

        wavAction = QtGui.QAction('&wavの書き出し', self)
        wavAction.setShortcut('Ctrl+L')
        wavAction.setStatusTip('wavの書き出し')
        self.connect(wavAction, QtCore.SIGNAL('triggered()'), self.showwavDialog)

        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        flgviewAction = QtGui.QAction('&Toggle flag editor', self)
        flgviewAction.setStatusTip('Show/Hide the flag editor view')
        flgviewAction.triggered.connect(self.flgviewToggle)

        tselectAction = QtGui.QAction('&Select', self)
        tselectAction.setStatusTip("Note select and edit tool")
        tselectAction.triggered.connect(self.toolSelect)
        
        tpenAction = QtGui.QAction('&Pen', self)
        tpenAction.setStatusTip("Note draw tool")
        tpenAction.triggered.connect(self.toolPen)
        
        teraseAction = QtGui.QAction('&Erase', self)
        teraseAction.setStatusTip("Note erase tool")
        teraseAction.triggered.connect(self.toolErase)

        tpquant4Action = QtGui.QAction('&L4 Quarter Note', self)
        tpquant4Action.setStatusTip('Set Quantization to Quarter notes')
        tpquant4Action.triggered.connect(self.quant4)

        tpquant8Action = QtGui.QAction('&L8 Eighth Note', self)
        tpquant8Action.setStatusTip('Set Quantization to Eighth notes')
        tpquant8Action.triggered.connect(self.quant8)

        tpquant16Action = QtGui.QAction('&L16 Sixteenth Note', self)
        tpquant16Action.setStatusTip('Set Quantization to Sixteenth notes')
        tpquant16Action.triggered.connect(self.quant16)

        playAction=QtGui.QAction('&Play',self)
        playAction.setStatusTip('Synthesize')
        playAction.triggered.connect(self.playAction)

        MonoAction=QtGui.QAction('&monoラベルの書き出し',self)
        MonoAction.setStatusTip('monoラベル書き出し')
        self.connect(MonoAction, QtCore.SIGNAL('triggered()'), self.MonoDialog)

        ##Menubar Menus setup
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(fileAction)
        fileMenu.addAction(NameFileAction)
        fileMenu.addAction(xmlAction)
        fileMenu.addAction(wavAction)
        fileMenu.addAction(MonoAction)
        fileMenu.addAction(exitAction)

        editMenu = menubar.addMenu('&Edit')

        trackMenu = menubar.addMenu('&Track')

        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(flgviewAction)

        searchMenu = menubar.addMenu('&Search')

        projMenu = menubar.addMenu('&Project')
        projMenu.addAction(playAction)

        toolMenu = menubar.addMenu('&Tools')
        toolMenu.addAction(tselectAction)
        toolMenu.addAction(tpenAction)
        toolMenu.addAction(teraseAction)
        quantMenu = toolMenu.addMenu('&Quantization')
        quantMenu.addAction(tpquant4Action)
        quantMenu.addAction(tpquant8Action)
        quantMenu.addAction(tpquant16Action)

        ModeMenu = menubar.addMenu('&Mode')



        self.quantize = 4
        
        helpMenu = menubar.addMenu('&Help')
        savemeMenu = helpMenu.addMenu('&Save me from this hell')
        nopeLabel = savemeMenu.addMenu('&There is no salvation')

        #Set Up Tool Bar? yeah
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        
        
        #Status bar message
        self.statusBar().showMessage('This is the status bar message :D')




        self.track = Editor.noteEditor(self)
        self.track.show()


        #hide scroll bars and hide their bg bars
        self.piano = Editor.pianoRoll(self)
        self.piano.show()
        self.piano.verticalScrollBar().hide()
        self.piano.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")
        self.piano.horizontalScrollBar().hide()
        self.piano.horizontalScrollBar().setStyleSheet("QScrollBar {height:0px;}")

        self.measure = Editor.measureDraw(self)
        self.measure.show()
        #newmeasureCnt
        self.measure.verticalScrollBar().hide()
        self.measure.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")
        self.measure.horizontalScrollBar().hide()
        self.measure.horizontalScrollBar().setStyleSheet("QScrollBar {height:0px;}")
        
        #Show Window
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('SiVo')
        self.show()


    def flgviewToggle(self):
        self.showFlg = not self.showFlg
    def rsz(self):
        #Starting at 20 because menu bar is 20 px
        #120 is px for keyboard role
        #-60 because bottom scrollbar will cut off and measure is on top
        #extra  200 off for flag editor
        #Make it so the flag editor is toggleable
        if self.showFlg:
            self.track.setGeometry(120, 40, self.width() - 120, self.height() - 60 - 200)
        else:
            self.track.setGeometry(120, 40, self.width() - 120, self.height() - 60)

        if self.showFlg:
            self.piano.setGeometry(0, 40, 120, self.height() - 60 - 200)
        else:
            self.piano.setGeometry(0, 40, 120, self.height() - 60)

        self.measure.setGeometry(120, 40, self.width() - 120, 20)

        if self.track.newmeasureCnt != 0:
            self.measure.drawMeasures(self.track.measureCnt, self.track.newmeasureCnt)
            self.track.measureCnt += self.track.newmeasureCnt
            self.track.newmeasureCnt = 0
        #set scroll of piano role to the track
        self.piano.verticalScrollBar().setValue(self.track.verticalScrollBar().value())
        self.measure.horizontalScrollBar().setValue(self.track.horizontalScrollBar().value())

    def toolSelect(self):
        self.track.selTool = "Select"
        print ("Sel")
    def toolPen(self):
        self.track.selTool = "Pen"
        print ("Pen")
    def toolErase(self):
        self.track.selTool = "Erase"
        print ("Del")

    def quant4(self):
        self.quantize = 4
        self.track.quantize=self.quantize
        self.track.grid=self.quantize
    def quant8(self):
        self.quantize = 8
        self.track.quantize=self.quantize
        self.track.grid=self.quantize
    def quant16(self):
        self.quantize = 16
        self.track.quantize=self.quantize
        self.track.grid=self.quantize

    def showOpenDialog(self):

        self.filename = QtGui.QFileDialog.getOpenFileName(self,'Open','')
        from os.path import isfile
        if isfile(self.filename):
            import codecs
            fname = codecs.open(self.filename,'r','utf-8')
            data = fname.read()
            self.NoteEdit.setNote(data)

    def showSaveDialog(self):

        savename = QtGui.QFileDialog.getSaveFileName(self, '名前を付けて保存', '')
        fname = open(savename, 'w')
        fname.write(self.textEdit.toPlainText())

    def showxmlDialog(self):

        savename = QtGui.QFileDialog.getSaveFileName(self, 'xmlの書き出し', '.xml')
        fname = open(savename, 'w')

        root = ET.Element('SINGING')

        sub = ET.SubElement(root, 'PITCH')

        subsub = ET.SubElement(sub, 'DURATION')
        subsub.set('PITCH', 'C4')
        subsub.text = 'doe'

        subsub2 = ET.SubElement(sub, 'DURATION')
        subsub2.set('PITCH', 'B4')
        subsub2.text = 'ray'

        string = ET.tostring(root, 'utf-8')
        pretty_string = minidom.parseString(string).toprettyxml(indent='?xml version="1.0" ')

        with open('test.xml', 'w') as f:
            f.write(pretty_string)

        with open('test.xml', 'w') as f:
            f.write(pretty_string)
    def showwavDialog(self):

        savename = QtGui.QFileDialog.getSaveFileName(self, 'Wavの書き出し', '.wav')
        fname = open(savename, 'w')



    def MonoDialog(self):
        savename=QtGui.QFileDialog.getSaveFileName(self,'Monoラベルの書き出し', '.lab')

    def trimSpace(st):
        while len(st) > 0 and (st[0] == " " or st[0] == "\n"):
            st = st[1:]
        while len(st) > 0 and (st[-1] == " " or st[-1] == "\n"):
            st = st[:-1]
        return st

    def genMonoLabel(name, out, df):
        # Read xml
        try:
            tree = ET.parse(name)
        except:
            raise Exception("File " + str(name) + " does not exist")
        root = tree.getroot()

        parts = []
        for child in root:
            # print (child.tag, child.attrib)
            if child.tag.lower() == "part":
                parts.append(child)
                # print ("haha")

        measures = []
        for i in parts:
            for j in i:
                # print (j.tag, j.attrib)
                if j.tag.lower() == "measure":
                    measures.append(j)

        # print
        direct = []
        # for i in measures[0]:
        # print (i.tag, i.attrib)
        # if i.tag.lower() == "direction":
        # direct = i
        # if i.tag.lower() == "note":
        # notes.append(i)
        # print ("aaa")
        # for i in notes[-1]:
        # print (i.tag, i.attrib)

        # print ("\n")
        # print (notes[-1][0][0].text)
        # note struct
        # ([measure], [duration], tempo, [step], [octave], word, [parts]) #this is for per word

        tempo = 120
        notes = []
        mNo = 0

        tOctave = []
        tStep = []
        tWord = ""
        tPart = []
        tSyl = ""
        tDur = []
        tMes = []
        # Add code to read scale later T_T (needed to correctly identify sharps and flats)

        for measure in measures:
            mNo = measure.attrib["number"]
            for part in measure:
                if part.tag.lower() == "direction":
                    for tg in part:
                        if tg.tag.lower() == "sound":
                            tempo = float(tg.attrib["tempo"])
                            print(tempo)
                if part.tag.lower() == "sound":
                    tempo = float(part.attrib["tempo"])
                    print(tempo)
                if part.tag.lower() == "note":
                    tMes.append(mNo)
                    for tg in part:
                        if tg.tag.lower() == "rest":
                            tWord = "ppppp"
                            tPart = ["ppppp"]
                            tSyl = "single"
                            tStep = [0]
                            tOctave = [0]
                        if tg.tag.lower() == "duration":
                            tDur.append(float(tg.text))
                        if tg.tag.lower() == "lyric":
                            for tgtg in tg:
                                if tgtg.tag.lower() == "syllabic":
                                    tSyl = tgtg.text.lower()
                                if tgtg.tag.lower() == "text":
                                    tWord += tgtg.text.lower()
                                    tPart.append(tgtg.text.lower())
                        if tg.tag.lower() == "pitch":
                            for tgtg in tg:
                                if tgtg.tag.lower() == "step":
                                    tStep.append(tgtg.text.lower())
                                if tgtg.tag.lower() == "octave":
                                    tOctave.append(int(tgtg.text.lower()))

                    if tSyl == "single" or tSyl == "end":
                        notes.append((tMes, tDur, tempo, tStep, tOctave, tWord, tPart))
                        tOctave = []
                        tStep = []
                        tWord = ""
                        tPart = []
                        tSyl = ""
                        tDur = []
                        tMes = []

        # note struct
        # ([measure], [duration], tempo, [step], [octave], word, [parts]) #this is for per word

        # load dictionary
        dic = {"ppppp": "pau"}
        try:
            with open(df) as fp:
                for line in fp:
                    word = ""
                    phons = ""
                    for i in range(0, len(line)):
                        if line[i] == " ":
                            phons = line[i + 1:-1]
                            break
                        word += line[i]
                    # print word
                    # dic[word] = trimSpace(phons)
        except:
            raise Exception("Cannot locate " + df + "\nMake sure it is in the same directory as monoLabel.py")

        last = 0.0
        dur = 0
        phons = []
        mp = []
        for i in notes:
            lng = 0
            phons = []
            tempoScal = 1.0 / i[2] * 60.0
            pts = 0.0
            dur = 0
            for j in i[1]:
                dur += (j / 4.0) * tempoScal
            try:
                print(i[5], dic[i[5]])
                phons = dic[i[5]].split(" ")
            except:
                print("Warning!!!\nWord not in dictionary: " + i[5])
                phons = [i[5]]
            pts = dur / float(len(phons))
            for i in phons:
                mp.append((last, last + pts, i))
                last += pts

        mp2 = []
        temp = (0.0, 0.0, "")
        procP = False
        for i in mp:
            if i[2] == "pau" and procP:
                temp = (temp[0], i[1], "pau")
            elif i[2] == "pau":
                temp = i
                procP = True
            elif procP:
                mp2.append(temp)
                procP = False
                mp2.append(i)
            else:
                mp2.append(i)

        lab = open("outLab.Audacity.lab", 'w')
        for i in mp2:
            lab.write(str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n")
        lab.close()

        lab = open(out, 'w')
        for i in mp2:
            lab.write(str(int(i[0] * 10000000)) + " " + str(int(i[1] * 10000000)) + " " + str(i[2]) + "\n")
        lab.close()

        return 1

    def lab2grid(file, out):
        labs = []
        try:
            with open(file) as fp:
                for line in fp:
                    ln = line.split(" ")
                    labs.append((float(ln[0]), float(ln[1]), ln[2]))
        except:
            raise Exception("File " + file + " does not exist or is in the wrong format")
        grid = open(out, 'w')
        grid.write("File type = \"ooTextFile\"\n")
        grid.write("Object class = \"TextGrid\"\n")
        grid.write("\n0\n")
        grid.write(str(labs[-1][1] / 10000000.0) + "\n")
        grid.write("<exists>\n")
        grid.write("1\n")
        grid.write("\"IntervalTier\"\n")
        grid.write("\"words\"\n")
        grid.write("0\n")
        grid.write(str(labs[-1][1] / 10000000.0) + "\n")
        grid.write(str(int(len(labs))) + "\n")
        for i in labs:
            grid.write(str(i[0] / 10000000.0) + "\n")
            grid.write(str(i[1] / 10000000.0) + "\n")
            grid.write("\"" + trimSpace(i[2]) + "\"\n")
        grid.close()

    def grid2lab(file, out):
        try:
            grid = open(file, 'r')
        except:
            Exception("File " + file + " does not exist")
        grid.readline()
        check = trimSpace(grid.readline())
        if check[-3:].lower() != 'id"':
            grid.close()
            raise Exception("Invalid File Type")
        grid.readline()
        check = trimSpace(grid.readline())
        if check[0] == 'x':
            grid.close()
            raise Exception("Expected Short Text TextGrid, given Long Text")
        grid.readline()  # xmax
        grid.readline()  # exists
        grid.readline()  # 1
        grid.readline()  # interval
        grid.readline()  # words
        grid.readline()  # xmin
        grid.readline()  # xm
        grid.readline()  # count
        labs = []

        temp = trimSpace(grid.readline())
        while temp != "":
            labs.append((float(temp) * 10000000, float(trimSpace(grid.readline())) * 10000000,
                         trimSpace(grid.readline())[1:-1]))
            temp = trimSpace(grid.readline())
        grid.close()

        lab = open(out, 'w')
        for i in labs:
            lab.write(str(int(i[0])) + " " + str(int(i[1])) + " " + str(i[2]) + "\n")
        lab.close()

    def main():
        parser = argparse.ArgumentParser(
            description="Utility program for Mono Labeling. Please use short text TextGrids and HTK labels only.")
        parser.add_argument("mode", help="Specify operation mode", choices=["label", "lab2grid", "grid2lab"])
        parser.add_argument("file", help="Path to file")
        parser.add_argument("-o", help="Output file")
        parser.add_argument("-d", help="Path to dictionary file (Default: english.utf_8.table)")
        args = parser.parse_args()

        file = args.file
        out = args.file
        if args.o:
            out = args.o

        dic = "dic/ja/japanese.utf_8.table"
        if args.d:
            dic = args.d

        if args.mode == "label":
            if file[-4:] != ".xml":
                file = file + ".xml"
            if out[-4:] != ".lab":
                out = out + ".lab"
            genMonoLabel(file, out, dic)
        if args.mode == "lab2grid":
            if file[-4:] != ".lab":
                file = file + ".lab"
            if out[-9:].lower() != ".textgrid":
                out = out + ".textgrid"
            lab2grid(file, out)
        if args.mode == "grid2lab":
            if file[-9:].lower() != ".textgrid":
                file = file + ".textgrid"
            if out[-4:] != ".lab":
                out = out + ".lab"
            grid2lab(file, out)

        print(args.mode)
        print(args.file)
        print(args.o)
        return 1

    def playAction(self):
        w = QWidget()

        # Show a message box
        result = QMessageBox.information(w, 'SiVo', "Synthesize.....")


def main():

    app = QtGui.QApplication(sys.argv)

    mui = mainUI()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
