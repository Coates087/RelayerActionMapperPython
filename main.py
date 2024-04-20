import tkinter as tk
from tkinter.filedialog import askopenfile, askopenfilename, asksaveasfile
import os
import constantsPython
from formControls import pyControl
from previewFile import previewFileForm


const = constantsPython.strResourcePath()
global myControl

myControl = pyControl

global root
root = tk.Tk()

# global myPreview
# myPreview = tk.Tk()#tk.Toplevel()

pixel = tk.PhotoImage(width=1, height=1)
global fileContents
fileContents: str


def close_win():
   root.destroy()

def main():
    # Setting up main window
    root.geometry("660x473") # size of main window
    root.title("Relayer Action Mapper")
    root.iconbitmap(const.programIcon)

    #pixel.blank
    #btnLoadFile = tk.Button(root, image=pixel,text="Load File",width=133,height=33, font=('Segoe 9'), compound="left", command=openConfigFile)
    btnLoadFile = myControl.createButton(controlMaster=root, controlText="Load File", myCommand=openConfigFile)
    btnLoadFile.place(x=153, y=87) # Setting button position

    btnExit = myControl.createButton(controlMaster=root, controlText="Exit", myCommand=close_win)
    btnExit.place(x=461, y=329) # Setting button position

    btnPreview = myControl.createButton(controlMaster=root, controlText="Preview Config File", myCommand=previewFile)
    btnPreview.place(x=461, y=87) # Setting button position 
    root.mainloop()
    return (True)


def openConfigFile():
    #
    myFile = askopenfile(mode='r',defaultextension="json",filetypes=[("JSON", ".json")])

    if not myFile == None:
        myFileName = myFile.name
        textResult = myFile.read()
        global fileContents 
        fileContents = textResult
        print("File Found: " + myFileName)
    else:
        print("No file selected")

def previewFile():
    previewFileForm(root)

main()