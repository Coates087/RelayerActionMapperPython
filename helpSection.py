import tkinter as tk
import constantsPython
from formControls import BetterTextBox, pyControl
import resource_files.general_icons as gIcons
from tkinter.scrolledtext import ScrolledText
import platform as os_sys

#global myPreview
#
const = constantsPython.strResourcePath()
myControl = pyControl


global btnTextPreview
bigTextPreview:dict[str,ScrolledText] = {}

global ConstTextPreview
ConstTextPreview:str='ConstTextPreview'

global myPreview
myPreview: tk.Toplevel = None
global parentForm
parentForm: tk.Misc = None

def helpSectionForm(controlMaster: tk.Misc):
    global bigTextPreview
    global ConstTextPreview    
    global myPreview
    global parentForm
    parentForm = controlMaster

    myPreview = tk.Toplevel()

    strRez = "680x600"
    strMyOS = os_sys.uname().system
    strMac = 'Darwin' # Mac system name is called "Darwin"

    yExit = 529
    if strMyOS == 'Linux' or  strMyOS == strMac:
        strRez = '780x600'
        yExit = 540

    myPreview.geometry(strRez) # size of main window
    myPreview.title("Preview Config File")
    myPreview.iconphoto(True, tk.PhotoImage(data=gIcons.OtherIcons.AppIconPNG, format="png"))

    myLable1:BetterTextBox = myControl.createBetterTextbox(controlMaster=myPreview, controlText ='Help Section:', myWidth=34,myHeight=1,readOnly=True)
    myLable1.configure(bg="#E5E5E5", padx=5)
    myLable1.place(x=5, y=29)

    testStr = LoadHelpText()
    btPreview = myControl.createMultilineTextbox(controlMaster=myPreview, myWidth=55,myHeight=20, controlText=testStr, controlFont="Consolas 15",readOnly=True)
    bigTextPreview[ConstTextPreview] = btPreview
    btPreview.place(x=5, y=49) # Setting position

    btnPreviewExit = myControl.createButton(controlMaster=myPreview, controlText="Close")
    
    btnPreviewExit.configure(command=closeThis)
    myPreview.protocol('WM_DELETE_WINDOW', closeThis)  # overrides control box's X button

    btnPreviewExit.place(x=461, y=yExit) # Setting button position
    
    myPreview.grab_set() # forces focus on form
    myPreview.transient(parentForm) # set to be on top of the main window

def LoadHelpText():
    myText:str = ''

    return myText

def closeThis():
    global myPreview
    global parentForm
    parentForm.grab_set()
    myPreview.destroy()
    pass