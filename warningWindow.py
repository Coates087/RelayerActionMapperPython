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


def warningForm(controlMaster: tk.Misc):

    strNexusLink:str='https://www.nexusmods.com/relayeradvanced/mods/1'
    strGameBananaLink:str='https://gamebanana.com/mods/490768'
    myWarn = tk.Toplevel()
    strNewLine:str = '\n\n'

    myWarn.geometry("810x400") # size of main window
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
    btnPreviewExit.configure(command=myWarn.destroy)
    # btnPreviewExit.pack()
    btnPreviewExit.place(x=461, y=329) # Setting button position
    
    myWarn.grab_set() # forces focus on form