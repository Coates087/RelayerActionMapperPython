import io, base64
import time
import tkinter as tk
import ntpath
import json
from tkinter.filedialog import askopenfile, askopenfilename, asksaveasfile
import os
import constantsPython
from formControls import pyControl
from previewFile import previewFileForm
from resource_files.xbox_buttons import xBtn
from GameControlsClass import GameControls #,GameControls2


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

global allDropdowns
allDropdowns: list[tk.OptionMenu]
## https://stackoverflow.com/a/45442534

global allButtons
allButtons: list[tk.Button] = []

def LoadpdateControlsForm(controlMaster: tk.Misc, jsonData:str, myTempGameContrls:GameControls):
    #global myPreview

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

    try:
        testStr = GameControls.Serialize(myGameContrls) #myGameContrls.Serialize()
        tempContrls =GameControls.Deserialize(testStr)
    except Exception as e:
        # handle it
        print(e.args[0])
        print("Add Dummy JSON")

    if not updateControlForm == None:
        updateControlForm.grab_set() # forces focus on form
    LoadImages(updateControlForm)
   

def LoadJson():
    strJson:str = '{"Ctrl+D":{"ButtonName":"Axis_1_P"}}' #"\"Ctrl+D\": {\"ButtonName\": \"Axis_1_P\"}"
    strJson = '{"CtrlD":{"ButtonName":"Axis_1_P"}}'
    
    try:
        global allButtons

        temp1 =allButtons

        print(temp1)
        # do something
        obj:GameControls = GameControls.Deserialize(jsonFileData)
        print(obj.CtrlD.ButtonName)
        print(obj.W)
        print(obj.W.KeyCode)
    except Exception as e:
        # handle it
        print("Error: " + e.args[0])
     #= #json.loads(strJson)
    #obj = GameControls(**json.loads(strJson))




def LoadImages(myGlobalForm:tk.Misc):

   
    myFrame = tk.Frame(myGlobalForm,width=200,height=200)
    myFrame.place(y=10, x=10)

    #bytesXbox = xBtn
    myButtons = vars(xBtn)
    myXboxButtons = getXboxButtons()
    
    aLength = myXboxButtons.__len__()
    for r in range(aLength - 1):
        anXboxButton:str = myXboxButtons[r]

        mySubFrame = tk.Frame(myFrame,width=100,height=100)

        myData:bytes =myButtons[anXboxButton]
        myImage2 = tk.PhotoImage(data=myData,format="png")
        lbl = tk.Label(mySubFrame, image=myImage2)
        
        lbl.pack(in_= mySubFrame, side='left')
        lbl.image = myImage2 # save the image reference
        strSample = "Sample "+ str(r) + "-" + str(0)
        myLable1:tk.Text = myControl.createTextbox(controlMaster=myFrame, controlText =strSample , myWidth=35,myHeight=1,readOnly=True)
        myLable1.pack(in_=mySubFrame,side=tk.BOTTOM)


        
        btnKeys1:tk.Button = myControl.createButton(controlMaster=myFrame, myWidth=10,myHeight=1, controlText="Edit Keys", myCommand=LoadJson)


        global allButtons
        allButtons.append(btnKeys1)

        btnKeys1.pack(in_=mySubFrame, side=tk.BOTTOM)
        mySubFrame.grid(row=r,column=0)

    myGlobalForm.mainloop()
    return (True)


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
