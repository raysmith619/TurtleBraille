#turtle_screen_scaled.py    22Jun2022  crs
"""
Simple scaled turtle in an attempt to give non-negative canvas coordinates 
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
main_mw.geometry(f"{win_height}x{win_width}")
drag_pen = True
canvas = CanvasView(main_mw, width=win_width, height=win_height,
                    drag_pen=drag_pen)
canvas.pack(expand=1, fill='both')

list_marks = True

        
dsz = 30
line_width = 10
offset = dsz      # offset from edge

SlTrace.lg()

ts = tu.TurtleScreen(canvas)
rtu = tu.RawTurtle(canvas)
x_min = y_min = 0
x_max = y_max = 800
ts.setworldcoordinates(llx=x_min, lly=y_min,
                            urx=x_max, ury=y_max)

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

    

SlTrace.lg(f"turtle_mark_it: x_min:{x_min} x_max:{x_max}"
           f"  y_min:{y_min} y_max:{y_max}")
rtu.penup()
rtu.goto(0,0)
rtu.width(line_width)
x_mid = (x_min+x_max)/2
y_mid = (y_min+y_max)/2

tu_mark_it(x=x_min+offset, y=y_max-offset, color="red")
tu_mark_it(x=x_max-offset, y=y_max-offset, color="orange")
tu_mark_it(x=x_min+offset, y=y_max-offset, color="yellow")
tu_mark_it(x=x_max-offset, y=y_max-offset, color="green")


tk.mainloop()