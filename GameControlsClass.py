import json
from typing import Any
from dataclasses import dataclass
from copy import copy, deepcopy

class KeyboardClass:
    def __init__(self, KeyCode:str, KeyName:str):
        self.KeyCode = KeyCode
        self.KeyName = KeyName


        

class GenericKeyButtonName2:
    def __init__(self, ButtonName:str, XBoxButton:str = ''):
        self.ButtonName = ButtonName
        self.XBoxButton = XBoxButton




class GenericKey2(GenericKeyButtonName2):
  def __init__(self, ButtonName:str, KeyCode:list[str], XBoxButton:str = ''):
    self.KeyCode = KeyCode
    super().__init__(self, ButtonName, XBoxButton) 

# @dataclass
# class CtrlD:
#     def __init__(self, Key:GenericKeyButtonName):
#         super().__init__(self,Key.ButtonName, Key.XBoxButton)
    
#     def from_dict(obj: GenericKeyButtonName) -> 'CtrlD':
#         print(obj.ButtonName)
#         # _KeyCode = [tk.from_dict(y) for y in obj.get("KeyCode")]
#         # _ButtonName = str(obj.get("ButtonName"))
#         # return CtrlD(_KeyCode, _ButtonName)

@dataclass
class GenericKeyCode:
    KeyCode:list[str]
    def __init__(self, KeyCode:list[str]):
        self.KeyCode = KeyCode

@dataclass        
class GenericKey:
    ButtonName: str
    XBoxButton:str
    KeyCode:list[str]
    def __init__(self, ButtonName:str, KeyCode:list[str], XBoxButton:str = ''):
        self.KeyCode = KeyCode
        self.ButtonName = ButtonName
        self.XBoxButton = XBoxButton

@dataclass
class GenericKeyButtonName:
    ButtonName: str
    XBoxButton:str
    def __init__(self, ButtonName: str, XBoxButton:str = '') -> None:
        self.ButtonName = ButtonName
        self.XBoxButton = XBoxButton


@dataclass
class GameControls:
    # region Description
    CtrlD:GenericKeyButtonName
    CtrlA:GenericKeyButtonName
    CtrlW:GenericKeyButtonName
    CtrlS:GenericKeyButtonName
    Enter:GenericKey
    Backspace:GenericKey
    Tab:GenericKey
    W:GenericKey
    S:GenericKey
    A:GenericKey
    D:GenericKey
    Q:GenericKey
    E:GenericKey
    F:GenericKey
    R:GenericKey
    V:GenericKey
    Escape:GenericKey
    UpArrow:GenericKey
    DownArrow:GenericKey
    LeftArrow:GenericKey
    RightArrow:GenericKey
    WheelUp:GenericKey
    WheelDown: GenericKey
    Ctrl: GenericKeyCode
    # endregion


    def __init__(self, CtrlD:GenericKeyButtonName=None, CtrlA:GenericKeyButtonName=None, CtrlW:GenericKeyButtonName=None,CtrlS:GenericKeyButtonName=None,
                 Enter: GenericKey=None,Backspace: GenericKey=None,Shift: GenericKey=None,
                    Tab: GenericKey=None,W: GenericKey=None,S: GenericKey=None,A: GenericKey=None,D: GenericKey=None,
                    Q: GenericKey=None,E: GenericKey=None,F: GenericKey=None,R: GenericKey=None,V: GenericKey=None,
                    Escape: GenericKey=None,UpArrow: GenericKey=None,DownArrow: GenericKey=None,
                    LeftArrow: GenericKey=None,RightArrow: GenericKey=None,WheelUp: GenericKey=None,
                    WheelDown: GenericKey=None,Ctrl: GenericKeyCode=None) -> None:
        self.CtrlD = GenericKeyButtonName(**CtrlD)
        self.CtrlA = GenericKeyButtonName(**CtrlA)
        self.CtrlW = GenericKeyButtonName(**CtrlW)
        self.CtrlS = GenericKeyButtonName(**CtrlS)

        self.Enter = GenericKey(**Enter)
        self.Backspace = GenericKey(**Backspace)
        self.Shift = GenericKey(**Shift)
        self.Tab = GenericKey(**Tab)
        self.W = GenericKey(**W)
        self.S = GenericKey(**S)
        self.A = GenericKey(**A)
        self.D = GenericKey(**D)
        self.Q = GenericKey(**Q)
        self.E = GenericKey(**E)
        self.F = GenericKey(**F)
        self.R = GenericKey(**R)
        self.V = GenericKey(**V)
        
        self.Escape = GenericKey(**Escape)
        self.UpArrow = GenericKey(**UpArrow)
        self.DownArrow = GenericKey(**DownArrow)
        self.LeftArrow = GenericKey(**LeftArrow)
        self.RightArrow = GenericKey(**RightArrow)
        self.WheelUp = GenericKey(**WheelUp)
        self.WheelDown = GenericKey(**WheelDown)
        self.Ctrl = GenericKeyCode(**Ctrl)
    # def __init__(self,CtrlD:CtrlD):
    #     self.CtrlD = CtrlD
        
    def Deserialize(jsonString:str):
        
        strNew = jsonString.replace("Ctrl+","Ctrl")
        obj1 = json.loads(strNew)
        obj:GameControls = GameControls(**obj1)
        return obj
    
    def Serialize(self):
        #[a for a in dir(self) if not a.startswith('__') and not callable(getattr(obj, a))]
        #obj = vars(self)
        obj1 = deepcopy(self) ##GameControls(**self)
        obj2 = vars_recursive(obj1)

        #self = GameControls(**obj2)
        jsonString = json.dumps(obj2)
        strNew = jsonString.replace("CtrlD","Ctrl+D")
        strNew = strNew.replace("CtrlW","Ctrl+W")
        strNew = strNew.replace("CtrlS","Ctrl+S")
        strNew = strNew.replace("CtrlA","Ctrl+A")

        print('serialize')
        print(strNew)

        obj = json.loads(strNew)
        
        obj3 = delete_prop_recursive(obj,"XBoxButton")
        
        self = GameControls(**obj2)
        strFinal = json.dumps(obj3)
        return strFinal
    
def delete_prop_recursive(obj, keyToRemove = ''):
    if (not isinstance(obj, str) and not isinstance(obj, int) and not isinstance(obj, float) and not isinstance(obj, list)):

        for item in obj:
            if item == keyToRemove and keyToRemove != '':
                del obj[keyToRemove] ## We don't want this property to be included in the json string
                return obj
            elif obj[item] != None:
                temp = obj[item]
                try:
                    if not (isinstance(temp, str) and not isinstance(temp, int) and not isinstance(temp, float) and not isinstance(temp, list)):
                        delete_prop_recursive(obj[item], keyToRemove)
                except Exception as e:
                    print(obj[item])
                    pass
    return obj

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