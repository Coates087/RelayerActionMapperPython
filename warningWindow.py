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

global parentForm
parentForm:tk.Toplevel = None

global myWarn
myWarn:tk.Toplevel = None

def warningForm(controlMaster: tk.Misc):

    strNexusLink:str='https://www.nexusmods.com/relayeradvanced/mods/1'
    strGameBananaLink:str='https://gamebanana.com/mods/490768'

    global myWarn
    
    global parentForm
    parentForm = controlMaster
    myWarn = tk.Toplevel()
    strNewLine:str = '\n\n'
    
    strRez = "810x400"
    strMyOS = os_sys.uname().system
    strMac = 'Darwin' # Macs system name is called "Darwin"

    if strMyOS == 'Linux' or  strMyOS == strMac:
        strRez = "870x400" ## Linux has weird sizing differences
        pass


    myWarn.geometry(strRez) # size of main window
    myWarn.title("Information")
    myWarn.iconphoto(True, tk.PhotoImage(data=gIcons.OtherIcons.AppIconPNG, format="png"))

    myLable1:BetterTextBox = myControl.createBetterTextbox(controlMaster=myWarn, controlText ='Information:', myWidth=34,myHeight=1,readOnly=True)
    myLable1.configure(bg="#E5E5E5", padx=5)
    myLable1.place(x=5, y=29)

    testStr = 'You have selected "“Edit for Controller Only”". This mode is intended for the "Controller Button Prompts" mod on Nexus Mods and Game Banana.' 
    testStr += strNewLine
    testStr += 'Nexus Mods Link:'
    testStr += '\n'
    testStr += strNexusLink
    testStr += strNewLine
    testStr += 'Game Banana Link:'
    testStr += '\n'
    testStr += strGameBananaLink

    btPreview = myControl.createMultilineTextbox(controlMaster=myWarn, myWidth=70,myHeight=10, controlText=testStr, controlFont="Consolas 15",readOnly=True)
    btPreview.configure(bg="#E3E3E3")
    btPreview.place(x=5, y=49) # Setting position

    btnPreviewExit = myControl.createButton(controlMaster=myWarn, controlText="Close")
    #btnPreviewExit.configure(command=myPreview.destroy)
    btnPreviewExit.configure(command=closeThis)
    # btnPreviewExit.pack()
    btnPreviewExit.place(x=461, y=329) # Setting button position

    myWarn.protocol('WM_DELETE_WINDOW', closeThis)  # overrides control box's X button
    
    myWarn.grab_set() # forces focus on form
    myWarn.transient(parentForm) # set to be on top of the main window
    if not parentForm.master == None:
        myWarn.transient(parentForm.master) # set to be on top of the main window

def closeThis():
    global myWarn
    global parentForm
    parentForm.grab_set()
    myWarn.destroy()
    pass