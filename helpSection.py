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

    strRez = "700x600"
    strMyOS = os_sys.uname().system
    strMac = 'Darwin' # Mac system name is called "Darwin"

    yExit = 529
    
    canvasWidth = 680
    if strMyOS == 'Linux' or  strMyOS == strMac:
        strRez = '800x600'
        yExit = 540
        canvasWidth = 730
        pass

    myPreview.geometry(strRez) # size of main window
    myPreview.title("Help Section")
    myPreview.iconphoto(True, tk.PhotoImage(data=gIcons.OtherIcons.AppIconPNG, format="png"))

    myLable1:BetterTextBox = myControl.createBetterTextbox(controlMaster=myPreview, controlText ='Help Section:', myWidth=34,myHeight=1,readOnly=True)
    myLable1.configure(bg="#E5E5E5", padx=5)
    myLable1.place(x=5, y=29)

    strHelpText:str = LoadHelpText()
    #btPreview:ScrolledText = myControl.createMultilineTextbox(controlMaster=myPreview, myWidth=70,myHeight=24, controlText=strHelpText, controlFont="Consolas 10",readOnly=True)
    btPreview:ScrolledText = myControl.createMultilineTextbox(controlMaster=myPreview, myWidth=90,myHeight=32, controlText=strHelpText, controlFont="Consolas 10",readOnly=True)
    btPreview.configure(wrap='word', padx=8,pady=2, bg='#f9f9f9')

    bigTextPreview[ConstTextPreview] = btPreview
    btPreview.place(x=5, y=49) # Setting position

    # frame_main = tk.Frame(myPreview, width=660, height=390 #, bg='black'
    #                    )
    # myCanvas  = tk.Canvas(frame_main, width=canvasWidth, height=690)  
    # frame_main.place(x=5, y=49) # Setting position 
    # msgHelp = tk.Message(myCanvas, font="Consolas 12", width=650, text=strHelpText, bg='lightblue')
    
    # myCanvas.place(x=1, y=1)
    # msgHelp.place(x=1, y=1) # Setting position

    # y_scrollbar = tk.Scrollbar(frame_main, orient=tk.VERTICAL, command=myCanvas.yview)
    # y_scrollbar.configure(width=25, )
    # y_scrollbar.place(x=646, y=2)
    # #y_scrollbar.pack( side = tk.RIGHT )
    # myCanvas.configure(yscrollcommand=y_scrollbar.set)
    

    # myCanvas.config(scrollregion=myCanvas.bbox("all"))
    # myCanvas.bind('<Configure>',lambda e:myCanvas.configure(scrollregion=myCanvas.bbox('all')))

    # myCanvas.create_window((0, 0))
    

    btnHelpExit = myControl.createButton(controlMaster=myPreview, controlText="Close")
    
    btnHelpExit.configure(command=closeThis)
    myPreview.protocol('WM_DELETE_WINDOW', closeThis)  # overrides control box's X button

    btnHelpExit.place(x=461, y=(yExit + 10)) # Setting button position
    
    myPreview.grab_set() # forces focus on form
    myPreview.transient(parentForm) # set to be on top of the main window

def LoadHelpText():
    
    strMyOS = os_sys.uname().system
    strMac = 'Darwin' # Mac system name is called "Darwin"

    strScriptFileName = 'batch'
    strScriptExt = '.bat'
    strFolderSlash = '\\'
    strDefaultDrive = 'C:\\'
    strProgramName = 'Relayer Action Mapper PE'
    strProgramNameWithExt:str = strProgramName

    strAppleArticle: str = ''

    #strMyOS = 'Linux'
    if strMyOS == 'Linux':
        strFolderSlash = '/'
        strDefaultDrive = '/'
        strProgramNameWithExt += '.elf'
        strScriptFileName = 'shell script'
        strScriptExt = '.sh'
        pass
    elif strMyOS == strMac:
        strFolderSlash = '/'
        strDefaultDrive = '/'
        strProgramNameWithExt += '.elf'
        strScriptFileName = 'apple script'
        strAppleArticle = 'n'
        strScriptExt = '.scpt'
    else:
        strProgramNameWithExt += '.exe'
        pass
    # myText+=fr''

    myText:str = fr'The Relayer Action Mapper PE supports command line arguments.'

    myText+=fr' You can run these arguments by adding them in a{strAppleArticle} {strScriptFileName} ({strScriptExt}) file. See below for available command line arguments.'
    myText+='\n\n**Commands**'
    myText+='\n\n'

    # -ps
    myText+=fr'-ps'
    myText+='\n'
    myText+=fr'Description: Sets {strProgramName} to "PlayStation" mode.'
    myText+=fr' This is the mode that changes the button icons and game pad options on the "Edit Controls screen".'
    myText+='\n'
    myText+=fr'Usage: {strProgramNameWithExt} -ps'
    myText+='\n\n'

    # -overridesave
    myText+=fr'-overridesave'
    myText+='\n'
    myText+='Description: Checks the "Always Override File" checkbox. When checking this checkbox, the "Save File" '
    myText+="button won't ask you if you want to override your config file." 
    myText+='\n'
    myText+=fr'Usage: {strProgramNameWithExt} -overridesave'
    myText+='\n\n'

    # -load
    myText+=fr'-load'
    myText+='\n'
    myText+='Description: Immediately loads your config file, if the file exist. If the file path of your file contains a space, you must surround it with double quotes.'     
    myText+='\n'
    myText+=fr'Usage: {strProgramNameWithExt} -load'
    myText+= fr' "{strDefaultDrive}My Folder{strFolderSlash}KeyConfig.json"'
    myText+='\n\n'

    # -save
    myText+=fr'-save'
    myText+='\n'
    myText+='Description: Sets the default directory for saving your config file. Like the "-load" command, you will need to surround the directory path with double quotes if it contains spaces.'     
    myText+='\n'
    myText+=fr'Usage: {strProgramNameWithExt} -save'
    myText+= fr' "{strDefaultDrive}My Folder{strFolderSlash}Keys{strFolderSlash}"'
    myText+='\n\n'

    # combo
    myText+=fr'**Additional Information**'
    myText+='\n'
    myText+='You can use none, one, or a combonation of these command line arguments together.'     
    myText+='\n'
    myText+='Example: \n'
    myText+= fr'{strProgramNameWithExt} -ps -load "{strDefaultDrive}My Folder{strFolderSlash}KeyConfig.json"'
    myText+= fr' -save "{strDefaultDrive}My Folder{strFolderSlash}Keys{strFolderSlash}"'
    myText+= fr' -overridesave'
    # -overridesave
    return myText

def closeThis():
    global myPreview
    global parentForm
    parentForm.grab_set()
    myPreview.destroy()
    pass