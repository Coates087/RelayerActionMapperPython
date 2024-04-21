import base64
import tkinter as tk
import ntpath
import json
from tkinter.filedialog import askopenfile, askopenfilename, asksaveasfile
import os
import constantsPython
from formControls import pyControl
from previewFile import previewFileForm
import resource_files.xbox_buttons as xBtn


const = constantsPython.strResourcePath()
myControl = pyControl


def previewFileForm(controlMaster: tk.Misc):
    #global myPreview
    myPreview = tk.Toplevel()

    myPreview.geometry("780x650") # size of main window
    myPreview.title("Update Controls")
    myPreview.iconbitmap(const.programIcon)
    #Consolas, 15.75pt
    pixel2 = tk.PhotoImage(width=1, height=1)
    
    testStr = "Relayer \nAdvanced"
    btPreview = myControl.createMultilineTextbox(controlMaster=myPreview, myWidth=40,myHeight=20, controlText=testStr, controlFont="Consolas 15",readOnly=True)
    btPreview.place(x=5, y=49) # Setting position

    btnPreviewExit = myControl.createButton(controlMaster=myPreview, controlText="Close")
    #btnPreviewExit.configure(command=myPreview.destroy)
    btnPreviewExit.configure(command=myPreview.destroy)
    # btnPreviewExit.pack()
    btnPreviewExit.place(x=461, y=329) # Setting button position
    
    myPreview.grab_set() # forces focus on form