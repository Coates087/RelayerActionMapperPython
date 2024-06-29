import argparse
import base64
from binascii import Incomplete
import sys
import tkinter as tk
import ntpath
import json
from tkinter.filedialog import askopenfile, askopenfilename, asksaveasfile
import os
from typing import IO
from GameControlsClass import GameControls
import constantsPython
from formControls import ToolTip, pyControl, BetterTextBox
from helpSection import helpSectionForm
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

global defaultSavePath
defaultSavePath:str = ''

global rdoGamePadType
rdoGamePadType:tk.StringVar = None
global chkOverrideSave
chkOverrideSave:tk.StringVar = None

global strLoadedFileName
strLoadedFileName:str = ''

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

    strRez = "660x474"
    strMyOS = os_sys.uname().system
    strMac = 'Darwin' # Macs system name is called "Darwin"

    if strMyOS == 'Linux' or  strMyOS == strMac:
        strRez = '780x474'
    # Setting up main window
    root.geometry(strRez) # size of main window
    root.title("Relayer Action Mapper PE (Python Edition)")
    # myIcon =tk.PhotoImage(data=gIcons.OtherIcons.AppIcon)#, format="bitmap")
    # root.iconbitmap(myIcon) #const.programIcon)
    root.iconphoto(True, tk.PhotoImage(data=gIcons.OtherIcons.AppIconPNG, format="png"))

    global rdoGamePadType
    rdoGamePadType = tk.StringVar()
    rdoGamePadType.set(0)

    rdoXbox = tk.Radiobutton(root, text="Xbox Mode", variable=rdoGamePadType, value=0, command=GamePadModeChange)
    rdoPS = tk.Radiobutton(root, text="PS Mode", variable=rdoGamePadType, value=1, command=GamePadModeChange)
    rdoXbox.place(x=10, y=15) # Setting button position
    rdoPS.place(x=113, y=15) # Setting button position
    
    global chkOverrideSave
    chkOverrideSave = tk.StringVar()
    chkOverrideSave.set(0)
    chkOver= tk.Checkbutton(root, text='Always Override File',variable=chkOverrideSave, onvalue=1, offvalue=0)
    chkOver.place(x=461, y=15) # Setting button position
    
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

    # btnTest = myControl.createButton(controlMaster=root, controlText="Test", myCommand=openBase64File)
    # btnTest.place(x=153, y=328) # Setting button position 

    # btnBase64 = myControl.createButton(controlMaster=root, controlText="Convert Base 64", myCommand=openBase64File)
    # btnBase64.place(x=153, y=328) # Setting button position 


    btnExit = myControl.createButton(controlMaster=root, controlText="Exit", myWidth=14, myCommand=close_win)
    btnExit.configure( bg="#FF8A8A")
    btnExit.place(x=461, y=359) # Setting button position

    ToolTip(btnExit, text="Exit Relayer Action Mapper PE",bg='#ebebed',fg='black',borderColor='#333b54', borderThickness=2)


    
    myLable11:BetterTextBox = myControl.createBetterTextbox(controlMaster=root, controlText ="" , myWidth=90,myHeight=1,readOnly=True)

    myLable11.configure(bg="#E5E5E5", padx=5, borderwidth=2, relief= "solid")
    
    
    myLable12:BetterTextBox = myControl.createBetterTextbox(controlMaster=root, controlText ="" , myWidth=90,myHeight=1,readOnly=True)

    myLable12.configure(bg="#EAEAEA", padx=5, borderwidth=2, relief= "solid", fg="#DC143C")

    # relief = "flat", "raised", "sunken", "ridge", "solid", and "groove".
    keyLabels['load-file'] = myLable11
    keyLabels['warn'] = myLable12
    myLable11.place(x=10, y=60) # Setting label position

    myLable12.place(x=10, y=418) # Setting label position
    #myLable11.tab
    btnExit.place(x=461, y=359) # Setting button position
    

    btnHelp = myControl.createButton(controlMaster=root, controlText="Help", myWidth=4, myHeight=1, myCommand=OpenHelp)
    btnHelp.place(x=598, y=14) 


    
    print("\nName of Python script:", sys.argv)
    HandleArgs()
    root.mainloop()
    return (True)

def OpenHelp():
    global root
    helpSectionForm(root)
    pass

def HandleArgs():
    global defaultSavePath
    global rdoGamePadType
    global chkOverrideSave
    myString:str = ', '.join(sys.argv)
    
    # when the user enclose the path the double quotes, the second double quote might be a part of the string if it is after a "\"
    myString = myString.replace('"',",")
    myArgs:list[str] = myString.split(', ')

    print(sys.argv)
    # print(myArgs)
    argLength = myArgs.__len__()
    for i in range(argLength):
        arg = myArgs[i]

        argLower = arg.lower()
        if argLower == '-ps':
            print('Turning on PS Mode...')
            rdoGamePadType.set(1) # setting the program to PlayStation mode
            pass
        elif argLower.startswith('-load'):
            myFileName:str = ''
            if argLower == '-load':
                if i+1 <= argLength:
                    myFileName = myArgs[i+1] # the path is in the next element of the array
                pass
            else:
                myFileName = arg.replace('-load ','')
                pass
            print(fr'Found File Path: {myFileName}')
            if os.path.isfile(myFileName):
                print(fr'Opening File: {myFileName}')
                f = open(myFileName, "r")
                myFileContents = f.read()
                f.close()
                loadConfigFile(myFileName, myFileContents)
                pass

        elif argLower.startswith('-save'):
            myPath:str = ''
            if argLower == '-save':
                if i+1 <= argLength:
                    myPath = myArgs[i+1] # the path is in the next element of the array
                pass
            else:
                myPath = arg.replace('-save ','')
                pass
            # when the user enclose the path the double quotes, the second double quote might be a part of the string if it is after a "\"
            myPath = myPath.replace('"','')
            print(fr'Checking Path: {myPath}')
            if os.path.isdir(myPath):
                print(fr'Setting Path: {myPath}')
                defaultSavePath = myPath
                pass

        elif argLower == '-overridesave':
            
            chkOverrideSave.set(1)
            pass


        # pass
    pass

def GamePadModeChange():
    global rdoGamePadType
    selecteMode = rdoGamePadType.get()

    if selecteMode == '0':
        print('Xbox Mode')
    else:
        print('PlayStation Mode')

    pass

def openSpecialFile():
    textResult:str = ''
    
    global rdoGamePadType
    selecteMode = rdoGamePadType.get()

    if selecteMode == '1':
        textResult = defaultConfigs.json_control_data.default_PS_config.decode()
        pass
    else:
        textResult = defaultConfigs.json_control_data.default_xbox_config.decode()
        pass
    # textResult = defaultConfigs.json_control_data.default_xbox_config.decode()
    # textResult = defaultConfigs.json_control_data.default_xbox_test_config.decode()
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
    
    textData:str = ''
    psMode: bool = False
    match strType:
        case defaultConfigOptions.defaultConfigOp:
            textData = defaultConfigs.json_control_data.default_config.decode()
            pass
        case defaultConfigOptions.defaultXboxConfigOp:
            textData = defaultConfigs.json_control_data.default_xbox_config.decode()
            pass
        case defaultConfigOptions.defaultPlayStationConfigOp:
            textData = defaultConfigs.json_control_data.default_PS_config.decode()
            psMode = True
            pass
        case defaultConfigOptions.defaultKeyboardConfigOp:
            textData = defaultConfigs.json_control_data.default_keyboard_config.decode()
            pass
        case _:
            textData = defaultConfigs.json_control_data.default_config.decode()
            pass
    
    
    global rdoGamePadType
    global fileContents 
    global keyLabels
    lblFile = keyLabels['load-file'] #tk.Text
    lblText = lblFile.get_value()

    loadSavedFile:bool = False
    if (lblText == '' or lblText == None) and fileContents == '':
        loadSavedFile = True
        pass
    saveResult = saveConfigFile(textData,False,loadSavedFile)

    if saveResult == True and loadSavedFile == True:
        if psMode == True:
            rdoGamePadType.set(1)
            pass
        else:
            rdoGamePadType.set(0)

    pass

def prepSaveConfig():
    global myGameContrls
    global fileContents 
    global rdoGamePadType

    selectedGamePadMode = rdoGamePadType.get()
    strSpecialMessage = 'No config file has been loaded. Please load a config file, or click the "Edit Controls" button in order to save your controls.'
    if fileContents == '':
        
        from tkinter import messagebox 
        messageResult = messagebox.showwarning("Information", strSpecialMessage)
        pass
    else:
        
        global keyLabels
        lblFile = keyLabels['load-file'] #tk.Text
        lblText = lblFile.get_value()

        loadSavedFile:bool = False
        if lblText == '':
            loadSavedFile = True
            pass
        strJson = myGameContrls.Serialize(4)
        saveConfigFile(strJson, True, loadSavedFile)
    pass

def saveConfigFile(strJson:str, clearMessage:bool = False, loadFile:bool = False):
    global chkOverrideSave
    global defaultSavePath
    global strLoadedFileName

    defaultFileName = "KeyConfig.json"
    saveSuccess:bool = False

    if strLoadedFileName != '':
        defaultFileName = strLoadedFileName
        pass

    boolConfirmoverwrite:bool= True
    chkVal = chkOverrideSave.get()
    if chkVal == '1':
        boolConfirmoverwrite = False
        pass
    myFile: IO[Incomplete] | None

    if os.path.isdir(defaultSavePath):
        myFile = asksaveasfile(mode='w',initialfile = defaultFileName, initialdir=defaultSavePath, confirmoverwrite=boolConfirmoverwrite, defaultextension="json",filetypes=[("JSON", ".json")])
        pass
    else:
        myFile = asksaveasfile(mode='w',initialfile = defaultFileName, confirmoverwrite=boolConfirmoverwrite, defaultextension="json",filetypes=[("JSON", ".json")])
        pass
    
    if not myFile == None:
        myFileName:str = myFile.name
        myFile.write(strJson)
        myFile.close()
        saveSuccess = True
        if loadFile == True:
            loadConfigFile(myFileName,strJson)
            pass

        if clearMessage == True:
            global keyLabels
            keyLabels['warn'].set_value("")
            
            pass

        from tkinter import messagebox 
        import subprocess 
        #from showinfm import show_in_file_manager
        messageResult = messagebox.askyesno("Save Successful", "Do you wish to open the directory for this file?") 
        if messageResult == True:
            aPath =os.path.realpath(myFileName)
            programOpen:str = ''
            
            strMac = 'Darwin' # Macs system name is called "Darwin"

            # we need to determent the os in order to properly unbind and rebind the mouse scroll os_sys
            strMyOS = os_sys.uname().system

            strFullPath:str = ''
            if strMyOS == 'Windows': 
                programOpen = 'explorer   /select'
                strFullPath = fr'"{aPath}"'
            elif strMyOS == strMac:
                programOpen = 'open' # untested
                strFullPath = fr'{os.path.dirname(aPath)}'
            else: # Linux
                programOpen = 'xdg-open'
                strFullPath = fr'{os.path.dirname(aPath)}'
                # os.system('xdg-open "%s"' % aPath)
                pass
            try:
                if strMyOS == 'Windows':
                    subprocess.Popen(fr'{programOpen}, {strFullPath}') ## open
                else:
                    subprocess.Popen([programOpen, strFullPath]) ## open
            except Exception as e:
                print(e)
                pass
            # subprocess.Popen(fr'{programOpen}  /select, "{aPath}"') ## open
            pass
        pass
    return saveSuccess

def openConfigFile():
    #
    myFile = askopenfile(mode='r',defaultextension="json",filetypes=[("JSON", ".json")])

    if not myFile == None:
        myFileName = myFile.name
        textResult = myFile.read()
        myFile.close()
        loadConfigFile(myFileName,textResult)

        print("File Found: " + myFileName)
    else:
        print("No file selected")


def loadConfigFile(strFileName:str, strFileContents:str):
    global strLoadedFileName    
    global fileContents 
    fileContents = strFileContents

    try:
        # do something
        obj:GameControls = GameControls.Deserialize(fileContents)

        global myGameContrls
        myGameContrls = obj
        
        global keyLabels
        lblFile = keyLabels['load-file'] #tk.Text

        if not lblFile == None:
            fileNameOnly:str = os.path.basename(strFileName) ## test this in linux
            strLoadedFileName =  fileNameOnly
            labelText = "File Loaded: " + fileNameOnly
            lblFile.set_value(labelText)
            pass

        
    except Exception as e:
        # handle it
        print("Error: " + e.args[0])
    pass

def previewFile():
    previewFileForm(root, fileContents)


def updateControls():
    global myGameContrls
    
    global rdoGamePadType

    selectedGamePadMode = rdoGamePadType.get()
    strSpecialMessage = 'No config file has been loaded. Do you wish to edit the controls from a pre-made configuration?'
    if fileContents == '':
        
        from tkinter import messagebox 
        messageResult = messagebox.askyesno("Information", strSpecialMessage)
        if messageResult == True:
            openSpecialFile()
            pass
        else:
            return
        
    LoadpdateControlsForm(root, fileContents, myGameContrls, selectedGamePadMode)

def testFunction():

    # from tkinter import messagebox 
    # import subprocess 
    # messageResult = messagebox.askyesno("Save Successful", "Do you wish to open the directory for this file?") 
    # if messageResult == True:
    #     aPath =os.path.realpath(myFileName)
    #     programOpen:str = ''
        
    #     strMac = 'Darwin' # Macs system name is called "Darwin"

    #     # we need to determent the os in order to properly unbind and rebind the mouse scroll os_sys
    #     strMyOS = os_sys.uname().system
        
    #     if strMyOS == 'Windows': 
    #         programOpen = 'explorer'
    #     elif strMyOS == strMac:
    #         programOpen = 'open'
    #     else: # Linux
    #         programOpen = 'xdg-open'
    #         # os.system('xdg-open "%s"' % aPath)
    #         pass
    #     try
    #         subprocess.Popen(fr'{programOpen}  /select, "{aPath}"') ## open
    #     except Exception as e:
    #         print(e)
    #         pass

    #     pass
    pass

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
        print()
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