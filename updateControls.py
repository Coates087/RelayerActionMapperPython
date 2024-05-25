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
import resource_files.xbox_buttons as xBtn
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

    LoadImages(updateControlForm)
    updateControlForm.grab_set() # forces focus on form
   

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

    mySubFrame = tk.Frame(myGlobalForm,width=100,height=100)

    myImage = tk.PhotoImage(data=xBtn.xbox_dpad_Down,format="png")
    canvas = tk.Canvas(myGlobalForm, width=100, height=100)
    canvas.create_image(10, 10, anchor=tk.NW, image=myImage)
    # canvas.place(y=10, x=10) 
    canvas.pack(in_= myFrame, side='left')
    myLable1:tk.Text = myControl.createTextbox(controlMaster=myGlobalForm, controlText ="Sample", myWidth=35,myHeight=1,readOnly=True)
    myLable1.pack(in_=mySubFrame,side=tk.BOTTOM)


    
    btnKeys1:tk.Button = myControl.createButton(controlMaster=myGlobalForm, myWidth=10,myHeight=1, controlText="Edit Keys", myCommand=LoadJson)


    global allButtons
    allButtons.append(btnKeys1)

    btnKeys1.pack(in_=mySubFrame,side=tk.TOP)
    mySubFrame.pack(in_= myFrame, side='left')

    myGlobalForm.mainloop()
    return (True)



