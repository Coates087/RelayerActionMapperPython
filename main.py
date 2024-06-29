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
import sys
#from updateControls import LoadpdateControlsForm
#import updateControls.LoadpdateControlsForm

#import updateControls
import resource_files.xbox_buttons as xBtn
import resource_files.general_icons as gIcons
import resource_files.default_controls as defaultConfigs


const = constantsPython.strResourcePath()

import mainWindow


# print("\nName of Python script:", sys.argv)

mainWindow.StartMain()



