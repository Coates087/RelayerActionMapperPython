import tkinter as tk
import constantsPython
from formControls import BetterTextBox, pyControl
import resource_files.general_icons as gIcons
from tkinter.scrolledtext import ScrolledText

#global myPreview
#
const = constantsPython.strResourcePath()
myControl = pyControl


global btnTextPreview
bigTextPreview:dict[str,ScrolledText] = {}

global ConstTextPreview
ConstTextPreview:str='ConstTextPreview'


def previewFileForm(controlMaster: tk.Misc, jsonData:str):
    global bigTextPreview
    global ConstTextPreview

    myPreview = tk.Toplevel()

    myPreview.geometry("680x600") # size of main window
    myPreview.title("Preview Config File")
    myPreview.iconphoto(True, tk.PhotoImage(data=gIcons.OtherIcons.AppIconPNG, format="png"))

    myLable1:BetterTextBox = myControl.createBetterTextbox(controlMaster=myPreview, controlText ='Config Preview:', myWidth=34,myHeight=1,readOnly=True)
    myLable1.configure(bg="#E5E5E5", padx=5)
    myLable1.place(x=5, y=29)

    testStr = jsonData ##"Relayer \nAdvanced"
    btPreview = myControl.createMultilineTextbox(controlMaster=myPreview, myWidth=55,myHeight=20, controlText=testStr, controlFont="Consolas 15",readOnly=True)
    bigTextPreview[ConstTextPreview] = btPreview
    btPreview.place(x=5, y=49) # Setting position

    btnPreviewExit = myControl.createButton(controlMaster=myPreview, controlText="Close")
    #btnPreviewExit.configure(command=myPreview.destroy)
    btnPreviewExit.configure(command=myPreview.destroy)
    # btnPreviewExit.pack()
    btnPreviewExit.place(x=461, y=529) # Setting button position
    
    myPreview.grab_set() # forces focus on form