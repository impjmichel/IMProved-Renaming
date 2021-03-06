'''
Created on Jul 8, 2013
Last version update: Aug 3, 2013
@author: Johannes [imp] Michel
'''
from Tkinter import *
import Tkinter
import glob
import os
import tkFileDialog

class App():
    '''
    Class for the renaming application (GUI)
    '''
    def __init__(self):
#         all needed frames:
        self.root = Tk()
        self.root.title("IMProved Renaming")
        self.root.iconbitmap(default="icon.ico")
        self.standardFrame = Frame(self.root)
        self.improvedFrame = Frame(self.root)
        self.batchFrame = Frame(self.root)
        self.numberFrame = Frame(self.improvedFrame)
        self.startingNumberFrame = LabelFrame(self.numberFrame, text="Starting Number", labelanchor=N)
        self.startingSeperatorFrame = LabelFrame(self.startingNumberFrame, text="Separator", labelanchor=N)
        self.endingNumberFrame = LabelFrame(self.numberFrame, text="Ending Number", labelanchor=N)
        self.endingSeperatorFrame = LabelFrame(self.endingNumberFrame, text="Separator", labelanchor=N)
        
#         all needed variables:
        self.frameSelectionVar = IntVar()
        self.egNameVar = StringVar()
        self.egNameVar.set("name")
        self.egNameVar2 = StringVar()
        self.oldPathVar = StringVar()
        self.newPathVar = StringVar()
        self.folderNameVar = IntVar()
        self.extensionLetters = IntVar()
        self.extensionRename = IntVar()
        self.totalCountVar = StringVar()
        self.totalCountVar.set("0")

        self.startingNumberVar = IntVar()
        self.startingBracketsVar = IntVar()
        self.startingBracketsCheck = Checkbutton(self.startingNumberFrame, text="Parenthesis", variable=self.startingBracketsVar, onvalue=1, offvalue=0, command=self.updateImproved)
        self.startingSeperatorVar = IntVar()
        self.startingSeperatorRButton0 = Radiobutton(self.startingSeperatorFrame, text='None', variable=self.startingSeperatorVar, value=0, command=self.updateImproved)
        self.startingSeperatorRButton1 = Radiobutton(self.startingSeperatorFrame, text='Space\t\t" "', variable=self.startingSeperatorVar, value=1, command=self.updateImproved)
        self.startingSeperatorRButton2 = Radiobutton(self.startingSeperatorFrame, text='Hyphen\t\t"-"', variable=self.startingSeperatorVar, value=2, command=self.updateImproved)
        self.startingSeperatorRButton3 = Radiobutton(self.startingSeperatorFrame, text='Underscore\t"_"', variable=self.startingSeperatorVar, value=3, command=self.updateImproved)
        self.startingSeperatorRButton4 = Radiobutton(self.startingSeperatorFrame, text='Spacehyphen\t" - "', variable=self.startingSeperatorVar, value=4, command=self.updateImproved)
        self.startingSmartDigits = IntVar()
        self.startingSmartDigitsCheck = Checkbutton(self.startingNumberFrame, text="Use Smart Digits", variable=self.startingSmartDigits, onvalue=1, offvalue=0, command=self.updateImproved)
        self.startingNumberDigits = IntVar()
        self.startingNumberDigitsScale = Scale(self.startingNumberFrame, variable=self.startingNumberDigits, orient=HORIZONTAL, from_=1, to=8, tickinterval=1, length=200, command=self.updateImproved)
        self.startingNumberStart = StringVar()
        self.startingNumberBox = Entry(self.startingNumberFrame, textvariable=self.startingNumberStart, width=5)
        self.startingNumberStartVar = IntVar()
        self.startingNumberStartCheck = Checkbutton(self.startingNumberFrame, text="Start from previous", variable=self.startingNumberStartVar, onvalue=1, offvalue=0, command=self.updateImproved)

        self.endingBracketsVar = IntVar()
        self.endingSeperatorVar = IntVar()
        self.endingSmartDigits = IntVar()
        self.endingNumberDigits = IntVar()
        self.endingNumberDigits.set(3)
        self.endingNumberStart = StringVar()
        self.endingNumberStartVar = IntVar()
        
#         the batch
        self.batchList = []
#         create everything:
        self.nameBox = Entry(self.root, textvariable=self.egNameVar)
        self.createRootFrame()
        self.createStandardFrame()
        self.createImprovedFrame()
        self.createBatchFrame()
        self.updateImproved()
        self.viewStandardFrame()
        self.updateStandardFrame()
        self.root.resizable(False, False)
        self.root.mainloop()
        
    def select(self):
        if self.frameSelectionVar.get() is 0:
            self.viewStandardFrame()
        else:
            self.viewImprovedFrame()

    def createRootFrame(self):    
        frameOptions = ('Standard Options', 'Improved Options')
        for c in range(len(frameOptions)):
            Tkinter.Radiobutton(self.root, text=frameOptions[c], variable=self.frameSelectionVar, value=c, command=self.select).grid(row=0, column=c + 1, sticky=NW, ipadx=10, ipady=10)
        
        nameLabel = Label(self.root, text="Name : ")
        nameLabel.grid(row=1, column=0, sticky=E)
        self.nameBox.grid(row=1, column=1, sticky=W)
        
        fromLabel = Label(self.root, text="From : ")
        fromLabel.grid(row=2, column=0, sticky=E)
        fromBox = Entry(self.root, width=50, textvariable=self.oldPathVar)
        fromBox.grid(row=2, column=1, sticky=W, columnspan=2)    
        fromButton = Button(self.root, text="Browse...", command=self.oldDirectory)
        fromButton.grid(row=2, column=2, sticky=E)
        
        toLabel = Label(self.root, text="To : ")
        toLabel.grid(row=3, column=0, sticky=E)
        toBox = Entry(self.root, width=50, textvariable=self.newPathVar)
        toBox.grid(row=3, column=1, sticky=W, columnspan=2)    
        toButton = Button(self.root, text="Browse...", command=self.newDirectory)
        toButton.grid(row=3, column=2, sticky=E)

    def createStandardFrame(self):    
        example = Label(self.standardFrame, text="Example : ", pady=15)
        example.grid(row=4, column=0, sticky=W)
        egLabel = Label(self.standardFrame, textvariable=self.egNameVar2, padx=0, pady=15)
        egLabel.grid(row=4, column=1, sticky=E)
        CLEAR = Button(self.standardFrame, text="Clear Batch", command=self.clearBatch)
        CLEAR.grid(row=5, column=1, sticky=W)
        BATCH = Button(self.standardFrame, text="Add to Batch", command=self.addBatchItem)
        BATCH.grid(row=5, column=2, sticky=E)
        RENAME = Button(self.standardFrame, text="Rename Batch", command=self.renameFiles)
        RENAME.grid(row=5, column=3, sticky=W)
    
    def viewStandardFrame(self):
        self.improvedFrame.grid_forget()
        self.standardFrame.grid(row=4, column=0, columnspan=3)

    def updateStandardFrame(self):
        self.updateBatchFrame()
        self.egNameVar2.set(self.getExampleName())
        self.root.after(1000, self.updateStandardFrame)

    def createImprovedFrame(self):
        nameCheck = Checkbutton(self.improvedFrame, text="Use origin folder name", variable=self.folderNameVar, onvalue=1, offvalue=0, command=self.updateImproved)
        nameCheck.grid(row=0, column=2, columnspan=2, sticky=W)
        
        extensionOptions = ('Original extension', 'CAPITALIZED extension', 'lower case extension')
        for c in range(3):
            Tkinter.Radiobutton(self.improvedFrame, text=extensionOptions[c], variable=self.extensionLetters, value=c, command=self.updateImproved).grid(row=3, column=c + 1, sticky=W)
        extensionRenameOptions = ('No renaming', '.jpeg renamed to .jpg', '.jpg renamed to .jpeg')
        for c in range(3):
            Tkinter.Radiobutton(self.improvedFrame, text=extensionRenameOptions[c], variable=self.extensionRename, value=c, command=self.updateImproved).grid(row=4, column=c + 1, sticky=W)
        
        self.numberFrame.grid(row=5, column=0, columnspan=4, sticky=N)
        
        self.startingNumberFrame.grid(row=0, column=0, sticky=N)
        useStartingCheck = Checkbutton(self.startingNumberFrame, text="Use starting number", variable=self.startingNumberVar, onvalue=1, offvalue=0, command=self.updateImproved)
        useStartingCheck.grid(row=1, column=1, columnspan=2, sticky=W)
        self.startingBracketsCheck.grid(row=2, column=1, columnspan=2, sticky=W)
        self.startingSeperatorFrame.grid(row=3, column=1, columnspan=2, sticky=N)
        self.startingSeperatorRButton0.grid(row=0, column=0, sticky=W, padx=10)
        self.startingSeperatorRButton1.grid(row=1, column=0, sticky=W, padx=10)
        self.startingSeperatorRButton2.grid(row=2, column=0, sticky=W, padx=10)
        self.startingSeperatorRButton3.grid(row=3, column=0, sticky=W, padx=10)
        self.startingSeperatorRButton4.grid(row=4, column=0, sticky=W, padx=10)
        self.startingSmartDigitsCheck.grid(row=4, column=1, columnspan=2, sticky=W)
        self.startingNumberDigitsScale.grid(row=5, column=1, columnspan=2, sticky=W)
        startingLabel = Label(self.startingNumberFrame, text="Start at")
        startingLabel.grid(row=6, column=1, sticky=E)
        self.startingNumberBox.grid(row=6, column=2, columnspan=2, sticky=W)
        self.startingNumberStartCheck.grid(row=7, column=1, columnspan=2, sticky=W)
        
        self.endingNumberFrame.grid(row=0, column=1, sticky=N)
        space = Label(self.endingNumberFrame, text="", pady=3)
        space.grid(row=1, column=1)
        endingBracketsCheck = Checkbutton(self.endingNumberFrame, text="Parenthesis", variable=self.endingBracketsVar, onvalue=1, offvalue=0, command=self.updateImproved)
        endingBracketsCheck.grid(row=2, column=1, columnspan=2, sticky=W)
        self.endingSeperatorFrame.grid(row=3, column=1, columnspan=2, sticky=N)
        endingSeperatorRButton0 = Radiobutton(self.endingSeperatorFrame, text='None', variable=self.endingSeperatorVar, value=0, command=self.updateImproved)
        endingSeperatorRButton1 = Radiobutton(self.endingSeperatorFrame, text='Space\t\t" "', variable=self.endingSeperatorVar, value=1, command=self.updateImproved)
        endingSeperatorRButton2 = Radiobutton(self.endingSeperatorFrame, text='Hyphen\t\t"-"', variable=self.endingSeperatorVar, value=2, command=self.updateImproved)
        endingSeperatorRButton3 = Radiobutton(self.endingSeperatorFrame, text='Underscore\t"_"', variable=self.endingSeperatorVar, value=3, command=self.updateImproved)
        endingSeperatorRButton4 = Radiobutton(self.endingSeperatorFrame, text='Spacehyphen\t" - "', variable=self.endingSeperatorVar, value=4, command=self.updateImproved)
        endingSeperatorRButton0.grid(row=0, column=0, sticky=W, padx=10)
        endingSeperatorRButton1.grid(row=1, column=0, sticky=W, padx=10)
        endingSeperatorRButton2.grid(row=2, column=0, sticky=W, padx=10)
        endingSeperatorRButton3.grid(row=3, column=0, sticky=W, padx=10)
        endingSeperatorRButton4.grid(row=4, column=0, sticky=W, padx=10)
        endingSmartDigitsCheck = Checkbutton(self.endingNumberFrame, text="use Smart Digits", variable=self.endingSmartDigits, onvalue=1, offvalue=0, command=self.updateImproved)
        endingSmartDigitsCheck.grid(row=4, column=1, columnspan=2, sticky=W)
        endingNumberDigitsScale = Scale(self.endingNumberFrame, variable=self.endingNumberDigits, orient=HORIZONTAL, from_=1, to=8, tickinterval=1, length=200, command=self.updateImproved)
        endingNumberDigitsScale.grid(row=5, column=1, columnspan=2, sticky=W)
        endingLabel = Label(self.endingNumberFrame, text="Start at")
        endingLabel.grid(row=6, column=1, sticky=E)
        endingNumberBox = Entry(self.endingNumberFrame, textvariable=self.endingNumberStart, width=5)
        endingNumberBox.grid(row=6, column=2, columnspan=2, sticky=W)
        endingNumberStartCheck = Checkbutton(self.endingNumberFrame, text="start from previous", variable=self.endingNumberStartVar, onvalue=1, offvalue=0, command=self.updateImproved)
        endingNumberStartCheck.grid(row=7, column=1, columnspan=2, sticky=W)
        
        example = Label(self.improvedFrame, text="Example : ", pady=15)
        example.grid(row=6, column=1, sticky=W)
        egLabel = Label(self.improvedFrame, textvariable=self.egNameVar2, padx=0, pady=15)
        egLabel.grid(row=6, column=2, sticky=N, columnspan=2)
        
        CLEAR = Button(self.improvedFrame, text="Clear Batch", command=self.clearBatch)
        CLEAR.grid(row=7, column=1, sticky=W)
        BATCH = Button(self.improvedFrame, text="Add to Batch", command=self.addBatchItem)
        BATCH.grid(row=7, column=2, sticky=E)
        RENAME = Button(self.improvedFrame, text="Rename Batch", command=self.renameFiles)
        RENAME.grid(row=7, column=3, sticky=W)
    
    def viewImprovedFrame(self):
        self.standardFrame.grid_forget()
        self.improvedFrame.grid(row=4, column=0, columnspan=3)
    
    def updateImproved(self, *args):
        self.updateBatchFrame()
        if self.startingNumberVar.get() is 0:
            self.startingBracketsCheck.configure(state="disabled")
            self.startingBracketsCheck.update()
            self.startingSeperatorRButton0.configure(state="disabled")
            self.startingSeperatorRButton0.update()
            self.startingSeperatorRButton1.configure(state="disabled")
            self.startingSeperatorRButton1.update()
            self.startingSeperatorRButton2.configure(state="disabled")
            self.startingSeperatorRButton2.update()
            self.startingSeperatorRButton3.configure(state="disabled")
            self.startingSeperatorRButton3.update()
            self.startingSeperatorRButton4.configure(state="disabled")
            self.startingSeperatorRButton4.update()
            self.startingSmartDigitsCheck.configure(state="disabled")
            self.startingSmartDigitsCheck.update()
            self.startingNumberBox.configure(state="disabled")
            self.startingNumberBox.update()
            self.startingNumberStartCheck.configure(state="disabled")
            self.startingNumberStartCheck.update()
        else:
            self.startingBracketsCheck.configure(state="normal")
            self.startingBracketsCheck.update()
            self.startingSeperatorRButton0.configure(state="normal")
            self.startingSeperatorRButton0.update()
            self.startingSeperatorRButton1.configure(state="normal")
            self.startingSeperatorRButton1.update()
            self.startingSeperatorRButton2.configure(state="normal")
            self.startingSeperatorRButton2.update()
            self.startingSeperatorRButton3.configure(state="normal")
            self.startingSeperatorRButton3.update()
            self.startingSeperatorRButton4.configure(state="normal")
            self.startingSeperatorRButton4.update()
            self.startingSmartDigitsCheck.configure(state="normal")
            self.startingSmartDigitsCheck.update()
            self.startingNumberBox.configure(state="normal")
            self.startingNumberBox.update()
            self.startingNumberStartCheck.configure(state="normal")
            self.startingNumberStartCheck.update()   
        if self.folderNameVar.get() is 1:
            self.nameBox.configure(state="disabled")
            self.nameBox.update()
        else:
            self.nameBox.configure(state="normal")
            self.nameBox.update()
        self.egNameVar2.set(self.getExampleName())

    def createBatchFrame(self):
        name = Label(self.batchFrame, text="Batch items:")
        name.grid(row=0, column=1, sticky=W)
        count = Label(self.batchFrame, text="file count:")
        count.grid(row=0, column=2, sticky=E)
        
        totalname = Label(self.batchFrame, text="total file count: ")
        totalname.grid(row=9000, column=1, sticky=E)
        totalcount = Label(self.batchFrame, textvariable=self.totalCountVar)
        totalcount.grid(row=9000, column=2, sticky=E)
        
    def updateBatchFrame(self):
        if len(self.batchList) is 0:
            self.batchFrame.grid_forget()
            self.batchFrame = Frame(self.root)
        else:
            self.createBatchFrame()
            self.batchFrame.grid(row=0, column=4, rowspan=5, sticky=N)
            rowCount = 0
            totalCount = 0
            for item in self.batchList:
                rowCount += 1
                number = Label(self.batchFrame, text=str(rowCount) + ")")
                number.grid(row=rowCount, column=0, sticky=W)
                label = Label(self.batchFrame, text=item[2])
                label.grid(row=rowCount, column=1, sticky=W)
                count = Label(self.batchFrame, text=item[1])
                count.grid(row=rowCount, column=2, sticky=E)
                totalCount += item[1]
            self.totalCountVar.set(str(totalCount))

    def oldDirectory(self):
        f = tkFileDialog.askdirectory()
        self.oldPathVar.set(str(f))
        if self.newPathVar.get() is "":
            self.newPathVar.set(str(f))
    def newDirectory(self):
        f = tkFileDialog.askdirectory()
        self.newPathVar.set(str(f))
    
    def getStartingNumberDigits(self):
        if self.startingSmartDigits.get() is 0:
            return self.startingNumberDigits.get()
        else:
            amount = 0
            for pathAndFilename in glob.iglob(os.path.join(self.oldPathVar.get() + '/', r'*.*')):
                amount += 1
            return len(str(amount))

    def getEndingNumberDigits(self):
        if self.endingSmartDigits.get() is 0:
            return self.endingNumberDigits.get()
        else:
            amount = 0
            for pathAndFilename in glob.iglob(os.path.join(self.oldPathVar.get() + '/', r'*.*')):
                amount += 1
            return len(str(amount))
    
    def getExampleName(self):
        exampleName = ''
        if self.startingNumberVar.get() is 1:
            if self.startingBracketsVar.get() is 1:
                exampleName += '('
            z = 1
            if self.startingNumberStart.get().isdigit():
                z = int(self.startingNumberStart.get())
            a = len(exampleName)
            while a + self.getStartingNumberDigits() - len(str(z)) - len(exampleName) > 0:
                exampleName += '0'
            exampleName += str(z)
            if self.startingBracketsVar.get() is 1:
                exampleName += ')'
            if self.startingSeperatorVar.get() is 1:
                exampleName += ' '
            elif self.startingSeperatorVar.get() is 2:
                exampleName += '-'
            elif self.startingSeperatorVar.get() is 3:
                exampleName += '_'
            elif self.startingSeperatorVar.get() is 4:
                exampleName += ' - '
        exampleName += self.getName()
        if self.endingSeperatorVar.get() is 1:
            exampleName += ' '
        elif self.endingSeperatorVar.get() is 2:
            exampleName += '-'
        elif self.endingSeperatorVar.get() is 3:
            exampleName += '_'
        elif self.endingSeperatorVar.get() is 4:
            exampleName += ' - '
        if self.endingBracketsVar.get() is 1:
            exampleName += '('
        y = len(exampleName)
        x = 1
        if self.endingNumberStart.get().isdigit():
            x = int(self.endingNumberStart.get())
        while y + self.getEndingNumberDigits() - len(str(x)) - len(exampleName) > 0:
            exampleName += '0'
        exampleName += str(x)
        if self.endingBracketsVar.get() is 1:
            exampleName += ')'
        if self.extensionRename.get() is 0:
            if self.extensionLetters.get() is 0:
                exampleName += '.XTension'
            elif self.extensionLetters.get() is 1:
                exampleName += '.XTENSION'
            elif self.extensionLetters.get() is 2:
                exampleName += '.xtension'
        elif self.extensionRename.get() is 1:
            if self.extensionLetters.get() is 0:
                exampleName += '.XTnsion'
            elif self.extensionLetters.get() is 1:
                exampleName += '.XTNSION'
            elif self.extensionLetters.get() is 2:
                exampleName += '.xtnsion'
        elif self.extensionRename.get() is 2:
            if self.extensionLetters.get() is 0:
                exampleName += '.EXTension'
            elif self.extensionLetters.get() is 1:
                exampleName += '.EXTENSION'
            elif self.extensionLetters.get() is 2:
                exampleName += '.extension'
        return exampleName

    def getName(self):
        if self.folderNameVar.get() is 0:
            return self.egNameVar.get()
        else:
            return self.oldPathVar.get().split('/')[-1]

    def renameFiles(self):
        self.updateBatchFrame()
        self.createProgressWindow()

    def addBatchItem(self):
        numberOfFiles = 0
        for pathAndFilename in glob.iglob(os.path.join(self.oldPathVar.get() + '/', r'*.*')):
            numberOfFiles += 1
        
        STARTING = True
        if self.startingNumberVar.get() is 0:
            STARTING = False
            
        if self.startingNumberStartVar.get() is 0:
            STARTINGNUMBER = 1
            if self.startingNumberStart.get().isdigit():
                STARTINGNUMBER = int(self.startingNumberStart.get())
        else:
            STARTINGNUMBER = 0
            for someItem in self.batchList:
                STARTINGNUMBER += someItem[1]
            if STARTINGNUMBER is 0:
                STARTINGNUMBER = 1
        
        splitStarting = ''
        if self.startingSeperatorVar.get() is 1:
            splitStarting = ' '
        elif self.startingSeperatorVar.get() is 2:
            splitStarting = '-'
        elif self.startingSeperatorVar.get() is 3:
            splitStarting = '_'
        elif self.startingSeperatorVar.get() is 4:
            splitStarting = ' - '
        
        bracketsStarting = True
        if self.startingBracketsVar.get() is 0:
            bracketsStarting = False
        
        if self.endingNumberStartVar.get() is 0:
            ENDINGNUMBER = 1
            if self.endingNumberStart.get().isdigit():
                ENDINGNUMBER = int(self.endingNumberStart.get())
        else:
            ENDINGNUMBER = 0
            for someItem in self.batchList:
                ENDINGNUMBER += someItem[1]
            if ENDINGNUMBER is 0:
                ENDINGNUMBER = 1
        
        splitEnding = ''
        if self.endingSeperatorVar.get() is 1:
            splitEnding = ' '
        elif self.endingSeperatorVar.get() is 2:
            splitEnding = '-'
        elif self.endingSeperatorVar.get() is 3:
            splitEnding = '_'
        elif self.endingSeperatorVar.get() is 4:
            splitEnding = ' - '
            
        bracketsEnding = True
        if self.endingBracketsVar.get() is 0:
            bracketsEnding = False
        
        item = Rename(self.getName(), self.oldPathVar.get(), self.newPathVar.get(), STARTING, STARTINGNUMBER, self.getStartingNumberDigits(), splitStarting, bracketsStarting, ENDINGNUMBER, self.getEndingNumberDigits(), splitEnding, bracketsEnding, self.extensionLetters.get(), self.extensionRename.get())
        self.batchList.append((item, numberOfFiles, self.getExampleName()))
        self.clearInput()
    
    def clearBatch(self):
        del self.batchList[:]
    
    def clearInput(self):
        self.egNameVar.set("")
        self.oldPathVar.set("")
        self.newPathVar.set("")
        
    def createProgressWindow(self):
        self.progWin = Tk()
        self.progWin.focus_force()
        self.progWin.title("Rename the files?")
        self.progWin.iconbitmap(default="icon.ico")
        label = Label(self.progWin, text="")
        label.grid(row=0, column=0)
        bLabel = Label(self.progWin, text="Are you sure you want to rename " + self.totalCountVar.get() + " files?")
        bLabel.grid(row=1, column=0, columnspan=4, sticky=W, ipadx=20)
        
        preRows = 2
        rowCount = preRows
        for item in self.batchList:
            rowCount += 1
            number = Label(self.progWin, text=str(rowCount - preRows) + ")")
            number.grid(row=rowCount, column=0, sticky=W)
            label = Label(self.progWin, text=item[2])
            label.grid(row=rowCount, column=1, sticky=W)
            count = Label(self.progWin, text=item[1])
            count.grid(row=rowCount, column=2, sticky=N)
        
        startButton = Button(self.progWin, text="   Start   ", command=self.renameForReal)
        startButton.grid(row=9000, column=2, sticky=E)
        cancelButton = Button(self.progWin, text="  Cancel  ", command=self.closeProgWin)
        cancelButton.grid(row=9000, column=3, sticky=W)
        self.progWin.resizable(False, False)
        self.progWin.mainloop()
    
    def renameForReal(self):
        for batchItem in self.batchList:
            batchItem[0].renameFiles()
        self.clearInput()
        self.clearBatch()
        self.closeProgWin()
        
    def closeProgWin(self):
        self.progWin.destroy()
        
class Rename:
    '''
    The class for the actual file renaming
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

app = App()