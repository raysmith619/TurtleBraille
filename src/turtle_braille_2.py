#turtle_braille_2.py 01Jun2022  crs  scan tk canvas items
#                    16Apr2022  crs  Author
"""
Turtle augmented with braille graphics output
turtle commands create Turtle output plus approximate braille
output
Operation:
Act as derived from turtle
Pass display commands directly to turtle
except:
    done, mainloop which generate braille before going to turtle

"""
import tkinter as tk
import turtle as tu

from select_trace import SlTrace
SlTrace.clearFlags()
from braille_display_2 import BrailleDisplay
    
class TurtleBraille(tu.RawTurtle):
    """ Parallel braille graphics output which attemps to aid
    blind people "see" simple graphics turtle output
    """
    def __init__(self, title=None,
                 canvas=None,
                 win_width=800, win_height=800,
                 cell_width=40, cell_height=25,
                 braille_window=True,
                 braille_print=True,
                 points_window=False,
                 print_cells=False,
                 tk_items=False
                 ):
        """ Setup display
        :title: title for display(s)
                If title is present and ends with "-"
                descriptive suffixes are generated for the
                different output
                default: Descriptive title(s) are generated
        :canvas: tk.Canvas basis
                default: generate tk.
        :win_width: display window width in pixels
                    default: 800
        :win_height: display window height in pixels
                    default: 800
        :cell_width: braille width in cells
                    default: 40
        :cell_height: braille width in cells
                    default: 25
        :braille_window: display a braille window
                    default: True
        :braille_print: print display braille to output
                    default: True
        :points_window: display window showing where
                        display points were found/calculated
                    default: False
        :print_cells: print cells in formatted way
                    default: False - no print
        :tk_items: print tkinter canvas items
        """
        
        if canvas is None:
            mw = tk.Tk()
            canvas = tk.Canvas(mw)
        self.tk_canvas = canvas
        super().__init__(canvas)
        self.title = title
        self.win_width = win_width
        self.win_height = win_height
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.braille_window = braille_window
        self.braille_print = braille_print
        self.points_window = points_window
        self.print_cells = print_cells
        self.tk_items = tk_items
        bd = BrailleDisplay(win_width=self.win_width,
                            win_height=self.win_height,
                            grid_width=self.cell_width,
                            grid_height=self.cell_height)
        self.bd = bd 


    def braille_draw(self, title=None):
        """ Draw steps in braille
            1. create screen with drawing
            2. create braille output
        """
        self.bd.display()
        

        
    def mainloop(self):
        title = self.title
        if title is None:
            title = "Braille Display -"
        self.bd.display(title=title,
                   braille_window=self.braille_window,
                   points_window=self.points_window,
                   braille_print=self.braille_print,
                   print_cells=self.print_cells,
                   tk_items=self.tk_items)
        self.bd.mainloop()        
    def done(self):
        return self.mainloop()

    # Tracking / special augmentations
    def goto(self, x, y=None):
        """ Implement tracking
        """
        self.bd.goto_pre(x,y)
        super().goto(x,y)
        self.bd.goto_post(x,y)


"""
External functions 
Some day may model after turtle's _make_global_funcs
"""
tum = TurtleBraille()


def backward(length):
    return tum.backward(length)

def color(*args):
    return tum.color(*args)

def dot(size=None, *color):
    return tum.dot(size, *color)

def filling():
    return tum.filling()

def begin_fill():
    return tum.begin_fill()

def end_fill():
    return tum.end_fill()

def forward(length):
    return tum.forward(length)

def goto(x, y=None):
    return tum.goto(x, y=y)
def setpos(x, y=None):
    return tum.setpos(x, y=y) 
def setposition(x, y=None):
    return tum.setposition(x, y=y) 

def left(angle):
    return tum.left(angle)

def pendown():
    return tum.pendown()

def penup():
    return tum.penup()

def right(angle):
    return tum.right(angle)

def speed(speed):
    return tum.speed(speed)

def mainloop():
    return tum.mainloop()
def done():
    return tum.done()

def pensize(width=None):
    return tum.pensize(width)
def width(width=None):
    return tum.pensize(width)

if __name__ == '__main__':
    #from turtle_braille import *    # Get graphics stuff
    #tum.points_window = True
    #tum.print_cells = True
    tum.tk_items = True
    width(40)
    color("green")
    pendown()
    forward(200)
    right(90)
    forward(200)
    right(90)
    forward(200)
    right(90)
    forward(200)
    penup()
    done()    
            
