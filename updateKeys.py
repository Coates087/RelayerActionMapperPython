import tkinter as tk
from resource_files.ps_buttons import psBtn
import resource_files.xbox_buttons as xBtn
import resource_files.general_icons as gIcons
from tkinter.filedialog import askopenfile, askopenfilename, asksaveasfile
from formControls import pyControl, BetterCombobox, BetterTextBox
from resource_files.xbox_buttons import xBtn
from GameControlsClass import GameControls, GamePadButton, KeyboardClass
from tkinter.tix import ScrolledWindow
from copy import copy, deepcopy
#from sys import platform as os_sys
import platform as os_sys

import updateControls # .childWin

global keyDropdowns
keyDropdowns: dict[str,BetterCombobox] = {}
global keyButtons
keyButtons: dict[str,tk.Button] = {}
global keyLabels
keyLabels: dict[str,BetterTextBox] = {}

global rdoInputType
rdoInputType:tk.StringVar = None

global keyControlForm
keyControlForm:tk.Toplevel


#@Constant
global ConstButtonName 
ConstButtonName:str = 'ButtonName'
global ConstKeyCode
ConstKeyCode:str = 'KeyCode'
global ConstKeyField
ConstKeyField:str = 'KeyField'

global newControls
newControls:bool = False

global strScrollActions
strScrollActions:list[str] = []

global strRemoveBtnKey
strRemoveBtnKey:list[str] = []

global strComboBoxKey
strComboBoxKey:list[str] = []

global myKeyOptions
myKeyOptions:list[KeyboardClass] = []

global indexKey
indexKey:int = 0

global strKey
strKey:str = 'Index-'

global strAction
strAction:str = ''

global frame_main
frame_main:tk.Frame = None

global frame_buttons
frame_buttons:tk.Frame = None

global canvas
canvas:tk.Canvas = None

global keySubFrames
keySubFrames:dict[str,tk.Frame] = {}

global lblKey
lblKey:BetterTextBox = None

myControl = pyControl

global myParent
myParent: tk.Misc

def LoadpdateKeysForm(controlMaster: tk.Misc, strActionName:str, myTempGameContrls:GameControls, altButton:str=''):
    global keyControlForm

    global strScrollActions
    strScrollActions = []

    global newControls
    newControls = False
    
    global myParent
    myParent =controlMaster

    global strAction
    strAction = strActionName

    strMac = 'Darwin' # Macs system name is called "Darwin"

    # we need to determent the os in order to properly unbind and rebind the mouse scroll os_sys
    strMyOS = os_sys.uname().system

    if strMyOS == 'Windows' or  strMyOS == strMac:
        strScrollActions.append('<MouseWheel>')
    else: # Linux
        strScrollActions.append('<ButtonPress-4>')
        strScrollActions.append('<ButtonPress-5>')

        
    keyControlForm = tk.Toplevel()
    keyControlForm.geometry("666x391") # size of main window
    keyControlForm.title("Control Window")
    keyControlForm.iconphoto(True, tk.PhotoImage(data=gIcons.OtherIcons.AppIconPNG, format="png"))


    global myGameContrls
    myGameContrls = myTempGameContrls

    global localGameContrls
    localGameContrls =deepcopy(myTempGameContrls)

    
    global myKeyOptions
    myKeyOptions = getKeyList()

    LoadFormContent(keyControlForm,strActionName, altButton)
    if not keyControlForm == None:
        keyControlForm.grab_set() # forces focus on form
        keyControlForm.transient(controlMaster) # set to be on top of the main window
        # child_window.transient(root) # set to be on top of the main window
        # child_window.grab_set() # hijack all commands from the master (clicks on the main window are ignored)
        # root.wait_window(child_window) # pause anything on the main window until this one closes
        
        keyControlForm.protocol('WM_DELETE_WINDOW', CancelChanges)  # overrides control box's X button
        pass


def AddKey():
    # print("AddKey")

    global indexKey
    global frame_buttons
    global canvas

    # dictionaries
    global keySubFrames

    numOfKeys = len(keySubFrames)

    createElements(indexKey, '', numOfKeys)
    indexKey += 1
    frame_buttons.update_idletasks()
    updateKeyCount()
    # Set the canvas scrolling region
    canvas.config(scrollregion=canvas.bbox("all"))
    
    pass


def RemoveKey(index):
    global keyButtons
    global keyDropdowns
    global keySubFrames
    global myKeyOptions
    global frame_main
    global canvas

    global strKey

    myFrameElement = keySubFrames[strKey + str(index)]
    myButton = keyButtons[strKey + str(index)]
    myDropdown = keyDropdowns[strKey + str(index)]

    if not myButton == None:
        myButton.destroy()
        del keyButtons[strKey + str(index)]

    if not myDropdown == None:
        myDropdown.destroy()
        del keyDropdowns[strKey + str(index)]

    if not myFrameElement == None:
        myFrameElement.destroy()
        del keySubFrames[strKey + str(index)]

    updateKeyCount()
    frame_buttons.update_idletasks()

    # Set the canvas scrolling region
    canvas.config(scrollregion=canvas.bbox("all"))
    pass


def SaveChanges():
    global myParent
    global keyControlForm
    
    global strAction
    global newControls
    newControls = True
    
    allKeycodes:list[str] =[]

    allKeycodes = getAllDropdows()
    
    global myParent
    myParent.grab_set()
    
    updateControls.childWin.storeKeyResults(strAction,allKeycodes)
    keyControlForm.destroy()
    pass

def CancelChanges():
    global keyControlForm

    global myParent
    myParent.grab_set()
    keyControlForm.destroy()
    pass


def getAllDropdows():
    global keyDropdowns

    allKeys = list(keyDropdowns.keys())

    allKeyCodes:list[str] = []
    
    aLength = allKeys.__len__()
    for r in range(aLength):
        aKey = allKeys[r]
        aDropDown = keyDropdowns[aKey]

        newVal = aDropDown.get_value()
        allKeyCodes.append(newVal)
        pass

    return allKeyCodes

def updateKeyCount():
    # dictionaries
    global keySubFrames
    global keyDropdowns
    global keyButtons
    global keyLabels

    global frame_buttons
    
    global strKey
    global strScrollActions
    numOfKeys = len(keySubFrames)
    
    global lblKey

    lblKey.set_value("Keys: " + str(numOfKeys))
    pass

def ClearGlobals():
    # dictionaries
    global keySubFrames
    global keyDropdowns
    global keyButtons
    global keyLabels

    global myKeyOptions

    global strScrollActions
    global frame_main
    global canvas
    
    global ConstButtonName 
    global ConstKeyCode
    global ConstKeyField

    global indexKey
    global strKey

    ## initalizing globals
    keySubFrames = {}
    keyDropdowns = {}
    keyButtons = {}
    keyLabels = {}
    frame_main = {}
    canvas = None
    indexKey = 0
    pass

def LoadFormContent(myGlobalForm:tk.Misc, strActionName:str, altButton:str=''):
    
    frame_top =tk.Frame(myGlobalForm, width=900, height=100)
    frame_top.place(x=1,y=1)    
    
    # strMyOS = os_sys.uname().system


    # strMac = 'Darwin' # Macs system name is called "Darwin"
    # if strMyOS == 'Linux' or  strMyOS == strMac:
    #     canvasWidth = 730 ## Linux has weird sizing differences
    #     pass
    
    global lblKey
    lblKey = myControl.createBetterTextbox(controlMaster=frame_top, controlText ="Keys: " , myWidth=34,myHeight=1,readOnly=True)
    lblKey.configure(bg="#E5E5E5", padx=5)
    #lblKey = tk.Label(frame_top, text="Keys", padx=2)
    lblKey.grid(column=0,row=0, rowspan=2)

    
    # dictionaries
    global keySubFrames
    global keyDropdowns
    global keyButtons
    global keyLabels

    global myKeyOptions

    global strScrollActions
    global frame_main
    global canvas
    
    global ConstButtonName 
    global ConstKeyCode
    global ConstKeyField

    global indexKey
    global strKey

    ## initalizing globals
    ClearGlobals()

    frame_parent = tk.Frame(frame_top)
    frame_parent.grid(sticky='news')

    frame_main = tk.Frame(frame_parent, bg="gray")
    frame_main.grid(sticky='news', row=1, column=2)
    
    
    btnAddKeys:tk.Button = myControl.createButton(controlMaster=myGlobalForm, myWidth=14,myHeight=4, controlText="Add Key", myCommand=AddKey)
    btnAddKeys.place(x=500,y=90)
    
    btnSave:tk.Button = myControl.createButton(controlMaster=myGlobalForm, myWidth=14,myHeight=1, controlText="Save", myCommand=SaveChanges)
    btnSave.place(x=500,y=260)
    
    btnCancel:tk.Button = myControl.createButton(controlMaster=myGlobalForm, myWidth=14,myHeight=1, controlText="Cancel", myCommand=CancelChanges)
    btnCancel.place(x=500,y=300)

    myButtons = vars(xBtn)

    myPSButtons = vars(psBtn)
    
    myXboxSticks = getXboxSticks()

    myKeyField = getControlSetting(strActionName)
    myKeyList:list[str] = []
    myKeyList = myKeyField[ConstKeyCode]
    aLength = myKeyList.__len__()

    myData:bytes = None 
    if altButton != '':
        myData = myPSButtons[altButton]
        pass
    else:
        myData = myButtons[strActionName]
        pass
    
    myImage2 = tk.PhotoImage(data=myData,format="png",width=70,height=70)
    img = myImage2
    
    
    isXboxStick = (strActionName in myXboxSticks)
    if isXboxStick == True:
        ## create larger container for image, then shrink it
        myImage2 = tk.PhotoImage(data=myData,format="png",width=107,height=70)
        myImage2  = myImage2.zoom(x=7)

        img  = myImage2.subsample(x=10)
        img.configure(width=70,height=70)

    lbl = tk.Label(frame_parent, image=img, bg="#E5E5E5", padx=2)

    #myKeys = getControlSetting(anXboxButton)
    lbl.grid(sticky="NW",column=0,row=1, rowspan=1)
    lbl.image = img # save the image reference

    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(frame_main)
    frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
    frame_canvas.grid_rowconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(0, weight=1)
    # Set grid_propagate to False to allow 5-by-5 buttons resizing later
    frame_canvas.grid_propagate(False)

    # Add a canvas in that frame
    canvas = tk.Canvas(frame_canvas)
    canvas.grid(row=0, column=0, sticky="news")

    # Link a scrollbar to the canvas
    vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=vsb.set)

    global frame_buttons
    # Create a frame to contain the buttons and dropdowns
    frame_buttons = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

    myXboxSticks = getXboxSticks()

    myKeyField = getControlSetting(strActionName)
    myKeyList:list[str] = []
    myKeyList = myKeyField[ConstKeyCode]
    aLength = myKeyList.__len__() # getting number of keys for action
    
    lblKey.set_value("Keys: " + str(aLength))
    # Keys
    for r in range(aLength):
        aKey:str = myKeyList[r]

        createElements(indexKey, aKey, indexKey)
        indexKey += 1
        pass
    frame_buttons.update_idletasks()
    

    frame_canvas.config(width=370,
                        height=300)
    # Set the canvas scrolling region
    canvas.config(scrollregion=canvas.bbox("all"))
    pass


def createElements(myIndex:int = 0, strKeyCode:str = 'None', intRow:int = 0):
    
    # dictionaries
    global keySubFrames
    global keyDropdowns
    global keyButtons
    global keyLabels

    global frame_buttons
    
    global strKey
    global strScrollActions

    if strKeyCode == '':
        strKeyCode= 'None'
        pass

    mySubFrame = tk.Frame(frame_buttons, width=400, bg="#E5E5E5")
    # ## Grid Style
    # specialFrame = tk.Frame(mySubFrame)
    keySubFrames[strKey + str(indexKey)] = mySubFrame
    aDropDown = BetterCombobox(master= mySubFrame, width=20, dislplayMember='KeyName', valueMember='KeyCode',values=myKeyOptions)  ##tk.OptionMenu(specialFrame, optionVar, myButtonOptions)
    aDropDown.configure(state="readonly")

    
    for strScroll in strScrollActions:
        myResult = aDropDown.bindtags()
        aDropDown.unbind_class("TCombobox", strScroll)
        pass
        

    aDropDown.grid(column=1,row=0, sticky="SW")

    keyDropdowns[strKey + str(indexKey)] = aDropDown
    aDropDown.set(strKeyCode)
    
    btnKeys1:tk.Button = myControl.createButton(controlMaster=mySubFrame, myWidth=10,myHeight=1, controlText="Remove", myCommand=lambda buttonIndex=myIndex: RemoveKey(buttonIndex))
    
    keyButtons[strKey + str(indexKey)] = btnKeys1

    ## specialFrame.grid(column=1,row=0, sticky="SW", pady=2)

    if intRow == 0:
        btnKeys1.configure(state=tk.DISABLED, bg="#ebebeb")

    btnKeys1.grid(column=2,row=0, sticky="SW")
        
    mySubFrame.grid(row=intRow,column=2, pady=2)

    pass


def getXboxButtons():
    xboxList: list[str] = []

    # other
    xboxList.append("xbox_start")
    xboxList.append("xbox_back")

    # face buttons
    xboxList.append("xbox_A")
    xboxList.append("xbox_B")
    xboxList.append("xbox_X")
    xboxList.append("xbox_Y")
    
    # shoulder buttons
    xboxList.append("xbox_LB")
    xboxList.append("xbox_RB")
    xboxList.append("xbox_LT")
    xboxList.append("xbox_RT")

    # dpad
    xboxList.append("xbox_dpad_Up")
    xboxList.append("xbox_dpad_Down")
    xboxList.append("xbox_dpad_Left")
    xboxList.append("xbox_dpad_Right")
    
    # left analog stick
    xboxList.append("xbox_left_stick")
    xboxList.append("xbox_left_stick_Up")
    xboxList.append("xbox_left_stick_Down")
    xboxList.append("xbox_left_stick_Left")
    xboxList.append("xbox_left_stick_Right")
    xboxList.append("xbox_left_stick_click")

    # right analog stick
    xboxList.append("xbox_right_stick_Up")
    xboxList.append("xbox_right_stick_Down")
    xboxList.append("xbox_right_stick_Left")
    xboxList.append("xbox_right_stick_Right")
    xboxList.append("xbox_right_stick_click")

    return xboxList

def getControlSetting(actionId:str):
    global localGameContrls

    global ConstButtonName 
    global ConstKeyCode
    global ConstKeyField

    tempList:list[str] = []
    resultDict: dict[str,any] = {}

    resultDict[ConstButtonName] = ''
    resultDict[ConstKeyField] = ''
    resultDict[ConstKeyCode] = tempList

    match actionId:
        case "xbox_start":
            resultDict[ConstButtonName] = localGameContrls.Escape.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.Escape.KeyCode
            resultDict[ConstKeyField] = "Escape"
            pass
        case "xbox_back":
            resultDict[ConstButtonName] = localGameContrls.V.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.V.KeyCode
            resultDict[ConstKeyField] = "V"
            pass
        case "xbox_A":
            resultDict[ConstButtonName] = localGameContrls.Enter.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.Enter.KeyCode
            resultDict[ConstKeyField] = "Enter"
            pass
        case "xbox_B":
            resultDict[ConstButtonName] = localGameContrls.Backspace.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.Backspace.KeyCode
            resultDict[ConstKeyField] = "Backspace"
            pass
        case "xbox_X":
            resultDict[ConstButtonName] = localGameContrls.Tab.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.Tab.KeyCode
            resultDict[ConstKeyField] = "Tab"
            pass
        case "xbox_Y":
            resultDict[ConstButtonName] = localGameContrls.Shift.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.Shift.KeyCode
            resultDict[ConstKeyField] = "Shift"
            pass
        case "xbox_LB":
            resultDict[ConstButtonName] = localGameContrls.Q.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.Q.KeyCode
            resultDict[ConstKeyField] = "Q"
            pass
        case "xbox_RB":
            resultDict[ConstButtonName] = localGameContrls.E.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.E.KeyCode
            resultDict[ConstKeyField] = "E"
            pass
        case "xbox_LT":
            resultDict[ConstButtonName] = localGameContrls.WheelUp.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.WheelUp.KeyCode # [ "None" ]
            resultDict[ConstKeyField] = "WheelUp"
            pass
        case "xbox_RT":
            resultDict[ConstButtonName] = localGameContrls.WheelDown.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.WheelDown.KeyCode # [ "None" ]
            resultDict[ConstKeyField] = "WheelDown"
            pass
        case "xbox_dpad_Up":
            resultDict[ConstButtonName] = localGameContrls.W.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.W.KeyCode
            resultDict[ConstKeyField] = "W"
            pass
        case "xbox_dpad_Down":
            resultDict[ConstButtonName] = localGameContrls.S.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.S.KeyCode
            resultDict[ConstKeyField] = "S"
            pass
        case "xbox_dpad_Left":
            resultDict[ConstButtonName] = localGameContrls.A.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.A.KeyCode
            resultDict[ConstKeyField] = "A"
            pass
        case "xbox_dpad_Right":
            resultDict[ConstButtonName] = localGameContrls.D.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.D.KeyCode
            resultDict[ConstKeyField] = "D"
        case "xbox_left_stick":
            # resultDict[ConstButtonName] = # localGameContrls.Ctrl..ButtonName
            resultDict[ConstKeyCode] = localGameContrls.Ctrl.KeyCode
            resultDict[ConstKeyField] = "Ctrl"
            pass
        case "xbox_left_stick_Up":
            resultDict[ConstButtonName] = localGameContrls.CtrlW.ButtonName
            resultDict[ConstKeyCode] = ['[Control] + [W]']
            resultDict[ConstKeyField] = "CtrlW"
            pass
        case "xbox_left_stick_Down":
            resultDict[ConstButtonName] = localGameContrls.CtrlS.ButtonName
            resultDict[ConstKeyCode] = ['[Control] + [S]']
            resultDict[ConstKeyField] = "CtrlS"
            pass
        case "xbox_left_stick_Left":
            resultDict[ConstButtonName] = localGameContrls.CtrlA.ButtonName
            resultDict[ConstKeyCode] = ['[Control] + [A]']
            resultDict[ConstKeyField] = "CtrlA"
            pass
        case "xbox_left_stick_Right":
            resultDict[ConstButtonName] = localGameContrls.CtrlD.ButtonName
            resultDict[ConstKeyCode] = ['[Control] + [D]']
            resultDict[ConstKeyField] = "CtrlD"
            pass
        case "xbox_left_stick_click":
            resultDict[ConstButtonName] = localGameContrls.F.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.F.KeyCode
            resultDict[ConstKeyField] = "F"
            pass
        
        case "xbox_right_stick_Up":
            resultDict[ConstButtonName] = localGameContrls.UpArrow.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.UpArrow.KeyCode
            resultDict[ConstKeyField] = "UpArrow"
            pass
        case "xbox_right_stick_Down":
            resultDict[ConstButtonName] = localGameContrls.DownArrow.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.DownArrow.KeyCode
            resultDict[ConstKeyField] = "DownArrow"
            pass
        case "xbox_right_stick_Left":
            resultDict[ConstButtonName] = localGameContrls.LeftArrow.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.LeftArrow.KeyCode
            resultDict[ConstKeyField] = "LeftArrow"
            pass
        case "xbox_right_stick_Right":
            resultDict[ConstButtonName] = localGameContrls.RightArrow.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.RightArrow.KeyCode
            resultDict[ConstKeyField] = "RightArrow"
            pass
        case "xbox_right_stick_click":
            resultDict[ConstButtonName] = localGameContrls.R.ButtonName
            resultDict[ConstKeyCode] = localGameContrls.R.KeyCode
            resultDict[ConstKeyField] = "R"
            pass
        case _:
            pass
    return resultDict


def getKeyList():
    keyList:list[KeyboardClass] = []

    keyList.append(KeyboardClass(KeyCode="None", KeyName="None"))

    keyList.append(KeyboardClass(KeyCode = "Backspace", KeyName = "Backspace"))
    keyList.append(KeyboardClass(KeyCode = "Tab", KeyName = "Tab"))
    keyList.append(KeyboardClass(KeyCode = "Clear", KeyName = "Clear"))
    keyList.append(KeyboardClass(KeyCode = "Return", KeyName = "Enter"))
    keyList.append(KeyboardClass(KeyCode = "Escape", KeyName = "Escape"))
    keyList.append(KeyboardClass(KeyCode = "Pause", KeyName = "Pause"))
    keyList.append(KeyboardClass(KeyCode = "Space", KeyName = "Space"))
    keyList.append(KeyboardClass(KeyCode = "Exclaim", KeyName = "Exclaimation"))
    keyList.append(KeyboardClass(KeyCode = "DoubleQuote", KeyName = "DoubleQuote"))
    keyList.append(KeyboardClass(KeyCode = "Quote", KeyName = "Quote"))
    keyList.append(KeyboardClass(KeyCode = "Hash", KeyName = "# (Hash)"))
    keyList.append(KeyboardClass(KeyCode = "Dollar", KeyName = "$ (Dollar)"))
    keyList.append(KeyboardClass(KeyCode = "Percent", KeyName = "% (Percent)"))
    keyList.append(KeyboardClass(KeyCode = "Ampersand", KeyName = "& (Ampersand)"))
    keyList.append(KeyboardClass(KeyCode = "LeftParen", KeyName = "( (LeftParen)"))
    keyList.append(KeyboardClass(KeyCode = "RightParen", KeyName = ") (RightParen)"))
    keyList.append(KeyboardClass(KeyCode = "Asterisk", KeyName = "* (Asterisk)"))
    keyList.append(KeyboardClass(KeyCode = "Plus", KeyName = "+ (Plus)"))
    keyList.append(KeyboardClass(KeyCode = "Comma", KeyName = ", (Comma)"))
    keyList.append(KeyboardClass(KeyCode = "Minus", KeyName = "- (Minus)"))
    keyList.append(KeyboardClass(KeyCode = "Period", KeyName = ". (Period)"))
    keyList.append(KeyboardClass(KeyCode = "Slash", KeyName = "/ (Slash)"))
    keyList.append(KeyboardClass(KeyCode = "Backslash", KeyName = "\\ (Back Slash)"))
    keyList.append(KeyboardClass(KeyCode = "Period", KeyName = ". (Period)"))
    keyList.append(KeyboardClass(KeyCode = "Colon", KeyName = ": (:)"))
    keyList.append(KeyboardClass(KeyCode = "Semicolon", KeyName = "; (;)"))
    keyList.append(KeyboardClass(KeyCode = "Less", KeyName = "< (Less)"))
    keyList.append(KeyboardClass(KeyCode = "Equals", KeyName = "= (Equals)"))
    keyList.append(KeyboardClass(KeyCode = "Greater", KeyName = "> (Greater)"))
    keyList.append(KeyboardClass(KeyCode = "Question", KeyName = "? (Question)"))
    keyList.append(KeyboardClass(KeyCode = "At", KeyName = "@ (At Symbol)"))
    keyList.append(KeyboardClass(KeyCode = "LeftBracket", KeyName = "[ (LeftBracket)"))
    keyList.append(KeyboardClass(KeyCode = "RightBracket", KeyName = "] (RighttBracket)"))
    keyList.append(KeyboardClass(KeyCode = "LeftCurlyBracket", KeyName = "{ (LeftCurlyBracket)"))
    keyList.append(KeyboardClass(KeyCode = "RightCurlyBracket", KeyName = "} (RightCurlyBracket)"))

    keyList.append(KeyboardClass(KeyCode = "Caret", KeyName = "^ (Caret)"))
    keyList.append(KeyboardClass(KeyCode = "Underscore", KeyName = "_ (Underscore)"))
    keyList.append(KeyboardClass(KeyCode = "BackQuote", KeyName = "` (BackQuote)"))
    keyList.append(KeyboardClass(KeyCode = "A", KeyName = "A"))
    keyList.append(KeyboardClass(KeyCode = "B", KeyName = "B"))
    keyList.append(KeyboardClass(KeyCode = "C", KeyName = "C"))
    keyList.append(KeyboardClass(KeyCode = "D", KeyName = "D"))
    keyList.append(KeyboardClass(KeyCode = "E", KeyName = "E"))
    keyList.append(KeyboardClass(KeyCode = "F", KeyName = "F"))
    keyList.append(KeyboardClass(KeyCode = "G", KeyName = "G"))
    keyList.append(KeyboardClass(KeyCode = "H", KeyName = "H"))
    keyList.append(KeyboardClass(KeyCode = "I", KeyName = "I"))
    keyList.append(KeyboardClass(KeyCode = "J", KeyName = "J"))
    keyList.append(KeyboardClass(KeyCode = "K", KeyName = "K"))
    keyList.append(KeyboardClass(KeyCode = "L", KeyName = "L"))
    keyList.append(KeyboardClass(KeyCode = "M", KeyName = "M"))
    keyList.append(KeyboardClass(KeyCode = "N", KeyName = "N"))
    keyList.append(KeyboardClass(KeyCode = "O", KeyName = "O"))

    keyList.append(KeyboardClass(KeyCode = "P", KeyName = "P"))
    keyList.append(KeyboardClass(KeyCode = "Q", KeyName = "Q"))
    keyList.append(KeyboardClass(KeyCode = "R", KeyName = "R"))
    keyList.append(KeyboardClass(KeyCode = "S", KeyName = "S"))
    keyList.append(KeyboardClass(KeyCode = "T", KeyName = "T"))
    keyList.append(KeyboardClass(KeyCode = "U", KeyName = "U"))
    keyList.append(KeyboardClass(KeyCode = "V", KeyName = "V"))
    keyList.append(KeyboardClass(KeyCode = "W", KeyName = "W"))
    keyList.append(KeyboardClass(KeyCode = "X", KeyName = "X"))
    keyList.append(KeyboardClass(KeyCode = "Y", KeyName = "Y"))
    keyList.append(KeyboardClass(KeyCode = "Z", KeyName = "Z"))

    keyList.append(KeyboardClass(KeyCode = "Pipe", KeyName = "| (Pipe)"))
    keyList.append(KeyboardClass(KeyCode = "Tilde", KeyName = "~ (Tilde)"))
    keyList.append(KeyboardClass(KeyCode = "Delete", KeyName = "Delete"))
    keyList.append(KeyboardClass(KeyCode = "Keypad0", KeyName = "Keypad 0"))
    keyList.append(KeyboardClass(KeyCode = "Keypad1", KeyName = "Keypad 1"))
    keyList.append(KeyboardClass(KeyCode = "Keypad2", KeyName = "Keypad 2"))
    keyList.append(KeyboardClass(KeyCode = "Keypad3", KeyName = "Keypad 3"))
    keyList.append(KeyboardClass(KeyCode = "Keypad4", KeyName = "Keypad 4"))
    keyList.append(KeyboardClass(KeyCode = "Keypad5", KeyName = "Keypad 5"))
    keyList.append(KeyboardClass(KeyCode = "Keypad6", KeyName = "Keypad 6"))
    keyList.append(KeyboardClass(KeyCode = "Keypad7", KeyName = "Keypad 7"))
    keyList.append(KeyboardClass(KeyCode = "Keypad8", KeyName = "Keypad 8"))
    keyList.append(KeyboardClass(KeyCode = "Keypad9", KeyName = "Keypad 9"))

    keyList.append(KeyboardClass(KeyCode = "KeypadPeriod", KeyName = "Keypad ."))
    keyList.append(KeyboardClass(KeyCode = "KeypadDivide", KeyName = "Keypad /"))
    keyList.append(KeyboardClass(KeyCode = "KeypadMultiply", KeyName = "Keypad *"))
    keyList.append(KeyboardClass(KeyCode = "KeypadMinus", KeyName = "Keypad -"))
    keyList.append(KeyboardClass(KeyCode = "KeypadPlus", KeyName = "Keypad +"))
    keyList.append(KeyboardClass(KeyCode = "KeypadEnter", KeyName = "Keypad Enter"))
    keyList.append(KeyboardClass(KeyCode = "UpArrow", KeyName = "Up Arrow"))
    keyList.append(KeyboardClass(KeyCode = "DownArrow", KeyName = "Down Arrow"))
    keyList.append(KeyboardClass(KeyCode = "LeftArrow", KeyName = "Left Arrow"))
    keyList.append(KeyboardClass(KeyCode = "RightArrow", KeyName = "Right Arrow"))

    keyList.append(KeyboardClass(KeyCode = "Insert", KeyName = "Insert"))
    keyList.append(KeyboardClass(KeyCode = "Home", KeyName = "Home"))
    keyList.append(KeyboardClass(KeyCode = "End", KeyName = "End"))
    keyList.append(KeyboardClass(KeyCode = "PageUp", KeyName = "Page Up"))
    keyList.append(KeyboardClass(KeyCode = "PageDown", KeyName = "Page Down"))

    keyList.append(KeyboardClass(KeyCode = "F1", KeyName = "F1"))
    keyList.append(KeyboardClass(KeyCode = "F2", KeyName = "F2"))
    keyList.append(KeyboardClass(KeyCode = "F3", KeyName = "F3"))
    keyList.append(KeyboardClass(KeyCode = "F4", KeyName = "F4"))
    keyList.append(KeyboardClass(KeyCode = "F5", KeyName = "F5"))
    keyList.append(KeyboardClass(KeyCode = "F6", KeyName = "F6"))
    keyList.append(KeyboardClass(KeyCode = "F7", KeyName = "F7"))
    keyList.append(KeyboardClass(KeyCode = "F8", KeyName = "F8"))
    keyList.append(KeyboardClass(KeyCode = "F9", KeyName = "F9"))
    keyList.append(KeyboardClass(KeyCode = "F10", KeyName = "F10"))
    keyList.append(KeyboardClass(KeyCode = "F11", KeyName = "F11"))
    keyList.append(KeyboardClass(KeyCode = "F12", KeyName = "F12"))
    keyList.append(KeyboardClass(KeyCode = "F13", KeyName = "F13"))
    keyList.append(KeyboardClass(KeyCode = "F14", KeyName = "F14"))
    keyList.append(KeyboardClass(KeyCode = "F15", KeyName = "F15"))
    keyList.append(KeyboardClass(KeyCode = "Numlock", KeyName = "Numlock"))
    keyList.append(KeyboardClass(KeyCode = "CapsLock", KeyName = "CapsLock"))
    keyList.append(KeyboardClass(KeyCode = "ScrollLock", KeyName = "ScrollLock"))
    keyList.append(KeyboardClass(KeyCode = "LeftShift", KeyName = "LeftShift"))
    keyList.append(KeyboardClass(KeyCode = "RightShift", KeyName = "RightShift"))
    keyList.append(KeyboardClass(KeyCode = "LeftControl", KeyName = "LeftControl"))
    keyList.append(KeyboardClass(KeyCode = "RightControl", KeyName = "RightControl"))
    keyList.append(KeyboardClass(KeyCode = "LeftAlt", KeyName = "LeftAlt"))
    keyList.append(KeyboardClass(KeyCode = "RightAlt", KeyName = "RightAlt"))

    keyList.append(KeyboardClass(KeyCode = "LeftCommand", KeyName = "LeftCommand"))
    keyList.append(KeyboardClass(KeyCode = "RightCommand", KeyName = "RightCommand"))
    keyList.append(KeyboardClass(KeyCode = "Command", KeyName = "Command"))
    keyList.append(KeyboardClass(KeyCode = "LeftApple", KeyName = "LeftApple"))
    keyList.append(KeyboardClass(KeyCode = "RightApple", KeyName = "RightApple"))
    keyList.append(KeyboardClass(KeyCode = "Apple", KeyName = "Apple"))
    keyList.append(KeyboardClass(KeyCode = "Help", KeyName = "Help"))
    keyList.append(KeyboardClass(KeyCode = "Print", KeyName = "Print"))

    keyList.append(KeyboardClass(KeyCode = "SysReq", KeyName = "SysReq"))
    keyList.append(KeyboardClass(KeyCode = "Break", KeyName = "Break"))
    keyList.append(KeyboardClass(KeyCode = "Menu", KeyName = "Menu"))

    keyList.append(KeyboardClass(KeyCode = "Mouse0", KeyName = "Mouse 0"))
    keyList.append(KeyboardClass(KeyCode = "Mouse1", KeyName = "Mouse 1"))
    keyList.append(KeyboardClass(KeyCode = "Mouse2", KeyName = "Mouse 2"))
    keyList.append(KeyboardClass(KeyCode = "Mouse3", KeyName = "Mouse 3"))
    keyList.append(KeyboardClass(KeyCode = "Mouse4", KeyName = "Mouse 4"))
    keyList.append(KeyboardClass(KeyCode = "Mouse5", KeyName = "Mouse 5"))
    keyList.append(KeyboardClass(KeyCode = "Mouse6", KeyName = "Mouse 6"))
    return keyList


def getXboxSticks():
    xboxList: list[str] = []

    # left analog stick
    xboxList.append("xbox_left_stick")
    xboxList.append("xbox_left_stick_Up")
    xboxList.append("xbox_left_stick_Down")
    xboxList.append("xbox_left_stick_Left")
    xboxList.append("xbox_left_stick_Right")
    xboxList.append("xbox_left_stick_click")

    # right analog stick
    xboxList.append("xbox_right_stick_Up")
    xboxList.append("xbox_right_stick_Down")
    xboxList.append("xbox_right_stick_Left")
    xboxList.append("xbox_right_stick_Right")
    xboxList.append("xbox_right_stick_click")

    return xboxList
