import base64
import tkinter as tk
import ntpath
import json
from tkinter.filedialog import askopenfile, askopenfilename, asksaveasfile
import os
from GameControlsClass import GameControls
import constantsPython
from formControls import pyControl, BetterTextBox
from previewFile import previewFileForm
from updateControls import LoadpdateControlsForm
import platform as os_sys
#import updateControls.LoadpdateControlsForm

#import updateControls
import resource_files.xbox_buttons as xBtn
import resource_files.general_icons as gIcons
import resource_files.default_controls as defaultConfigs


const = constantsPython.strResourcePath()
global myControl

myControl = pyControl

global root
root:tk.Tk = None

global saveWarn
saveWarn:str 
saveWarn = "Click on the <<Save File>> button to save your changes."

global unsaved
unsaved:bool = False

class defaultConfigOptions:
    defaultConfigOp:str = 'defaultConfig'
    
    defaultXboxConfigOp:str = 'defaultXboxConfig'
    
    defaultPlayStationConfigOp:str = 'defaultPlayStationConfig'
    
    defaultKeyboardConfigOp:str = 'defaultKeyboardConfig'


global keyLabels
keyLabels: dict[str,BetterTextBox] = {}

## also try PyInstaller

## for compiling this program: 
## python -m PyInstaller --clean --onefile --noconsole --icon "../resource_objects/RelayerIcon.png" --specpath "./build/" --distpath  "./build/dist/" main.py --name "Relayer Action Mapper Python" 

## pixel = tk.PhotoImage(width=1, height=1)
global fileContents
fileContents: str = ""

global myGameContrls
myGameContrls:GameControls = None


class mainWin:
    def setGameControlChanges(changes:bool, textResult:str):
    
        global fileContents 
        global myGameContrls
        global keyLabels
        global saveWarn
        fileContents = textResult

        global unsaved
        unsaved = True #changes

        obj:GameControls = GameControls.Deserialize(fileContents)

        myGameContrls = obj

        if unsaved == True:
            keyLabels['warn'].set_value(saveWarn)
            pass
        pass
    pass    

def close_win():
   root.destroy()


def StartMain():
    global root
    root = tk.Tk()

    # Setting up main window
    root.geometry("660x473") # size of main window
    root.title("Relayer Action Mapper")
    # myIcon =tk.PhotoImage(data=gIcons.OtherIcons.AppIcon)#, format="bitmap")
    # root.iconbitmap(myIcon) #const.programIcon)
    root.iconphoto(True, tk.PhotoImage(data=gIcons.OtherIcons.AppIconPNG, format="png"))
    
    global keyLabels

    btnLoadFile = myControl.createButton(controlMaster=root, controlText="Load File", myCommand=openConfigFile)
    btnLoadFile.place(x=53, y=87) # Setting button position
    
    btnSaveFile = myControl.createButton(controlMaster=root, controlText="Save File", myCommand=prepSaveConfig)
    btnSaveFile.place(x=53, y=147) # Setting button position


    btnUpdateCtrls = myControl.createButton(controlMaster=root, controlText="Edit Controls", myCommand=updateControls)
    btnUpdateCtrls.place(x=231, y=87) # Setting button position 

    btnPreview = myControl.createButton(controlMaster=root, controlText="Preview Config File", myWidth=22, myCommand=previewFile)
    btnPreview.place(x=461, y=87) # Setting button position 

    configButtonWidth:int 
    configButtonWidth= 34
    configButtonX:int 
    configButtonX = 363

    btnDefault = myControl.createButton(controlMaster=root, controlText="Create Default Config File", myWidth=configButtonWidth, myCommand=lambda:prepDefaultConfig(defaultConfigOptions.defaultConfigOp))
    btnDefault.place(x=configButtonX, y=147) # Setting button position 

    btnXbox = myControl.createButton(controlMaster=root, controlText="Create Xbox Game Pad Config File", myWidth=configButtonWidth, myCommand=lambda:prepDefaultConfig(defaultConfigOptions.defaultXboxConfigOp))
    btnXbox.place(x=configButtonX, y=198) # Setting button position 

    btnPS = myControl.createButton(controlMaster=root, controlText="Create PlayStation Game Pad Config File", myWidth=configButtonWidth, myCommand=lambda:prepDefaultConfig(defaultConfigOptions.defaultPlayStationConfigOp))
    btnPS.place(x=configButtonX, y=249) # Setting button position 

    btnKeyboard = myControl.createButton(controlMaster=root, controlText="Create Keyboard Config File", myWidth=configButtonWidth, myCommand=lambda:prepDefaultConfig(defaultConfigOptions.defaultKeyboardConfigOp))
    btnKeyboard.place(x=configButtonX, y=300) # Setting button position 


    btnBase64 = myControl.createButton(controlMaster=root, controlText="Convert Base 64", myCommand=openBase64File)
    btnBase64.place(x=153, y=328) # Setting button position 


    btnExit = myControl.createButton(controlMaster=root, controlText="Exit", myWidth=14, myCommand=close_win)
    btnExit.configure( bg="#FF8A8A")
    btnExit.place(x=461, y=359) # Setting button position


    
    myLable11:BetterTextBox = myControl.createBetterTextbox(controlMaster=root, controlText ="" , myWidth=90,myHeight=1,readOnly=True)

    myLable11.configure(bg="#E5E5E5", padx=5, borderwidth=2, relief= "solid")
    
    
    myLable12:BetterTextBox = myControl.createBetterTextbox(controlMaster=root, controlText ="" , myWidth=90,myHeight=1,readOnly=True)

    myLable12.configure(bg="#EAEAEA", padx=5, borderwidth=2, relief= "solid", fg="red")

    # relief = "flat", "raised", "sunken", "ridge", "solid", and "groove".
    keyLabels['load-file'] = myLable11
    keyLabels['warn'] = myLable12
    myLable11.place(x=10, y=60) # Setting label position

    myLable12.place(x=10, y=418) # Setting label position
    #myLable11.tab
    btnExit.place(x=461, y=359) # Setting button position
    # 'saveWarn'
    # canvas = tk.Canvas(root, width=300, height=300)
    # canvas.pack()
    # canvas.create_image(20, 20, anchor=tk.NW, image=myImage)
    ## root.configure(background=myImage)
    root.mainloop()
    return (True)

def openSpecialFile():

    # textResult = defaultConfigs.json_control_data.default_xbox_config.decode()
    textResult = defaultConfigs.json_control_data.default_xbox_test_config.decode()
    global fileContents 
    fileContents = textResult
    
    try:
        # do something
        obj:GameControls = GameControls.Deserialize(fileContents)

        global myGameContrls
        myGameContrls = obj
        
    except Exception as e:
        # handle it
        print("Error: " + e.args[0])


def prepDefaultConfig(strType:str =''):
    
    textData:str #defaultConfigs.json_control_data.default_xbox_config.decode()
    match strType:
        case defaultConfigOptions.defaultConfigOp:
            textData = defaultConfigs.json_control_data.default_config.decode()
            pass
        case defaultConfigOptions.defaultXboxConfigOp:
            textData = defaultConfigs.json_control_data.default_xbox_config.decode()
            pass
        case defaultConfigOptions.defaultPlayStationConfigOp:
            textData = defaultConfigs.json_control_data.default_PS_config.decode()
            pass
        case defaultConfigOptions.defaultKeyboardConfigOp:
            textData = defaultConfigs.json_control_data.default_keyboard_config.decode()
            pass
        case _:
            textData = defaultConfigs.json_control_data.default_config.decode()
            pass

    saveConfigFile(textData)
    pass

def prepSaveConfig():
    global myGameContrls
    strJson = myGameContrls.Serialize()
    saveConfigFile(strJson, True)
    pass

def saveConfigFile(strJson:str, clearMessage:bool = False):
    #myFile:any
    myFile = asksaveasfile(mode='w',initialfile = "KeyConfig.json", defaultextension="json",filetypes=[("JSON", ".json")])
    #KeyConfig.json
    if not myFile == None:
        myFileName:str = myFile.name
        myFile.write(strJson)
        myFile.close()

        if clearMessage == True:
            global keyLabels
            keyLabels['warn'].set_value("")
            
            pass

        from tkinter import messagebox 
        import subprocess 
        messageResult = messagebox.askyesno("Save Successful", "Do you wish to open the directory for this file?") 
        if messageResult == True:
            aPath =os.path.realpath(myFileName)
            programOpen:str = ''
            
            strMac = 'Darwin' # Macs system name is called "Darwin"

            # we need to determent the os in order to properly unbind and rebind the mouse scroll os_sys
            strMyOS = os_sys.uname().system
            
            if strMyOS == 'Windows': 
                programOpen = 'explorer'
            elif strMyOS == strMac:
                programOpen = 'open'
            else: # Linux
                programOpen = 'xdg-open'
                # os.system('xdg-open "%s"' % aPath)
                pass
            # ubprocess.Popen(f'explorer {os.path.realpath(path)}')
            subprocess.Popen(fr'{programOpen}  /select, "{aPath}"')            ## open
            #os.system(f'start "{os.path.realpath(myFileName)}"')
            pass
        pass

def openConfigFile():
    #
    myFile = askopenfile(mode='r',defaultextension="json",filetypes=[("JSON", ".json")])

    if not myFile == None:
        myFileName = myFile.name
        textResult = myFile.read()
        myFile.close()
        global fileContents 
        fileContents = textResult
        
        try:
            # do something
            obj:GameControls = GameControls.Deserialize(fileContents)

            global myGameContrls
            myGameContrls = obj
            
            global keyLabels
            lblFile = keyLabels['load-file'] #tk.Text

            if not lblFile == None:
                fileNameOnly:str = os.path.basename(myFileName) ## test this in linux
                labelText = "File Loaded: " + fileNameOnly
                lblFile.set_value(labelText)
                pass

            
        except Exception as e:
            # handle it
            print("Error: " + e.args[0])

        print("File Found: " + myFileName)
    else:
        print("No file selected")


def previewFile():
    previewFileForm(root, fileContents)


def updateControls():
    global myGameContrls
    if fileContents == '':
        openSpecialFile()
        
    LoadpdateControlsForm(root, fileContents, myGameContrls)

def openBase64File():
    
    myFile = askopenfile(mode='r')

    if not myFile == None:
        myFileName = myFile.name
        myFile.close()

        onlyFile = ntpath.basename(myFileName)
        textResult =""
        with open(myFileName, "rb") as image_file:
            textResult = base64.b64encode(image_file.read())

        # textResult = myFile.read()
        decoded = base64.b64decode(textResult)
        print("printing: " + myFileName)
        print(decoded)
        currentDir = os.getcwd()
        finalPath = currentDir + "/temp/" + onlyFile + ".txt"
        
        os.makedirs(os.path.dirname(finalPath), exist_ok=True)
        f = open(finalPath, "w")
        myDataStr = repr(decoded)
        f.write(myDataStr)
        f.close()


# if root == None:
#     StartMain()
#     pass