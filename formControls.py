import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import json


class pyControl:
    def createButton(controlMaster: tk.Misc, controlText="", controlFont="Segoe 10",myWidth:int=18,myHeight:int=2, myCommand:lambda:function=None):
        
        myButton = tk.Button(controlMaster, width=myWidth,height=myHeight, text=controlText, font=(controlFont), compound="right", background="lightblue", 
                             activebackground='#0398fc', command=myCommand)

        return myButton
    
    def createTextbox(controlMaster: tk.Misc, controlText="", controlFont="Segoe 9",myWidth:int=50,myHeight:int=23, readOnly=False):
        textboxState = 'normal'
        if readOnly == True:
            textboxState = 'disabled'
        myTexbox = tk.Text(controlMaster)
        myTexbox.insert(tk.INSERT, controlText)
        myTexbox.configure(width=myWidth,height=myHeight, font=(controlFont), state=textboxState)
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
                #d = dictionaryResult.get(valueMember)
                self.dict = newDict #.get(valueMember)
                # for r in range(optionsVals.__len__()):
                #     anOption = optionsVals[r]
                #     results = vars_recursive(anOption)
                #     self.dict = optionsVals[valueMember]

        
        optionVals2:list[str] = [] #self.dict.values().mapping #.values()
        
        for index, definition in enumerate(self.dict.values()):
            optionVals2.append(definition)
            
        # combobox constructor with list of keys
        ttk.Combobox.__init__(self,master=master, values=optionVals2)
        #ttk.Combobox.__init__(self,master=master, **optionVals2)

        # assign some function
        self.bind('<<ComboboxSelected>>', self.on_select)

    def on_select(self, event):
        print(self.get(), self.get_key(), self.get_value())

    # overwrite `get()` to return `value` instead of `key`
    def get(self):                              
        if self.dict:
            #v = self.get()
            d =ttk.Combobox.get(self)
            myKeys = list(self.dict.keys())
            myVals = list(self.dict.values())
            myIndex = myVals.index(d)
            result = myKeys[myIndex]
            return result #self.dict[ttk.Combobox.get(self)]
        else:
            return ttk.Combobox.get(self)

    def get_key(self):
        return ttk.Combobox.get(self)

    def get_value(self):                              
        return self.get()
    

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