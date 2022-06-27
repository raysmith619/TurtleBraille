#turtle_screen_simple.py    17Jun2022  crs
"""
Investigate scaling RawTurtle,TurtleScreen and tkinter canvas
We're having problems with BrailleDisplay and braille window being
scaled offset and  y coordinate reversed 
"""
import tkinter as tk
import turtle as tu

from select_trace import SlTrace
from canvas_view import CanvasView

SlTrace.clearFlags()

win_height = 800
win_width = 800

    
main_mw = tk.Tk()
main_mw.title("Simple turtle / canvas test")
main_mw.geometry(f"{int(win_height*1.5)}x{int(win_width*1.5)}")
drag_pen = True
canvas = CanvasView(main_mw, width=win_width, height=win_height,
                    drag_pen=drag_pen)
canvas.pack(expand=1, fill='both')
set_world_coordinates = True
#set_world_coordinates = False
SlTrace.lg(f"set_world_coordinates: {set_world_coordinates}")
canvas_mark_it = False
#canvas_mark_it = True 
turtle_mark_it = False 
turtle_mark_it = True
SlTrace.lg(f"canvas_mark_it:{canvas_mark_it} turtle_mark_it:{turtle_mark_it}")
tu_zero_to_max = True   # turtle 0-max

list_marks = True

        
dsz = 30
line_width = 10
offset = 40      # offset from edge
SlTrace.lg()

ts = tu.TurtleScreen(canvas)
rtu = tu.RawTurtle(canvas)
if set_world_coordinates:
    SlTrace.lg(f"ts.setworldcoordinates("
               f"llx=0, lly=win_height({win_height}),"
               f"urx=win_width({win_width}), ury=0)")
    ts.setworldcoordinates(llx=0, lly=win_height,
                            urx=win_width, ury=0)

rtu.speed('fastest')
rtu.width(line_width)

def show_new_items(prefix=None):
    new_items = canvas.get_new_items()
    for item in new_items:
        canvas.show_canvas_item(item, prefix=prefix)

tu_mark_it_no = 0      # Track markings
def tu_mark_it(x, y, color=None, width=None):
    global tu_mark_it_no
    
    if width is None:
        width = line_width
    tu_mark_it_no += 1
    if drag_pen:
        rtu.width(width)
        rtu.pendown()
    else:
        rtu.penup()
    rtu.color(color)
    rtu.goto(x,y)
    if (list_marks):
        ts.update()
        SlTrace.lg(f"\ntu_mark_it {tu_mark_it_no}:"
                       f" x={x} y={y} {color}")
        show_new_items()
    rtu.pendown()
    rtu.dot(dsz, color)
    if (list_marks):
        ts.update()
        SlTrace.lg(f"\ntu_mark_it {tu_mark_it_no}:"
                       f" x={x} y={y} {color} DOT")
        show_new_items()
        canvas.mark_it_x = x        # sharing marker info
        canvas.mark_it_y = y

    
if turtle_mark_it:
    if tu_zero_to_max:
        x_min = 0
        x_max = win_width
        y_min = 0
        y_max = win_height
    else:
        x_min = -win_width/2
        x_max = win_width/2
        y_min = -win_height/2
        y_max = win_height/2

    SlTrace.lg(f"turtle_mark_it: x_min:{x_min} x_max:{x_max}"
               f"  y_min:{y_min} y_max:{y_max}")
    rtu.penup()
    rtu.goto(0,0)
    line_width = 20
    rtu.width(line_width)
    x_mid = (x_min+x_max)/2
    y_mid = (y_min+y_max)/2
    x1 = x_mid
    y1 = y_mid
    x2 = x1 + x_mid/2
    y2 = y1 - y_mid/2
    tu_mark_it(x=x1, y=y1, color="red")
    tu_mark_it(x=x2, y=y2, color="orange")
    tu_mark_it(x=x_min+offset, y=y_min+offset, color="yellow")
    tu_mark_it(x=x_max-offset, y=y_max-offset, color="green")

if canvas_mark_it:
    x_min = 0
    x_max = win_width
    y_min = 0
    y_max = win_height
    line_width = 10
    rtu.width(line_width)
    canvas.goto(0,0)
    SlTrace.lg(f"x_min:{x_min} x_max:{x_max}"
               f"  y_min:{y_min} y_max:{y_max}")
    canvas.mark_it(x=x_min+offset, y=y_max-offset, color="red")
    canvas.mark_it(x=x_max-offset, y=y_min+offset, color="orange")
    canvas.mark_it(x=x_min+offset, y=y_min+offset, color="yellow")
    canvas.mark_it(x=x_max-offset, y=y_max-offset, color="green")


tk.mainloop()