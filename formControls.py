import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import json


    ## see here for tooltop: https://stackoverflow.com/a/65524559
class ToolTip:
    def __init__(self,widget,text=None, bg=None, fg=None, borderColor=None, borderThickness=None):
        self.borderColor =borderColor
        self.bg =bg
        self.fg =fg
        self.borderThickness =borderThickness
        # self.borderColor =borderColor
        # self.borderColor =borderColor

        def on_enter(event):
            self.tooltip=tk.Toplevel()
            self.tooltip.overrideredirect(True)
            self.tooltip.geometry(f'+{event.x_root+15}+{event.y_root+10}')

            self.label=tk.Label(self.tooltip,text=self.text, anchor='nw')

            if bg != None:
                self.label.configure(bg=bg)
            if fg != None:
                self.label.configure(fg=fg)
            if borderColor != None:
                self.label.configure(highlightbackground=borderColor)
            if borderThickness != None:
                self.label.configure(highlightthickness=borderThickness)

            self.label.pack()

        def on_move(event):
            self.tooltip.geometry(f'+{event.x_root+15}+{event.y_root+10}')


        def on_leave(event):
            self.tooltip.destroy()

        self.widget=widget
        self.text=text

        self.widget.bind('<Enter>',on_enter)
        self.widget.bind('<Motion>',on_move)
        self.widget.bind('<Leave>',on_leave)
        pass

class pyControl:
    def createButton(controlMaster: tk.Misc, controlText="", controlFont="Segoe 10",myWidth:float=18,myHeight:float=2, myCommand:lambda:function=None):
        
        myButton = tk.Button(controlMaster, width=myWidth,height=myHeight, text=controlText, font=(controlFont), compound="right", background="lightblue", 
                             activebackground='#0398fc', command=myCommand)

        return myButton
    
    def createTextbox(controlMaster: tk.Misc, controlText="", controlFont="Segoe 9",myWidth:float=50,myHeight:float=23, readOnly=False):
        textboxState = 'normal'
        if readOnly == True:
            textboxState = 'disabled'
        myTexbox = tk.Text(controlMaster)
        myTexbox.insert(tk.INSERT, controlText)
        myTexbox.configure(width=myWidth,height=myHeight, font=(controlFont), state=textboxState)
        #myTexbox.master = controlMaster
        return myTexbox
        
    def createBetterTextbox(controlMaster: tk.Misc, controlText="", controlFont="Segoe 9",myWidth:float=50,myHeight:float=23, readOnly=False):
        textboxState = 'normal'
        if readOnly == True:
            textboxState = 'disabled'
        myTexbox = BetterTextBox(controlMaster)
        myTexbox.set_value(controlText)
        myTexbox.configure(width=myWidth,height=myHeight, font=(controlFont), state=textboxState)
        #myTexbox.master = controlMaster
        return myTexbox
    
    def createMultilineTextbox(controlMaster: tk.Misc, controlText="", controlFont="Segoe 9",myWidth:float=50,myHeight:float=23, readOnly=False):
        textboxState = 'normal'
        if readOnly == True:
            textboxState = 'disabled'
        myTexbox = ScrolledText(controlMaster)
        myTexbox.insert(tk.INSERT, controlText)
        myTexbox.configure(width=myWidth,height=myHeight, font=(controlFont), state=textboxState)
        #myTexbox = ScrolledText(controlMaster, image=myPixel,text=controlText,width=myWidth,height=myHeigt, font=(controlFont), compound="left", state=textboxState)
        #myTexbox.master = controlMaster
        return myTexbox


class BetterTextBox(tk.Text):
    def get_value(self):
        myText = self.get("1.0",tk.END) # get textbox value

        myTextLength = myText.__len__()
        if myTextLength > 0:
            myText = myText[:-1]

        return myText
    
    def set_value(self,labelText:str=''):
        myStatus =self["state"]

        if myStatus == "disabled":
            self.config(state='normal')

        self.delete("1.0",tk.END) # clears textbox
        self.insert(tk.INSERT, labelText) # sets textbox value
        
        if myStatus == "disabled":
            self.config(state='disabled')
        pass

## Source: https://stackoverflow.com/a/41369025    
class BetterCombobox(ttk.Combobox):
    isDict = False
    def __init__(self, master=None, cnf={}, dislplayMember:str = '', valueMember:str='', **options):

        self.dict = None
        self.master = master

        # get dictionary from options and put list of keys
        if 'values' in options:
            optionsVals =options.get('values')
            if isinstance(options.get('values'), dict):
                isDict = True
                self.dict = options.get('values')
                options['values'] = sorted(self.dict.keys())
            elif isinstance(options.get('values'), list):
                jsonText = json.dumps(optionsVals,default=vars)
                dictionaryResult = json.loads(jsonText)

                newDict:dict[str,any] = {}       
                for index, definition in enumerate(dictionaryResult):
                    a1 = definition[valueMember]
                    newDict[a1] = definition[dislplayMember]
                   
                    pass
                self.dict = newDict 
        
        optionVals2:list[str] = [] #self.dict.values().mapping #.values()
        
        for index, definition in enumerate(self.dict.values()):
            optionVals2.append(definition)
            
        # combobox constructor with list of keys
        ttk.Combobox.__init__(self,master=master, values=optionVals2)
        # assign some function
        # self.bind('<<ComboboxSelected>>', self.on_select)

    def on_select(self, event):
        print(self.get(), self.get_key(), self.get_value())

    # overwrite `get()` to return `value` instead of `key`
    def get(self):                              
        if self.dict:
            #v = self.get()
            result = ''
            try:
                d =ttk.Combobox.get(self)
                myKeys = list(self.dict.keys())
                myVals = list(self.dict.values())
                myIndex = myVals.index(d)
                result = myKeys[myIndex]
            
            except:
                pass
            return result #self.dict[ttk.Combobox.get(self)]
        else:
            return ttk.Combobox.get(self)

    def get_key(self):
        return ttk.Combobox.get(self)

    def get_value(self):                              
        return self.get()
    
    
    # overwrite `get()` to return `value` instead of `key`
    def set(self, value:any):                              
        if self.dict:
            #v = self.get()
            result = ''
            myIndex = 0
            try:
                #call(self._w, "set", value)
                #ttk.Combobox.set()
                # =ttk.Combobox.get(self)
                myKeys = list(self.dict.keys())
                myVals = list(self.dict.values())
                myIndex = myKeys.index(value)
                result = myKeys[myIndex]
                self.current(myIndex)
            except:
                pass
            #self.dict[ttk.Combobox.get(self)]
        else:
            self.current(myIndex)

    # def get_key(self):
    #     return ttk.Combobox.get(self)

    # def get_value(self):                              
    #     return self.get()
    

def vars_recursive(obj, key1:str =''):
    objFinal = vars(obj)
    for key, value in objFinal.items():
        if (not value == None and not isinstance(value, str) and not isinstance(value, float)) and not isinstance(value, list): #and not isinstance(value, str) and not isinstance(value, float)
            try:
                vars(value)
                objFinal[key] = vars_recursive(value, key)
            except Exception as e:
                print(value)
                pass
            
        
    return objFinal