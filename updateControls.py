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
from GameControlsClass import GameControls
from tkinter.tix import ScrolledWindow


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
    #LoadForm()
   

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


def LoadForm():
    root = tk.Tk()
    root.grid_rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    frame_main = tk.Frame(root, bg="gray")
    frame_main.grid(sticky='news')

    label1 = tk.Label(frame_main, text="Label 1", fg="green")
    label1.grid(row=0, column=0, pady=(5, 0), sticky='nw')

    label2 = tk.Label(frame_main, text="Label 2", fg="blue")
    label2.grid(row=1, column=0, pady=(5, 0), sticky='nw')

    label3 = tk.Label(frame_main, text="Label 3", fg="red")
    label3.grid(row=3, column=0, pady=5, sticky='nw')

    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(frame_main)
    frame_canvas.grid(row=2, column=0, pady=(5, 0), sticky='nw')
    frame_canvas.grid_rowconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(0, weight=1)
    # Set grid_propagate to False to allow 5-by-5 buttons resizing later
    frame_canvas.grid_propagate(False)

    # Add a canvas in that frame
    canvas = tk.Canvas(frame_canvas, bg="yellow")
    canvas.grid(row=0, column=0, sticky="news")

    # Link a scrollbar to the canvas
    vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=vsb.set)
    # Create a frame to contain the buttons
    frame_buttons = tk.Frame(canvas, bg="blue")
    canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

    # Add 9-by-5 buttons to the frame
    rows = 9
    columns = 5
    buttons = [[tk.Button() for j in range(columns)] for i in range(rows)]
    for i in range(0, rows):
        for j in range(0, columns):
            buttons[i][j] = tk.Button(frame_buttons, text=("%d,%d" % (i+1, j+1)))
            buttons[i][j].grid(row=i, column=j, sticky='news')

    # Update buttons frames idle tasks to let tkinter calculate buttons sizes
    frame_buttons.update_idletasks()

    # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
    first5columns_width = sum([buttons[0][j].winfo_width() for j in range(0, 5)])
    first5rows_height = sum([buttons[i][0].winfo_height() for i in range(0, 5)])
    frame_canvas.config(width=first5columns_width + vsb.winfo_width(),
                        height=first5rows_height)

    # Set the canvas scrolling region
    canvas.config(scrollregion=canvas.bbox("all"))

    # Launch the GUI
    root.mainloop()

def LoadImages(myGlobalForm:tk.Misc):

    frame_top =tk.Frame(myGlobalForm)
    frame_main = tk.Frame(frame_top, width=400, height=500)
    #rame_main.grid(sticky='news')
    frame_main.pack(fill=tk.BOTH, side=tk.LEFT, expand=0)

    frame_top.pack(fill=tk.BOTH, expand=0)
    
    #frame_canvas.grid_propagate(False)


    myCanvas  = tk.Canvas(frame_main,bg="yellow", width=400, height=400)
    myCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    second_frame = tk.Frame(myCanvas, width = 1000, height = 600, bg="green")
    second_frame.pack(expand=1)
    #bytesXbox = xBtn
    myButtons = vars(xBtn)
    myXboxButtons = getXboxButtons()
    
    aLength = myXboxButtons.__len__()
    for r in range(aLength):
        anXboxButton:str = myXboxButtons[r]

        mySubFrame = tk.Frame(second_frame)#,width=100,height=100)

        myData:bytes =myButtons[anXboxButton]
        myImage2 = tk.PhotoImage(data=myData,format="png",width=70,height=70)
        lbl = tk.Label(mySubFrame, image=myImage2, bg="#B1B1B1")
        
        lbl.pack(in_= mySubFrame, side='left')
        lbl.image = myImage2 # save the image reference
        strSample = "Sample "+ str(r) + "-" + str(0)
        myLable1:tk.Text = myControl.createTextbox(controlMaster=mySubFrame, controlText =strSample , myWidth=35,myHeight=1,readOnly=True)
        myLable1.pack(in_=mySubFrame,side=tk.BOTTOM)


        
        btnKeys1:tk.Button = myControl.createButton(controlMaster=mySubFrame, myWidth=10,myHeight=1, controlText="Edit Keys", myCommand=LoadJson)


        global allButtons
        allButtons.append(btnKeys1)

        btnKeys1.pack(in_=mySubFrame, side=tk.BOTTOM)
        mySubFrame.grid(row=r,column=0)

    
    myCanvas.grid(row=0, column=0, sticky="news")
    
    y_scrollbar = tk.Scrollbar(frame_main, orient=tk.VERTICAL, command=myCanvas.yview)
    y_scrollbar.grid(column=2, row=0, sticky="NS")
    #y_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
    myCanvas.configure(yscrollcommand=y_scrollbar.set)
    #y_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
    

    myCanvas.config(scrollregion=myCanvas.bbox("all"))
    myCanvas.bind('<Configure>',lambda e:myCanvas.configure(scrollregion=myCanvas.bbox('all')))

    myCanvas.create_window((0, 0), window=second_frame, anchor="nw")
    
    #frame_main.pack(height=100,width=350) 
    #frame_main.place(x=500,y=0,height=1000,width=837) 
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
