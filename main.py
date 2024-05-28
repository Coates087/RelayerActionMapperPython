import base64
import tkinter as tk
import ntpath
import json
from tkinter.filedialog import askopenfile, askopenfilename, asksaveasfile
import os
from GameControlsClass import GameControls
import constantsPython
from formControls import pyControl
from previewFile import previewFileForm
from updateControls import LoadpdateControlsForm
import resource_files.xbox_buttons as xBtn


const = constantsPython.strResourcePath()
global myControl

myControl = pyControl

global root
root = tk.Tk()

# global myPreview
# myPreview = tk.Tk()#tk.Toplevel()

## also try PyInstaller

## for compiling this program: 
## python -m PyInstaller --clean --onefile --noconsole --icon "../resource_objects/RelayerIcon.png" --specpath "./build/" --distpath  "./build/dist/" main.py --name "Relayer Action Mapper Python" 

pixel = tk.PhotoImage(width=1, height=1)
global fileContents
fileContents: str = ""

global myGameContrls
myGameContrls:GameControls = None


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
    btnLoadFile.place(x=103, y=87) # Setting button position

    btnExit = myControl.createButton(controlMaster=root, controlText="Exit", myCommand=close_win)
    btnExit.place(x=461, y=329) # Setting button position

    btnPreview = myControl.createButton(controlMaster=root, controlText="Preview Config File", myCommand=previewFile)
    btnPreview.place(x=461, y=87) # Setting button position 

    

    btnUpdateCtrls = myControl.createButton(controlMaster=root, controlText="Edit Controls", myCommand=updateControls)
    btnUpdateCtrls.place(x=281, y=87) # Setting button position 

    btnBase64 = myControl.createButton(controlMaster=root, controlText="Convert Base 64", myCommand=openBase64File)
    btnBase64.place(x=153, y=328) # Setting button position 

    # myImage = tk.PhotoImage(data=xBtn.xbox_dpad_Down, format="png")

    # canvas = tk.Canvas(root, width=300, height=300)
    # canvas.pack()
    # canvas.create_image(20, 20, anchor=tk.NW, image=myImage)
    ## root.configure(background=myImage)
    root.mainloop()
    return (True)

def openSpecialFile():
    myFile = open(const.xbox_pad_json, "r")        
    myFileName = myFile.name
    textResult = myFile.read()
    myFile.close()
    global fileContents 
    fileContents = textResult
    
    try:
        # do something
        obj:GameControls = GameControls.Deserialize(fileContents)

        global myGameContrls
        myGameContrls = obj
        print("success")
        
    except Exception as e:
        # handle it
        print("Error: " + e.args[0])

def openConfigFile():
    #
    myFile = askopenfile(mode='r',defaultextension="json",filetypes=[("JSON", ".json")])

    if not myFile == None:
        myFileName = myFile.name
        textResult = myFile.read()
        myFile.close()
        global fileContents 
        fileContents = textResult
        
        try:
            # do something
            obj:GameControls = GameControls.Deserialize(fileContents)

            global myGameContrls
            myGameContrls = obj
            print("success")
            
        except Exception as e:
            # handle it
            print("Error: " + e.args[0])

        print("File Found: " + myFileName)
    else:
        print("No file selected")


def previewFile():
    previewFileForm(root, fileContents)


def updateControls():
    global myGameContrls
    if fileContents == '':
        openSpecialFile()
        
    LoadpdateControlsForm(root, fileContents, myGameContrls)

def openBase64File():
    
    myFile = askopenfile(mode='r')

    if not myFile == None:
        myFileName = myFile.name
        myFile.close()

        onlyFile = ntpath.basename(myFileName)
        textResult =""
        with open(myFileName, "rb") as image_file:
            textResult = base64.b64encode(image_file.read())

        # textResult = myFile.read()
        decoded = base64.b64decode(textResult)
        print("printing: " + myFileName)
        print(decoded)
        currentDir = os.getcwd()
        finalPath = currentDir + "/temp/" + onlyFile + ".txt"
        
        os.makedirs(os.path.dirname(finalPath), exist_ok=True)
        f = open(finalPath, "w")
        myDataStr = repr(decoded)
        f.write(myDataStr)
        f.close()



main()