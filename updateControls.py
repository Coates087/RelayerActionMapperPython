from ast import Constant
import io, base64
import time
import tkinter as tk
from tkinter import ttk
import ntpath
import json
from tkinter.filedialog import askopenfile, askopenfilename, asksaveasfile
import os
import constantsPython
from formControls import pyControl, BetterCombobox
from previewFile import previewFileForm
from resource_files.xbox_buttons import xBtn
from GameControlsClass import GameControls, GamePadButton
from tkinter.tix import ScrolledWindow
from copy import copy, deepcopy
#from sys import platform as os_sys
import platform as os_sys



const = constantsPython.strResourcePath()
myControl = pyControl

global updateControlForm
updateControlForm: tk.Toplevel

global myImage #: tk.PhotoImage
myImage: tk.PhotoImage

global jsonFileData
jsonFileData:str = ''

global myGameContrls
myGameContrls:GameControls 

global localGameContrls
localGameContrls:GameControls = None

global allDropdowns
allDropdowns: list[BetterCombobox] = []
## https://stackoverflow.com/a/45442534
#str,any
global allButtons
allButtons: list[tk.Button] = []

global allLabels
allLabels:tk.Text = []


global keyDropdowns
keyDropdowns: dict[str,BetterCombobox] = {}
global keyButtons
keyButtons: dict[str,tk.Button] = {}
global keyLabels
keyLabels: dict[str,tk.Text] = {}

global rdoInputType
rdoInputType:tk.StringVar = None

#@Constant
global ConstButtonName 
ConstButtonName:str = 'ButtonName'
global ConstKeyCode
ConstKeyCode:str = 'KeyCode'
global ConstKeyField
ConstKeyField:str = 'KeyField'

global strScrollActions
strScrollActions:list[str] = []


def LoadpdateControlsForm(controlMaster: tk.Misc, jsonData:str, myTempGameContrls:GameControls):
    #global myPreview

    global strScrollActions

    strMac = 'Darwin' # Macs system name is called "Darwin"

    # we need to determent the os in order to properly unbind and rebind the mouse scroll os_sys
    strMyOS = os_sys.uname().system



    if strMyOS == 'Windows' or  strMyOS == strMac:
        strScrollActions.append('<MouseWheel>')
    else: # Linux
        strScrollActions.append('<ButtonPress-4>')
        strScrollActions.append('<ButtonPress-5>')
        
    updateControlForm = tk.Toplevel()
    updateControlForm.geometry("780x680") # size of main window
    updateControlForm.title("Update Controls")
    updateControlForm.iconbitmap(const.programIcon)
    #Consolas, 15.75pt
    # pixel2 = tk.PhotoImage(width=1, height=1)
    
    #jsonData ##"Relayer \nAdvanced"

    global jsonFileData
    jsonFileData = jsonData

    global myGameContrls
    myGameContrls = myTempGameContrls

    global localGameContrls
    localGameContrls =deepcopy(myTempGameContrls)
    
    try:
        testStr = GameControls.Serialize(myGameContrls) #myGameContrls.Serialize()
        tempContrls =GameControls.Deserialize(testStr)
    except Exception as e:
        # handle it
        print(e.args[0])
        print("Add Dummy JSON")

    if not updateControlForm == None:
        updateControlForm.grab_set() # forces focus on form
    LoadForm(updateControlForm)
    #LoadForm()
   

def LoadKeyDialog(eventIndex:str='0', buttonName:str=''):
    strJson:str = '{"Ctrl+D":{"ButtonName":"Axis_1_P"}}' #"\"Ctrl+D\": {\"ButtonName\": \"Axis_1_P\"}"
    strJson = '{"CtrlD":{"ButtonName":"Axis_1_P"}}'
    widgetIndex = buttonName
    #print(rdoInputType.get())
    try:
        global keyButtons

        temp1 =keyButtons[buttonName]


        valID = temp1.winfo_id()


        global keyDropdowns
        temp2 = keyDropdowns[buttonName]

        val = temp2.get()
        print(val)
        # do something
        # obj:GameControls = GameControls.Deserialize(jsonFileData)
        # print(obj.CtrlD.ButtonName)
        # print(obj.W)
        # print(obj.W.KeyCode)
    except Exception as e:
        # handle it
        print("Error: " + e.args[0])
     #= #json.loads(strJson)
    #obj = GameControls(**json.loads(strJson))


def InputModeChange():
    
    myXboxButtons = getXboxButtons()
    aLength = myXboxButtons.__len__()

    myXboxSticks = getXboxSticks()
    aLength2 = myXboxSticks.__len__()

    myActions:list[str] = deepcopy(myXboxButtons)
    myActions.extend(myXboxSticks)
    ## lightblue
    global allDropdowns
    global allButtons
    global allLabels
    global keyDropdowns
    global keyButtons
    global keyLabels

    global rdoInputType
    intInputType = rdoInputType.get()

    if intInputType == '1':
        for index, aButton in enumerate(allButtons):
            aButton.configure(state=tk.DISABLED, bg="#ebebeb")
            pass
        pass
    else:
        for index, aButton in enumerate(allButtons):
            anXboxButton = myActions[index]

            if not anXboxButton.startswith("xbox_left_stick_"):
                aButton.configure(state=tk.NORMAL, bg="lightblue")
            pass
        pass

    pass

def ComboScrollOnOpen(self, event, buttonNameKey:str=''): ## self, event, 
    global keyDropdowns

    temp1 =keyDropdowns[buttonNameKey]

    
    if not buttonNameKey == "xbox_left_stick":
        pass
    # "break" which will prevent default bindings from being processed
    return "break" 


def LoadForm(myGlobalForm:tk.Misc):

    frame_top =tk.Frame(myGlobalForm, width=2000, height=550)
    frame_main = tk.Frame(frame_top, width=400, height=500)
    frame_main.grid(sticky='nw', row=2)
    radio_frame = tk.Frame(frame_top)
    radio_frame.grid()
    radio_frame.grid_columnconfigure((0,1,2), weight=1, uniform="equal")

    global rdoInputType
    rdoInputType = tk.StringVar()
    rdoInputType.set(0)

    rdoKey = tk.Radiobutton(radio_frame, text="Edit for Keyboard and Gamepad", variable=rdoInputType, value=0, command=InputModeChange)
    rdoPad = tk.Radiobutton(radio_frame, text="Edit for Controller Only", variable=rdoInputType, value=1, command=InputModeChange)
    radio_frame.grid(row=1, column=0)
    frame_top.place(x=1,y=1)
    myCanvas  = tk.Canvas(frame_main, width=680, height=400)
    myCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    second_frame = tk.Frame(myCanvas, width = 1000, height = 600, #bg="green"
                            )
    second_frame.pack(expand=1)

    rdoKey.grid(row=1, column=1, sticky=tk.NW)
    rdoPad.grid(row=1, column=2, sticky=tk.NW)
    myButtons = vars(xBtn)

    myKeys = myButtons.keys()
    #print(myKeys)
    myXboxButtons = getXboxButtons()
    aLength = myXboxButtons.__len__()

    myXboxSticks = getXboxSticks()
    aLength2 = myXboxSticks.__len__()
    
    myButtonOptions = getXboxOptions()

    myButtonNames:list[str] =[]
    myButtonValues:list[str] =[]
    for index, definition in enumerate(myButtonOptions):
        myButtonNames.append(definition.GamePadButtonName)
        myButtonValues.append(definition.GamePadButtonValue)

    # lists
    global allDropdowns
    global allButtons
    global allLabels
    # dictionaries
    global keyDropdowns
    global keyButtons
    global keyLabels


    global strScrollActions

    # Xbox Buttons
    for r in range(aLength):
        anXboxButton:str = myXboxButtons[r]

        mySubFrame = tk.Frame(second_frame, width=400)

        myData:bytes =myButtons[anXboxButton]
        
        myImage2 = tk.PhotoImage(data=myData,format="png",width=70,height=70)
        lbl = tk.Label(mySubFrame, image=myImage2, bg="#E5E5E5")

        myKeys = getControlSetting(anXboxButton)
        ## Grid Style
        specialFrame = tk.Frame(mySubFrame)
        lbl.grid(column=0,row=0, rowspan=2)
        lbl.image = myImage2 # save the image reference

        keyList:list[str] = myKeys[ConstKeyCode]  
        strSample = ', '.join(keyList)  
        myLable1:tk.Text = myControl.createTextbox(controlMaster=mySubFrame, controlText =strSample , myWidth=34,myHeight=1,readOnly=True)
        
        myLable1.configure(bg="#E5E5E5", padx=5)
        allLabels.append(myLable1)
        keyLabels[anXboxButton] = myLable1
        myLable1.grid(column=1,row=1, rowspan=1)
        
        #button_var = tk.StringVar(value=aButtonId)
        btnKeys1:tk.Button = myControl.createButton(controlMaster=specialFrame, myWidth=10,myHeight=1, controlText="Edit Keys", myCommand=lambda buttonIndex=r, buttonName=anXboxButton: LoadKeyDialog(buttonIndex, buttonName))
       
        allButtons.append(btnKeys1)
        keyButtons[anXboxButton] = btnKeys1

        specialFrame.grid(column=1,row=0, sticky="SW")

        if anXboxButton.startswith("xbox_left_stick_"):
           btnKeys1.configure(state=tk.DISABLED, bg="#ebebeb")

        btnKeys1.grid(column=0,row=0, sticky="SW")

        # optionVar = tk.StringVar(name='GamePadButtonName', value='GamePadButtonValue')
        # optionVar.set(myKeys[ConstButtonName])
        
        aDropDown = BetterCombobox(master= specialFrame, width=20, dislplayMember='GamePadButtonName', valueMember='GamePadButtonValue',values=myButtonOptions)  ##tk.OptionMenu(specialFrame, optionVar, myButtonOptions)
        aDropDown.configure(state="readonly")

        
        for strScroll in strScrollActions:
            myResult = aDropDown.bindtags()
            aDropDown.unbind_class("TCombobox", strScroll)
            
            #aDropDown.bind(strScroll,lambda buttonNameKey=anXboxButton: ComboScrollOnOpen(aDropDown, buttonNameKey, buttonNameKey))
            pass
            

        allDropdowns.append(aDropDown)
        keyDropdowns[anXboxButton] = aDropDown

        
        # for strScroll in strScrollActions:
        #     aDropDown.unbind_class("TCombobox", strScroll)

        #ComboScrollOnOpen

        if not anXboxButton == "xbox_left_stick":
            #aDropDown.current(1)
            aDropDown.set(myKeys[ConstButtonName])
            aDropDown.grid(column=1,row=0, padx=2, sticky="SW")
            
        mySubFrame.grid(row=r,column=0)

    # Xbox Sticks
    for r in range(aLength2):
        anXboxButton:str = myXboxSticks[r]

        mySubFrame = tk.Frame(second_frame, width=400)

        myData:bytes =myButtons[anXboxButton]
        myImage2 = tk.PhotoImage(data=myData,format="png",width=107,height=70)
        myImage2  = myImage2.zoom(x=7)

        img  = myImage2.subsample(x=10)
        img.configure(width=70,height=70)
        lbl = tk.Label(mySubFrame, image=img, bg="#FFFFFF")

        myKeys = getControlSetting(anXboxButton)
        ## Grid Style
        specialFrame = tk.Frame(mySubFrame)
        lbl.grid(column=0,row=0, rowspan=2)
        lbl.image = img # save the image reference

        keyList:list[str] = myKeys[ConstKeyCode]  
        strSample = ', '.join(keyList)  
        #strSample = "Sample "+ str(r) + "-" + str(0)
        myLable1:tk.Text = myControl.createTextbox(controlMaster=mySubFrame, controlText =strSample , myWidth=34,myHeight=1,readOnly=True)
        myLable1.configure(bg="#E5E5E5", padx=5)
        allLabels.append(myLable1)
        keyLabels[anXboxButton] = myLable1
        myLable1.grid(column=1,row=1, rowspan=1)
        
        buttonIndexFinal = (r + aLength)
        btnKeys1:tk.Button = myControl.createButton(controlMaster=specialFrame, myWidth=10,myHeight=1, controlText="Edit Keys", myCommand=lambda buttonIndex=buttonIndexFinal, buttonName=anXboxButton: LoadKeyDialog(buttonIndex, buttonName))
       
        allButtons.append(btnKeys1)
        keyButtons[anXboxButton] = btnKeys1

        specialFrame.grid(column=1,row=0, sticky="SW")

        
        if anXboxButton.startswith("xbox_left_stick_"):
           btnKeys1.configure(state=tk.DISABLED, bg="#ebebeb")

        btnKeys1.grid(column=0,row=0, sticky="SW")

        # optionVar = tk.StringVar(name='GamePadButtonName', value='GamePadButtonValue')
        # optionVar.set(myButtonOptions[0].GamePadButtonValue)
        # aDropDown = BetterCombobox(master= specialFrame, width=20, dislplayMember='GamePadButtonName', valueMember='GamePadButtonValue',values=myButtonOptions)  ##tk.OptionMenu(specialFrame, optionVar, myButtonOptions)
        
        # allDropdowns.append(aDropDown)

        
        aDropDown = BetterCombobox(master= specialFrame, width=20, dislplayMember='GamePadButtonName', valueMember='GamePadButtonValue',values=myButtonOptions)  ##tk.OptionMenu(specialFrame, optionVar, myButtonOptions)
        aDropDown.configure(state="readonly")
        
        for strScroll in strScrollActions:
            aDropDown.unbind_class("TCombobox", strScroll)
            aDropDown.bind(strScroll,lambda buttonIndex=r, buttonName=anXboxButton: ComboScrollOnOpen(buttonName=buttonName))
            
        allDropdowns.append(aDropDown)
        keyDropdowns[anXboxButton] = aDropDown

        if not anXboxButton == "xbox_left_stick":
            #aDropDown.current(1)
            aDropDown.set(myKeys[ConstButtonName])
            aDropDown.grid(column=1,row=0, padx=2, sticky="SW")
        
        mySubFrame.grid(row=r,column=1)
    

    myCanvas.grid(row=0, column=0, sticky="news")
    
    y_scrollbar = tk.Scrollbar(frame_main, orient=tk.VERTICAL, command=myCanvas.yview)
    y_scrollbar.configure(width=25, )
    y_scrollbar.grid(column=1, row=0, sticky="NEWS"
                     )
    #y_scrollbar.pack( side = tk.RIGHT )
    myCanvas.configure(yscrollcommand=y_scrollbar.set)

    #second_frame.configure()
    

    myCanvas.config(scrollregion=myCanvas.bbox("all"))
    myCanvas.bind('<Configure>',lambda e:myCanvas.configure(scrollregion=myCanvas.bbox('all')))

    myCanvas.create_window((0, 0), window=second_frame, anchor="nw")
    
    myGlobalForm.mainloop()
    return (True)


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

def getXboxOptions():
    buttonList: list[GamePadButton] = []
    ## Face buttons
    buttonList.append(GamePadButton(GamePadButtonName="Xbox A", GamePadButtonValue="joystick_button_0"))
    buttonList.append(GamePadButton(GamePadButtonName="Xbox B", GamePadButtonValue="joystick_button_1"))
    buttonList.append(GamePadButton(GamePadButtonName="Xbox X", GamePadButtonValue="joystick_button_2"))
    buttonList.append(GamePadButton(GamePadButtonName="Xbox Y", GamePadButtonValue="joystick_button_3"))

    ## Shoulder buttons
    buttonList.append(GamePadButton(GamePadButtonName="Xbox LB", GamePadButtonValue="joystick_button_4"))
    buttonList.append(GamePadButton(GamePadButtonName="Xbox RB", GamePadButtonValue="joystick_button_5"))
    buttonList.append(GamePadButton(GamePadButtonName="Xbox LT", GamePadButtonValue="Axis_9_P"))
    buttonList.append(GamePadButton(GamePadButtonName="Xbox RT", GamePadButtonValue="Axis_10_P"))

    ## Analog Buttons
    buttonList.append(GamePadButton(GamePadButtonName="Xbox LStick Button", GamePadButtonValue="joystick_button_8"))
    buttonList.append(GamePadButton(GamePadButtonName="Xbox RStick Button", GamePadButtonValue="joystick_button_9"))

    ## Left Stick
    buttonList.append(GamePadButton(GamePadButtonName="Xbox LStick Up", GamePadButtonValue="Axis_2_N"))
    buttonList.append(GamePadButton(GamePadButtonName="Xbox LStick Down", GamePadButtonValue="Axis_2_P"))
    buttonList.append(GamePadButton(GamePadButtonName="Xbox LStick Left", GamePadButtonValue="Axis_1_N"))
    buttonList.append(GamePadButton(GamePadButtonName="Xbox LStick Right", GamePadButtonValue="Axis_1_P"))

    ## Right Stick
    buttonList.append(GamePadButton(GamePadButtonName="Xbox RStick Up", GamePadButtonValue="Axis_5_N"))
    buttonList.append(GamePadButton(GamePadButtonName="Xbox RStick Down", GamePadButtonValue="Axis_5_P"))
    buttonList.append(GamePadButton(GamePadButtonName="Xbox RStick Left", GamePadButtonValue="Axis_4_N"))
    buttonList.append(GamePadButton(GamePadButtonName="Xbox RStick Right", GamePadButtonValue="Axis_4_P"))
    
    ## D Pad
    buttonList.append(GamePadButton(GamePadButtonName="Xbox D Pad Up", GamePadButtonValue="Axis_7_P"))
    buttonList.append(GamePadButton(GamePadButtonName="Xbox D Pad Down", GamePadButtonValue="Axis_7_N"))
    buttonList.append(GamePadButton(GamePadButtonName="Xbox D Pad Left", GamePadButtonValue="Axis_6_N"))
    buttonList.append(GamePadButton(GamePadButtonName="Xbox D Pad Right", GamePadButtonValue="Axis_6_P"))

    ## Analog Buttons
    buttonList.append(GamePadButton(GamePadButtonName="Xbox Back/View", GamePadButtonValue="joystick_button_6"))
    buttonList.append(GamePadButton(GamePadButtonName="Xbox Start/Menu", GamePadButtonValue="joystick_button_7"))

    return buttonList

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
    return xboxList

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
