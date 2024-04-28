import tkinter as tk
import constantsPython
from formControls import pyControl
import ctypes

#global myPreview
#
const = constantsPython.strResourcePath()
myControl = pyControl


def previewFileForm(controlMaster: tk.Misc, jsonData:str):
    #global myPreview
    myPreview = tk.Toplevel()

    myPreview.geometry("680x550") # size of main window
    myPreview.title("Preview Config File")
    myPreview.iconbitmap(const.programIcon)
    #Consolas, 15.75pt
    pixel2 = tk.PhotoImage(width=1, height=1)
    
    testStr = jsonData ##"Relayer \nAdvanced"
    btPreview = myControl.createMultilineTextbox(controlMaster=myPreview, myWidth=40,myHeight=20, controlText=testStr, controlFont="Consolas 15",readOnly=True)
    btPreview.place(x=5, y=49) # Setting position

    btnPreviewExit = myControl.createButton(controlMaster=myPreview, controlText="Close")
    #btnPreviewExit.configure(command=myPreview.destroy)
    btnPreviewExit.configure(command=myPreview.destroy)
    # btnPreviewExit.pack()
    btnPreviewExit.place(x=461, y=329) # Setting button position
    
    myPreview.grab_set() # forces focus on form