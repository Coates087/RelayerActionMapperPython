import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

class pyControl:
    def createButton(controlMaster: tk.Misc, controlText="", controlFont="Segoe 10",myWidth:int=18,myHeight:int=2, myCommand:lambda:function=None):
        
        myButton = tk.Button(controlMaster, width=myWidth,height=myHeight, text=controlText, font=(controlFont), compound="right", background="lightblue", 
                             activebackground='#0398fc', command=myCommand)

        return myButton
    
    def createTextbox(controlMaster: tk.Misc, controlText="", controlFont="Segoe 9",myWidth:int=50,myHeight:int=23, readOnly=False):
        textboxState = 'normal'
        if readOnly == True:
            textboxState = 'disabled'
        myTexbox = tk.Text(controlMaster,text=controlText,width=myWidth,height=myHeight, font=(controlFont), state=textboxState)
        #myTexbox.master = controlMaster
        return myTexbox
    
    def createMultilineTextbox(controlMaster: tk.Misc, controlText="", controlFont="Segoe 9",myWidth:int=50,myHeight:int=23, readOnly=False):
        textboxState = 'normal'
        if readOnly == True:
            textboxState = 'disabled'
        myTexbox = ScrolledText(controlMaster)
        myTexbox.insert(tk.INSERT, controlText)
        myTexbox.configure(width=myWidth,height=myHeight, font=(controlFont), state=textboxState)
        #myTexbox = ScrolledText(controlMaster, image=myPixel,text=controlText,width=myWidth,height=myHeigt, font=(controlFont), compound="left", state=textboxState)
        #myTexbox.master = controlMaster
        return myTexbox