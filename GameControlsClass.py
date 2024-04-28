import json
from typing import Any
from dataclasses import dataclass


class KeyboardClass:
    def __init__(self, KeyCode:str, KeyName:str):
        self.KeyCode = KeyCode
        self.KeyName = KeyName


class GenericKeyCodeClass:
    def __init__(self, KeyCode:list[str]):
        self.KeyCode = KeyCode
        

class GenericKeyButtonName2:
    def __init__(self, ButtonName:str, XBoxButton:str = ''):
        self.ButtonName = ButtonName
        self.XBoxButton = XBoxButton

class GenericKey(GenericKeyButtonName2):
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
class GenericKeyButtonName:
    ButtonName: str
    XBoxButton:str
    def __init__(self, ButtonName: str, XBoxButton:str = '') -> None:
        self.ButtonName = ButtonName
        self.XBoxButton = XBoxButton


@dataclass
class GameControls:
    CtrlD:GenericKeyButtonName

    def __init__(self, CtrlD:GenericKeyButtonName) -> None:
        self.CtrlD = GenericKeyButtonName(**CtrlD)
    # def __init__(self,CtrlD:CtrlD):
    #     self.CtrlD = CtrlD
        
    def Deserialize(jsonString:str):
        
        strNew = jsonString.replace("Ctrl+","Ctrl")
        obj1 = json.loads(strNew)
        obj = GameControls(**obj1)
        return obj


@dataclass
class A(GenericKey):
    # KeyCode: list[str]
    # ButtonName: str
    def __init__(self, ButtonName:str, KeyCode:list[str], XBoxButton:str = ''):
        super().__init__(self, ButtonName=ButtonName, KeyCode=KeyCode, XBoxButton=XBoxButton) 
    # @staticmethod
    # def from_dict(obj: Any) -> 'A':
    #     _KeyCode = [tk.from_dict(y) for y in obj.get("KeyCode")]
    #     _ButtonName = str(obj.get("ButtonName"))
    #     return A(_KeyCode, _ButtonName)
    
# @dataclass
# class A2:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'A':
#         _KeyCode = [tk.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return A(_KeyCode, _ButtonName)

# @dataclass
# class Backspace:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'Backspace':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return Backspace(_KeyCode, _ButtonName)

# @dataclass
# class Ctrl:
#     KeyCode: list[str]

#     @staticmethod
#     def from_dict(obj: Any) -> 'Ctrl':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         return Ctrl(_KeyCode)

# @dataclass
# class CtrlA:
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'CtrlA':
#         _ButtonName = str(obj.get("ButtonName"))
#         return CtrlA(_ButtonName)

# @dataclass
# class CtrlD:
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'CtrlD':
#         _ButtonName = str(obj.get("ButtonName"))
#         return CtrlD(_ButtonName)

# @dataclass
# class CtrlS:
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'CtrlS':
#         _ButtonName = str(obj.get("ButtonName"))
#         return CtrlS(_ButtonName)

# @dataclass
# class CtrlW:
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'CtrlW':
#         _ButtonName = str(obj.get("ButtonName"))
#         return CtrlW(_ButtonName)

# @dataclass
# class D:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'D':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return D(_KeyCode, _ButtonName)

# @dataclass
# class DownArrow:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'DownArrow':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return DownArrow(_KeyCode, _ButtonName)

# @dataclass
# class E:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'E':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return E(_KeyCode, _ButtonName)

# @dataclass
# class Enter:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'Enter':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return Enter(_KeyCode, _ButtonName)

# @dataclass
# class Escape:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'Escape':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return Escape(_KeyCode, _ButtonName)

# @dataclass
# class F:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'F':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return F(_KeyCode, _ButtonName)

# @dataclass
# class LeftArrow:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'LeftArrow':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return LeftArrow(_KeyCode, _ButtonName)

# @dataclass
# class Q:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'Q':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return Q(_KeyCode, _ButtonName)

# @dataclass
# class R:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'R':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return R(_KeyCode, _ButtonName)

# @dataclass
# class RightArrow:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'RightArrow':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return RightArrow(_KeyCode, _ButtonName)

# @dataclass
# class S:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'S':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return S(_KeyCode, _ButtonName)

# @dataclass
# class Shift:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'Shift':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return Shift(_KeyCode, _ButtonName)

# @dataclass
# class Tab:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'Tab':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return Tab(_KeyCode, _ButtonName)

# @dataclass
# class UpArrow:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'UpArrow':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return UpArrow(_KeyCode, _ButtonName)

# @dataclass
# class V:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'V':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return V(_KeyCode, _ButtonName)

# @dataclass
# class W:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'W':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return W(_KeyCode, _ButtonName)

# @dataclass
# class WheelDown:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'WheelDown':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return WheelDown(_KeyCode, _ButtonName)

# @dataclass
# class WheelUp:
#     KeyCode: list[str]
#     ButtonName: str

#     @staticmethod
#     def from_dict(obj: Any) -> 'WheelUp':
#         _KeyCode = [.from_dict(y) for y in obj.get("KeyCode")]
#         _ButtonName = str(obj.get("ButtonName"))
#         return WheelUp(_KeyCode, _ButtonName)
    
# @dataclass
# class Root:
#     Enter: Enter
#     Backspace: Backspace
#     Shift: Shift
#     Tab: Tab
#     W: W
#     S: S
#     A: A
#     D: D
#     Q: Q
#     E: E
#     F: F
#     R: R
#     V: V
#     Escape: Escape
#     UpArrow: UpArrow
#     DownArrow: DownArrow
#     LeftArrow: LeftArrow
#     RightArrow: RightArrow
#     WheelUp: WheelUp
#     WheelDown: WheelDown
#     Ctrl: Ctrl
#     CtrlW: CtrlW
#     CtrlS: CtrlS
#     CtrlA: CtrlA
#     CtrlD: CtrlD

#     @staticmethod
#     def from_dict(obj: Any) -> 'Root':
#         _Enter = Enter.from_dict(obj.get("Enter"))
#         _Backspace = Backspace.from_dict(obj.get("Backspace"))
#         _Shift = Shift.from_dict(obj.get("Shift"))
#         _Tab = Tab.from_dict(obj.get("Tab"))
#         _W = W.from_dict(obj.get("W"))
#         _S = S.from_dict(obj.get("S"))
#         _A = A.from_dict(obj.get("A"))
#         _D = D.from_dict(obj.get("D"))
#         _Q = Q.from_dict(obj.get("Q"))
#         _E = E.from_dict(obj.get("E"))
#         _F = F.from_dict(obj.get("F"))
#         _R = R.from_dict(obj.get("R"))
#         _V = V.from_dict(obj.get("V"))
#         _Escape = Escape.from_dict(obj.get("Escape"))
#         _UpArrow = UpArrow.from_dict(obj.get("UpArrow"))
#         _DownArrow = DownArrow.from_dict(obj.get("DownArrow"))
#         _LeftArrow = LeftArrow.from_dict(obj.get("LeftArrow"))
#         _RightArrow = RightArrow.from_dict(obj.get("RightArrow"))
#         _WheelUp = WheelUp.from_dict(obj.get("WheelUp"))
#         _WheelDown = WheelDown.from_dict(obj.get("WheelDown"))
#         _Ctrl = Ctrl.from_dict(obj.get("Ctrl"))
#         _CtrlW = CtrlW.from_dict(obj.get("Ctrl+W"))
#         _CtrlS = CtrlS.from_dict(obj.get("Ctrl+S"))
#         _CtrlA = CtrlA.from_dict(obj.get("Ctrl+A"))
#         _CtrlD = CtrlD.from_dict(obj.get("Ctrl+D"))
#         return Root(_Enter, _Backspace, _Shift, _Tab, _W, _S, _A, _D, _Q, _E, _F, _R, _V, _Escape, _UpArrow, _DownArrow, _LeftArrow, _RightArrow, _WheelUp, _WheelDown, _Ctrl, _Ctrl+W, _Ctrl+S, _Ctrl+A, _Ctrl+D)


