import xml.etree.ElementTree as ET
import argparse

def trimSpace(st):
    while len(st) > 0 and (st[0] == " " or st[0] == "\n") :
        st = st[1:]
    while len(st) > 0 and (st[-1] == " " or st[-1] == "\n"):
        st = st[:-1]
    return st


def genMonoLabel(name, out, df):
    #Read xml
    try:
        tree = ET.parse(name)
    except:
        raise Exception("File " + str(name) + " does not exist")
    root = tree.getroot()

    parts = []
    for child in root:
        #print (child.tag, child.attrib)
        if child.tag.lower() == "part":
            parts.append(child)
            #print ("haha")

    measures = []
    for i in parts:
        for j in i:
            #print (j.tag, j.attrib)
            if j.tag.lower() == "measure":
                measures.append(j)


    ##print
    ##direct = []
    ##for i in measures[0]:
    ##    print i.tag, i.attrib
    ##    if i.tag.lower() == "direction":
    ##        direct = i
    ##    if i.tag.lower() == "note":
    ##        notes.append(i)
    ##        print "aaa"
    ##for i in notes[-1]:
    ##    print i.tag, i.attrib
    ##
    ##print "\n"
    ##print notes[-1][0][0].text
    #note struct
    #([measure], [duration], tempo, [step], [octave], word, [parts]) this is for per word

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
    #Add code to read scale later T_T (needed to correctly identify sharps and flats)

    for measure in measures:
        mNo = measure.attrib["number"]
        for part in measure:
            if part.tag.lower() == "direction":
                for tg in part:
                    if tg.tag.lower() == "sound":
                        #print (mNo)
                        try:
                            tempo = float(tg.attrib["tempo"])
                        except:
                            pass
                        #print (tempo)
            if part.tag.lower() == "sound":
                        tempo = float(part.attrib["tempo"])
                        #print (tempo)
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
                    notes.append( (tMes, tDur, tempo, tStep, tOctave, tWord, tPart) )
                    tOctave = []
                    tStep = []
                    tWord = ""
                    tPart = []
                    tSyl = ""
                    tDur = []
                    tMes = []

    #note struct
    #([measure], [duration], tempo, [step], [octave], word, [parts]) this is for per word

    #load dictionary
    dic = {"ppppp":"pau"}
    try:
        with open(df) as fp:
            for line in fp:
                word = ""
                phons = ""
                for i in range(0, len(line)):
                    if line[i] == " ":
                        phons = line[i+1:-1]
                        break
                    word += line[i]
                #print word
                dic[word] = trimSpace(phons)
    except:
        raise Exception("Cannot locate " + df + "\nMake sure it is in the same directory as monoLabel.py")

    last = 0.0
    dur = 0
    phons = []
    mp = []
    for i in notes:
        lng = 0
        phons = []
        tempoScal = 1.0/i[2]*60.0
        pts = 0.0
        dur = 0
        for j in i[1]:
            dur += (j/4.0)*tempoScal
        try:
            #print i[5], dic[i[5]]
            phons = dic[i[5]].split(" ")
        except:
            print ("Warning!!!\nWord not in dictionary: " + i[5])
            phons = [i[5]]
        pts = dur/float(len(phons))
        for i in phons:
            mp.append((last, last+pts, i))
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

    #lab = open("outLab.Audacity.lab", 'w')
    #for i in mp2:
    #    lab.write(str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n")
    #lab.close()
        
    lab = open(out, 'w')
    for i in mp2:
        lab.write(str(int(i[0]*10000000)) + " " + str(int(i[1]*10000000)) + " " + str(i[2]) + "\n")
    lab.close()

    return 1

def lab2grid(file, out):
    labs = []
    try:
        with open(file) as fp:
            for line in fp:
                ln = line.split(" ")
                labs.append( (float(ln[0]), float(ln[1]), ln[2]) )
    except:
        raise Exception("File " + file + " does not exist or is in the wrong format")
    grid = open(out, 'w')
    grid.write("File type = \"ooTextFile\"\n")
    grid.write("Object class = \"TextGrid\"\n")
    grid.write("\n0\n")
    grid.write(str(labs[-1][1]/10000000.0)+"\n")
    grid.write("<exists>\n")
    grid.write("1\n")
    grid.write("\"IntervalTier\"\n")
    grid.write("\"words\"\n")
    grid.write("0\n")
    grid.write(str(labs[-1][1]/10000000.0)+"\n")
    grid.write(str(int(len(labs)))+"\n")
    for i in labs:
        grid.write(str(i[0]/10000000.0)+"\n")
        grid.write(str(i[1]/10000000.0)+"\n")
        grid.write("\""+trimSpace(i[2])+"\"\n")
    grid.close()
                
def grid2lab(file, out):
    try:
        grid = open(file, 'r')
    except:
        raise Exception("File " + file + " does not exist")
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
    grid.readline()#xmax
    grid.readline()#exists
    grid.readline()#1
    grid.readline()#interval
    grid.readline()#words
    grid.readline()#xmin
    grid.readline()#xm
    grid.readline()#count
    labs = []
    
    temp = trimSpace(grid.readline())
    while temp != "":
        labs.append( ( float(temp)*10000000, float(trimSpace(grid.readline()))*10000000, trimSpace(grid.readline())[1:-1] ) )
        temp = trimSpace(grid.readline())
    grid.close()

    lab = open(out, 'w')
    for i in labs:
        lab.write(str(int(i[0])) + " " + str(int(i[1])) + " " + str(i[2]) + "\n")
    lab.close()
    
    
def main():
    parser = argparse.ArgumentParser(description="Utility program for Mono Labeling. Please use short text TextGrids and HTK labels only.")
    parser.add_argument("mode", help="Specify operation mode", choices=["label", "lab2grid", "grid2lab"])
    parser.add_argument("file", help="Path to file")
    parser.add_argument("-o", help="Output file")
    parser.add_argument("-d", help="Path to dictionary file (Default: english.utf_8.table)")
    args = parser.parse_args()

    file = args.file
    out = args.file
    if args.o:
        out = args.o

    dic = "english.utf_8.table"
    if args.d:
        dic = args.d
    
    if args.mode == "label":
        if file[-4:] != ".xml":
            file = file+".xml"
        if out[-4:] != ".lab":
            out = out+".lab"
        genMonoLabel(file, out, dic)
    if args.mode == "lab2grid":
        if file[-4:] != ".lab":
            file = file+".lab"
        if out[-9:].lower() != ".textgrid":
            out = out+".textgrid"
        lab2grid(file, out)
    if args.mode == "grid2lab":
        if file[-9:].lower() != ".textgrid":
            file = file+".textgrid"
        if out[-4:] != ".lab":
            out = out+".lab"
        grid2lab(file, out)
        
        
    #print (args.mode)
    #print(args.file)
    #print(args.o)
    return 1


if __name__ == "__main__":
    main()
