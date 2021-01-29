import operator

import _thread
import tkinter as tk

from Gui import Gui
from Etat import Etat
from PIL import Image
from Utils import solvable, h1, h2, get_shuffled, astar

gui = Gui(master=tk.Tk(), images=[Image.open(f"./res/{num}.png") for num in range(9)])
gui.mainloop()