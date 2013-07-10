from Tkinter import *
import Tkinter
import glob
import os
import tkFileDialog

class Rename:
    '''
    The base class for renaming files
    '''
    
    def __init__(self, name, oldpath, newpath, useStartingNumber, startingNumber, startingNumberDigits, splitStarting, bracketsStarting, endingNumber, endingNumberDigits, splitEnding, bracketsEnding, extensionCase, jpgCase):
        self.name = name
        self.oldpath = oldpath
        self.newpath = newpath
        self.useStartingNumber = useStartingNumber
        self.startingNumber = startingNumber
        self.startingNumberDigits = startingNumberDigits
        self.splitStarting = splitStarting
        self.bracketsStarting = bracketsStarting
        self.endingNumber = endingNumber
        self.endingNumberDigits = endingNumberDigits
        self.splitEnding = splitEnding
        self.bracketsEnding = bracketsEnding
        self.extensionCase = extensionCase
        self.jpgCase = jpgCase
    
    def renameFiles(self):
        for pathAndFilename in glob.iglob(os.path.join(self.oldpath + '/', r'*.*')):
            if self.useStartingNumber:
                numberedName = ''
                if self.bracketsStarting:
                    numberedName += '('
                a = len(numberedName)
                while a + self.startingNumberDigits - len(numberedName) - len(str(self.startingNumber)) > 0:
                    numberedName += '0'
                numberedName += str(self.startingNumber)
                if self.bracketsStarting:
                    numberedName += ')'
                numberedName += self.splitStarting + self.name + self.splitEnding
            else:
                numberedName = self.name + self.splitEnding
            if self.bracketsEnding:
                numberedName += '('
            length = len(numberedName)
            while length + self.endingNumberDigits - len(numberedName) - len(str(self.endingNumber)) > 0:
                numberedName += '0'
            numberedName += str(self.endingNumber)
            if self.bracketsEnding:
                numberedName += ')'
            splitPathAndFileName = pathAndFilename.split('.')
            if self.jpgCase is 0:
                if self.extensionCase is 0:
                    extension = splitPathAndFileName[-1]
                elif self.extensionCase is 1:
                    extension = splitPathAndFileName[-1].upper()
                else:
                    extension = splitPathAndFileName[-1].lower()
            elif self.jpgCase is 1:
                if self.extensionCase is 0:
                    extension = splitPathAndFileName[-1]
                    if extension.lower().endswith('jpeg'):
                        extension = 'jpg'
                elif self.extensionCase is 1:
                    extension = splitPathAndFileName[-1].upper()
                    if extension.endswith('JPEG'):
                        extension = 'JPG'
                else:
                    extension = splitPathAndFileName[-1].lower()
                    if extension.endswith('jpeg'):
                        extension = 'jpg'
            else:
                if self.extensionCase is 0:
                    extension = splitPathAndFileName[-1]
                    if extension.lower().endswith('jpg'):
                        extension = 'jpeg'
                elif self.extensionCase is 1:
                    extension = splitPathAndFileName[-1].upper()
                    if extension.endswith('JPG'):
                        extension = 'JPEG'
                else:
                    extension = splitPathAndFileName[-1].lower()
                    if extension.endswith('jpg'):
                        extension = 'jpeg'
            os.renames(pathAndFilename, self.newpath + '/' + numberedName + '.' + extension)
            self.endingNumber += 1
            self.startingNumber += 1

def select():
    if frameSelectionVar.get() is 0:
        viewStandardFrame()
    elif frameSelectionVar.get() is 1:
        viewAdvancedFrame()
    else:
        noFrame()

def createStandardFrame():
    nameLabel = Label(normalFrame, text="Name")
    nameLabel.grid(row=0, column=0, sticky=E)
    nameBox.grid(row=0, column=1, sticky=W)
    
    fromLabel = Label(normalFrame, text="From")
    fromLabel.grid(row=1, column=0, sticky=E)
    fromBox = Entry(normalFrame, width=40, textvariable=oldPathVar)
    fromBox.grid(row=1, column=1, sticky=W, columnspan=2)    
    fromButton = Button(normalFrame, text="Browse...", command=oldDirectory)
    fromButton.grid(row=1, column=3, sticky=W)
    
    toLabel = Label(normalFrame, text="To")
    toLabel.grid(row=2, column=0, sticky=E)
    toBox = Entry(normalFrame, width=40, textvariable=newPathVar)
    toBox.grid(row=2, column=1, sticky=W, columnspan=2)    
    toButton = Button(normalFrame, text="Browse...", command=newDirectory)
    toButton.grid(row=2, column=3, sticky=W)
    
    example = Label(normalFrame, text="Example : ", pady=15)
    example.grid(row=4, column=0, sticky=W)
    egLabel = Label(normalFrame, textvariable=egNameVar, padx=0, pady=15)
    egLabel.grid(row=4, column=1, sticky=E)
    exLabel = Label(normalFrame, text="001.*", padx=0, pady=15)
    exLabel.grid(row=4, column=2, sticky=W)
    
    RENAME = Button(normalFrame, text="Rename Files", command=renameFiles)
    RENAME.grid(row=5, column=3)
    
def viewStandardFrame():
    improvedFrame.grid_forget()
    normalFrame.grid(row=3, column=0, columnspan=3)

def createAdvancedFrame():
    nameLabel = Label(improvedFrame, text="Name")
    nameLabel.grid(row=0, column=0, sticky=E)
    nameBox2.grid(row=0, column=1, sticky=W)
    nameCheck = Checkbutton(improvedFrame, text="use origin folder name", variable=folderNameVar, onvalue=1, offvalue=0, command=updateAdvanced)
    nameCheck.grid(row=0, column=2, columnspan=2, sticky=W)
    
    fromLabel = Label(improvedFrame, text="From")
    fromLabel.grid(row=1, column=0, sticky=E)
    fromBox = Entry(improvedFrame, width=45, textvariable=oldPathVar)
    fromBox.grid(row=1, column=1, sticky=W, columnspan=2)    
    fromButton = Button(improvedFrame, text="Browse...", command=oldDirectory)
    fromButton.grid(row=1, column=3, sticky=W)
    
    toLabel = Label(improvedFrame, text="To")
    toLabel.grid(row=2, column=0, sticky=E)
    toBox = Entry(improvedFrame, width=45, textvariable=newPathVar)
    toBox.grid(row=2, column=1, sticky=W, columnspan=2)    
    toButton = Button(improvedFrame, text="Browse...", command=newDirectory)
    toButton.grid(row=2, column=3, sticky=W)
    
    extensionOptions = ('original extension', 'CAPITALIZED extension', 'lower case extension')
    for c in range(3):
        Tkinter.Radiobutton(improvedFrame, text=extensionOptions[c], variable=extensionLetters, value=c, command=updateAdvanced).grid(row=3, column=c + 1, sticky=W)
    extensionRenameOptions = ('no renaming', '.jpeg renamed to .jpg', '.jpg renamed to .jpeg')
    for c in range(3):
        Tkinter.Radiobutton(improvedFrame, text=extensionRenameOptions[c], variable=extensionRename, value=c, command=updateAdvanced).grid(row=4, column=c + 1, sticky=W)
    
    
    numberFrame.grid(row=5, column=0, columnspan=4, sticky=N)
    
    startingNumberFrame.grid(row=0, column=0, sticky=N)
    useStartingCheck = Checkbutton(startingNumberFrame, text="use starting number", variable=startingNumberVar, onvalue=1, offvalue=0, command=updateAdvanced)
    useStartingCheck.grid(row=1, column=1, columnspan=2, sticky=W)
    startingBracketsCheck.grid(row=2, column=1, columnspan=2, sticky=W)
    startingSeperatorFrame.grid(row=3, column=1, columnspan=2, sticky=N)
    startingSeperatorRButton0.grid(row=0, column=0, sticky=W, padx=10)
    startingSeperatorRButton1.grid(row=1, column=0, sticky=W, padx=10)
    startingSeperatorRButton2.grid(row=2, column=0, sticky=W, padx=10)
    startingSeperatorRButton3.grid(row=3, column=0, sticky=W, padx=10)
    startingSeperatorRButton4.grid(row=4, column=0, sticky=W, padx=10)
    startingSmartDigitsCheck.grid(row=4, column=1, columnspan=2, sticky=W)
    startingNumberDigitsScale.grid(row=5, column=1, columnspan=2, sticky=W)
    startingLabel = Label(startingNumberFrame, text="Start at")
    startingLabel.grid(row=6, column=1, sticky=E)
    startingNumberBox.grid(row=6, column=2, columnspan=2, sticky=W)
    startingNumberStartCheck.grid(row=7, column=1, columnspan=2, sticky=W)
    
    endingNumberFrame.grid(row=0, column=1, sticky=N)
    space = Label(endingNumberFrame, text="", pady=3)
    space.grid(row=1, column=1)
    endingBracketsCheck = Checkbutton(endingNumberFrame, text="parenthesis", variable=endingBracketsVar, onvalue=1, offvalue=0, command=updateAdvanced)
    endingBracketsCheck.grid(row=2, column=1, columnspan=2, sticky=W)
    endingSeperatorFrame.grid(row=3, column=1, columnspan=2, sticky=N)
    endingSeperatorRButton0 = Radiobutton(endingSeperatorFrame, text='None', variable=endingSeperatorVar, value=0, command=updateAdvanced)
    endingSeperatorRButton1 = Radiobutton(endingSeperatorFrame, text='Space\t\t" "', variable=endingSeperatorVar, value=1, command=updateAdvanced)
    endingSeperatorRButton2 = Radiobutton(endingSeperatorFrame, text='Hyphen\t\t"-"', variable=endingSeperatorVar, value=2, command=updateAdvanced)
    endingSeperatorRButton3 = Radiobutton(endingSeperatorFrame, text='underscore\t"_"', variable=endingSeperatorVar, value=3, command=updateAdvanced)
    endingSeperatorRButton4 = Radiobutton(endingSeperatorFrame, text='Spacehyphen\t" - "', variable=endingSeperatorVar, value=4, command=updateAdvanced)
    endingSeperatorRButton0.grid(row=0, column=0, sticky=W, padx=10)
    endingSeperatorRButton1.grid(row=1, column=0, sticky=W, padx=10)
    endingSeperatorRButton2.grid(row=2, column=0, sticky=W, padx=10)
    endingSeperatorRButton3.grid(row=3, column=0, sticky=W, padx=10)
    endingSeperatorRButton4.grid(row=4, column=0, sticky=W, padx=10)
    endingSmartDigitsCheck = Checkbutton(endingNumberFrame, text="use Smart Digits", variable=endingSmartDigits, onvalue=1, offvalue=0, command=updateAdvanced)
    endingSmartDigitsCheck.grid(row=4, column=1, columnspan=2, sticky=W)
    endingNumberDigitsScale = Scale(endingNumberFrame, variable=endingNumberDigits, orient=HORIZONTAL, from_=1, to=8, tickinterval=1, length=200, command=updateAdvanced)
    endingNumberDigitsScale.grid(row=5, column=1, columnspan=2, sticky=W)
    endingLabel = Label(endingNumberFrame, text="Start at")
    endingLabel.grid(row=6, column=1, sticky=E)
    endingNumberBox = Entry(endingNumberFrame, textvariable=endingNumberStart, width=5)
    endingNumberBox.grid(row=6, column=2, columnspan=2, sticky=W)
    endingNumberStartCheck = Checkbutton(endingNumberFrame, text="start from previous", variable=endingNumberStartVar, onvalue=1, offvalue=0, command=updateAdvanced)
    endingNumberStartCheck.grid(row=7, column=1, columnspan=2, sticky=W)
    
    example = Label(improvedFrame, text="Example : ", pady=15)
    example.grid(row=6, column=0, sticky=W)
    egLabel = Label(improvedFrame, textvariable=egNameVar2, padx=0, pady=15)
    egLabel.grid(row=6, column=1, sticky=N, columnspan=2)
    
    BATCH = Button(improvedFrame, text="ADD to Batch", command=addBatchItem)
    BATCH.grid(row=7, column=2, sticky=E)
    RENAME = Button(improvedFrame, text="ADD and Rename All", command=renameFiles)
    RENAME.grid(row=7, column=3, sticky=W)
    
def updateAdvanced(*args):  
    exampleName = ''
    if startingNumberVar.get() is 0:
        startingBracketsCheck.configure(state="disabled")
        startingBracketsCheck.update()
        startingSeperatorRButton0.configure(state="disabled")
        startingSeperatorRButton0.update()
        startingSeperatorRButton1.configure(state="disabled")
        startingSeperatorRButton1.update()
        startingSeperatorRButton2.configure(state="disabled")
        startingSeperatorRButton2.update()
        startingSeperatorRButton3.configure(state="disabled")
        startingSeperatorRButton3.update()
        startingSeperatorRButton4.configure(state="disabled")
        startingSeperatorRButton4.update()
        startingSmartDigitsCheck.configure(state="disabled")
        startingSmartDigitsCheck.update()
        startingNumberBox.configure(state="disabled")
        startingNumberBox.update()
        startingNumberStartCheck.configure(state="disabled")
        startingNumberStartCheck.update()
    else:
        startingBracketsCheck.configure(state="normal")
        startingBracketsCheck.update()
        startingSeperatorRButton0.configure(state="normal")
        startingSeperatorRButton0.update()
        startingSeperatorRButton1.configure(state="normal")
        startingSeperatorRButton1.update()
        startingSeperatorRButton2.configure(state="normal")
        startingSeperatorRButton2.update()
        startingSeperatorRButton3.configure(state="normal")
        startingSeperatorRButton3.update()
        startingSeperatorRButton4.configure(state="normal")
        startingSeperatorRButton4.update()
        startingSmartDigitsCheck.configure(state="normal")
        startingSmartDigitsCheck.update()
        startingNumberBox.configure(state="normal")
        startingNumberBox.update()
        startingNumberStartCheck.configure(state="normal")
        startingNumberStartCheck.update()
        a = 0
        if startingBracketsVar.get() is 1:
            exampleName += '('
            a = 1
        z = 1
        if startingNumberStart.get().isdigit():
            z = int(startingNumberStart.get())
        while a + getStartingNumberDigits() - len(str(z)) - len(exampleName) > 0:
            exampleName += '0'
        exampleName += str(z)
        if startingBracketsVar.get() is 1:
            exampleName += ')'
        if startingSeperatorVar.get() is 1:
            exampleName += ' '
        elif startingSeperatorVar.get() is 2:
            exampleName += '-'
        elif startingSeperatorVar.get() is 3:
            exampleName += '_'
        elif startingSeperatorVar.get() is 4:
            exampleName += ' - '
    if folderNameVar.get() is 1:
        nameBox2.configure(state="disabled")
        nameBox2.update()
    else:
        nameBox2.configure(state="normal")
        nameBox2.update()
    exampleName += getName()
    if endingSeperatorVar.get() is 1:
        exampleName += ' '
    elif endingSeperatorVar.get() is 2:
        exampleName += '-'
    elif endingSeperatorVar.get() is 3:
        exampleName += '_'
    elif endingSeperatorVar.get() is 4:
        exampleName += ' - '
    if endingBracketsVar.get() is 1:
        exampleName += '('
    y = len(exampleName)
    x = 1
    if endingNumberStart.get().isdigit():
        x = int(endingNumberStart.get())
    while y + getEndingNumberDigits() - len(str(x)) - len(exampleName) > 0:
        exampleName += '0'
    exampleName += str(x)
    if endingBracketsVar.get() is 1:
        exampleName += ')'
    if extensionRename.get() is 0:
        if extensionLetters.get() is 0:
            exampleName += '.XTension'
        elif extensionLetters.get() is 1:
            exampleName += '.XTENSION'
        elif extensionLetters.get() is 2:
            exampleName += '.xtension'
    elif extensionRename.get() is 1:
        if extensionLetters.get() is 0:
            exampleName += '.XTnsion'
        elif extensionLetters.get() is 1:
            exampleName += '.XTNSION'
        elif extensionLetters.get() is 2:
            exampleName += '.xtnsion'
    elif extensionRename.get() is 2:
        if extensionLetters.get() is 0:
            exampleName += '.EXTension'
        elif extensionLetters.get() is 1:
            exampleName += '.EXTENSION'
        elif extensionLetters.get() is 2:
            exampleName += '.extension'
    egNameVar2.set(exampleName)
    
def viewAdvancedFrame():
    normalFrame.grid_forget()
    improvedFrame.grid(row=3, column=0, columnspan=3)

def noFrame():
    normalFrame.grid_forget()
    improvedFrame.grid_forget()

def renameFiles():
    addBatchItem()
    for batch in batchList:
        batch[0].renameFiles()
    del batchList[:]

def oldDirectory():
    f = tkFileDialog.askdirectory()
    oldPathVar.set(str(f))
def newDirectory():
    f = tkFileDialog.askdirectory()
    newPathVar.set(str(f))
    
def getStartingNumberDigits():
    if startingSmartDigits.get() is 0:
        return startingNumberDigits.get()
    else:
        amount = 0
        for pathAndFilename in glob.iglob(os.path.join(oldPathVar.get()+'/', r'*.*')):
            amount += 1
        return len(str(amount))

def getEndingNumberDigits():
    if endingSmartDigits.get() is 0:
        return endingNumberDigits.get()
    else:
        amount = 0
        for pathAndFilename in glob.iglob(os.path.join(oldPathVar.get()+'/', r'*.*')):
            amount += 1
        return len(str(amount))

def getName():
    if folderNameVar.get() is 0:
        return egNameVar.get()
    else:
        return max(oldPathVar.get().split('/'))

def addBatchItem():
    numberOfFiles = 0
    for pathAndFilename in glob.iglob(os.path.join(oldPathVar.get()+'/', r'*.*')):
        numberOfFiles += 1
        
    if startingNumberVar.get() is 0:
        STARTING = False
    else:
        STARTING = True
        
    if startingNumberStartVar.get() is 0:
        STARTINGNUMBER = 1
        if startingNumberStart.get().isdigit():
            STARTINGNUMBER = int(startingNumberStart.get())
    else:
        STARTINGNUMBER = 0
        for someItem in batchList:
            STARTINGNUMBER += someItem[1]
        if STARTINGNUMBER is 0:
            STARTINGNUMBER = 1
    
    splitStarting = ''
    if startingSeperatorVar.get() is 1:
        splitStarting = ' '
    elif startingSeperatorVar.get() is 2:
        splitStarting = '-'
    elif startingSeperatorVar.get() is 3:
        splitStarting = '_'
    elif startingSeperatorVar.get() is 4:
        splitStarting = ' - '
        
    if startingBracketsVar.get() is 0:
        bracketsStarting = False
    else:
        bracketsStarting = True
    
    if endingNumberStartVar.get() is 0:
        ENDINGNUMBER = 1
        if endingNumberStart.get().isdigit():
            ENDINGNUMBER = int(endingNumberStart.get())
    else:
        ENDINGNUMBER = 0
        for someItem in batchList:
            ENDINGNUMBER += someItem[1]
        if ENDINGNUMBER is 0:
            ENDINGNUMBER = 1
    
    splitEnding = ''
    if endingSeperatorVar.get() is 1:
        splitEnding = ' '
    elif endingSeperatorVar.get() is 2:
        splitEnding = '-'
    elif endingSeperatorVar.get() is 3:
        splitEnding = '_'
    elif endingSeperatorVar.get() is 4:
        splitEnding = ' - '
        
    if endingBracketsVar.get() is 0:
        bracketsEnding = False
    else:
        bracketsEnding = True
    
    item = Rename(getName(), oldPathVar.get(), newPathVar.get(), STARTING, STARTINGNUMBER, getStartingNumberDigits(), splitStarting, bracketsStarting, ENDINGNUMBER, getEndingNumberDigits(), splitEnding, bracketsEnding, extensionLetters.get(), extensionRename.get())
    batchList.append((item, numberOfFiles))

root = Tk()
root.title("IMProved Renaming")
root.iconbitmap(default="icon.ico")
frameSelectionVar = IntVar()
egNameVar = StringVar()
egNameVar.set("name")
egNameVar2 = StringVar()
oldPathVar = StringVar()
newPathVar = StringVar()

normalFrame = Frame(root)
improvedFrame = Frame(root)
numberFrame = Frame(improvedFrame)
startingNumberFrame = LabelFrame(numberFrame, text="Starting Number", labelanchor=N)
startingSeperatorFrame = LabelFrame(startingNumberFrame, text="Separator", labelanchor=N)
endingNumberFrame = LabelFrame(numberFrame, text="Ending Number", labelanchor=N)
endingSeperatorFrame = LabelFrame(endingNumberFrame, text="Separator", labelanchor=N)

folderNameVar = IntVar()
extensionLetters = IntVar()
extensionRename = IntVar()

startingNumberVar = IntVar()
startingBracketsVar = IntVar()
startingBracketsCheck = Checkbutton(startingNumberFrame, text="parenthesis", variable=startingBracketsVar, onvalue=1, offvalue=0, command=updateAdvanced)
startingSeperatorVar = IntVar()
startingSeperatorRButton0 = Radiobutton(startingSeperatorFrame, text='None', variable=startingSeperatorVar, value=0, command=updateAdvanced)
startingSeperatorRButton1 = Radiobutton(startingSeperatorFrame, text='Space\t\t" "', variable=startingSeperatorVar, value=1, command=updateAdvanced)
startingSeperatorRButton2 = Radiobutton(startingSeperatorFrame, text='Hyphen\t\t"-"', variable=startingSeperatorVar, value=2, command=updateAdvanced)
startingSeperatorRButton3 = Radiobutton(startingSeperatorFrame, text='underscore\t"_"', variable=startingSeperatorVar, value=3, command=updateAdvanced)
startingSeperatorRButton4 = Radiobutton(startingSeperatorFrame, text='Spacehyphen\t" - "', variable=startingSeperatorVar, value=4, command=updateAdvanced)
startingSmartDigits = IntVar()
startingSmartDigitsCheck = Checkbutton(startingNumberFrame, text="use Smart Digits", variable=startingSmartDigits, onvalue=1, offvalue=0, command=updateAdvanced)
startingNumberDigits = IntVar()
startingNumberDigitsScale = Scale(startingNumberFrame, variable=startingNumberDigits, orient=HORIZONTAL, from_=1, to=8, tickinterval=1, length=200, command=updateAdvanced)
startingNumberStart = StringVar()
startingNumberBox = Entry(startingNumberFrame, textvariable=startingNumberStart, width=5)
startingNumberStartVar = IntVar()
startingNumberStartCheck = Checkbutton(startingNumberFrame, text="start from previous", variable=startingNumberStartVar, onvalue=1, offvalue=0, command=updateAdvanced)

endingBracketsVar = IntVar()
endingSeperatorVar = IntVar()
endingSmartDigits = IntVar()
endingNumberDigits = IntVar()
endingNumberDigits.set(3)
endingNumberStart = StringVar()
endingNumberStartVar = IntVar()

nameBox = Entry(normalFrame, textvariable=egNameVar)
nameBox2 = Entry(improvedFrame, textvariable=egNameVar)

frameOptions = ('Standard Options', 'Improved Options', 'No Options')
for c in range(3):
    Tkinter.Radiobutton(root, text=frameOptions[c], variable=frameSelectionVar, value=c, command=select).grid(row=2, column=c, sticky=NW, ipadx=10)
    
batchList = []

createStandardFrame()
createAdvancedFrame()
updateAdvanced()
viewStandardFrame()
root.mainloop()

