#braille_display_test2.py
import tkinter as tk

from select_trace import SlTrace
from braille_display_2 import BrailleDisplay

SlTrace.lg("BrailleDisplay Test braille_display_test2")
SlTrace.clearFlags()
#SlTrace.lg("\nAfter clearFlags")
#SlTrace.listTraceFlagValues()
SlTrace.setFlags("point,show_id")
from canvas_view import CanvasView

win_height = 400
win_width = 400
x_min = -win_width//2       # Force int
y_min = -win_height//2
x_max = win_width//2
y_max = win_height//2

'''
x_min = 0
y_min = 0
x_max = win_width
y_max = win_height
x_min = -1.0
y_min = -1.0
x_max = 1.0
y_max = 1.0
 
x_min = float(-win_width//2)       # Force float
y_min = float(-win_height//2)
x_max = float(win_width//2)
y_max = float(win_height//2)
'''
SlTrace.lg(f"x_min:{x_min} y_min:{y_min} x_max:{x_max} y_max:{y_max}")
grid_width = 3
grid_height = 2
display_all = False          # Display all things - True overrides other settings
braille_window = True       # Create braille window
#braille_window = False      # * Suppress braille window
points_window = True        # Create window showing points
points_window = False       # * Suppress braille window showing points
braille_print = True        # Print braille for figure 
print_braille_cells = False # Print braille cells
tk_items = False            # Display tkinter objs
do_snapshots = True         # Do setup and do shapshot
do_simple_test = False      # Do simple test
do_long_test = True         # do long tests
snapshot_clear = True       # Clear screen after snapshot
overlay_braille = True      # Overlay Braille on primary display
#overlay_braille = False     # Don't overlay Braille on primary
color_index = -1
colors = ["red", "orange", "yellow", "green", "blue",
          "indigo", "violet"]
def new_color():
    """ Cycle through simple list of colors
    :returns: next color string
    """
    global color_index
    
    color_index += 1
    return colors[color_index%len(colors)]

def reset_color(index=-1):
    """ reset cycle through colors
    :index: initial index default: -1
    """
    color_index = index
    
def btn_check(x,y):
    print("btn_check")
    SlTrace(f"btn_check(x={x}, y={y}")
    
    
"""
simple_test - do simple test(s)
NOFILL - suppress fill test versions, else do fill after
 non-fill
"""

tests = (
    "simple_test,"
    "goto, dots,"
    "horz_line, vert_line, diag_line,"
    "triangle, a_dot, square, diamond"
    )

tk_items = True
#tests = "snapshots diagz_line" 
#tests = "snapshots square"
#tests = "snapshots goto"

#display_all = True
#tests = ("vert_line, horz_line")
#tests = ("simple_test")
#tests = ("goto")
#tests = "dots"
tests = "grid_text"

if "simple_test" in tests:
    do_simple_test = True 
if "no_long_test" in tests:
    do_long_test = False 
elif "do_long_test" in tests:
    do_long_test = True 
            
SlTrace.lg(f"\ntests: {tests}")
main_mw = tk.Tk()
main_mw.title("BrailleDisplay Tests")
main_mw.geometry(f"{win_width}x{win_height}")
main_canvas = CanvasView(main_mw, width=win_width, height=win_height)
main_canvas.pack(expand=1, fill='both')

if do_simple_test:
    bw = BrailleDisplay(title="braille_display test",
                mw=main_mw,
                win_width=win_width, win_height=win_height,
                grid_width=grid_width, grid_height=grid_height,
                canvas=main_canvas)

    bw.pensize(20)
    bw.color("green")
    bw.forward(200)
    bw.right(90)
    bw.forward(200)
    bw.right(90)
    bw.forward(200)
    bw.right(90)
    bw.forward(200)

    bw.display(braille_window=braille_window, braille_print=braille_print,
               print_cells=print_braille_cells,
               points_window=points_window,
               tk_items=tk_items,
               overlay_braille=overlay_braille)


bwsn = None                 # Snapshot BrailleDisplay
bwsn_title = None
def setup_snapshot(title=None, keep_bw=False):
    global bw
    global bwsn
    global bwsn_title
    if not keep_bw or bwsn is None:
        
        bwsn = BrailleDisplay(title=title, mw=main_mw,
                canvas=main_canvas,
                win_width=win_width, win_height=win_width,
                x_min=x_min, y_min=y_min, x_max=x_max, y_max=y_max,
                grid_width=grid_width, grid_height=grid_height)
        bw = bwsn
        #bw.reset()      # Note only one screen
        reset_color()
        bw.speed("fastest")

    bwsn_title = title + " -"
    
def do_snapshot():
    """ Take snapshot now
    """
    bw.display(title=bwsn_title,
               braille_window=braille_window,
               points_window=points_window,
               braille_print=braille_print,
               print_cells=print_braille_cells,
               tk_items=tk_items,
               overlay_braille=overlay_braille,
               all=display_all)
        
        
        
if SlTrace.trace("cell"):
    SlTrace.lg("cell limits")
    for ix in range(len(bw.cell_xs)):
        SlTrace.lg(f"ix: {ix} {bw.cell_xs[ix]:5}")
    for iy in range(len(bw.cell_ys)):
        SlTrace.lg(f"iy: {iy} {bw.cell_ys[iy]:5}")
    
sz = 400
color = "purple"
wd = 2

def add_square(fill_color=None):
    """ Simple colored square
    :fill_color: fill color
                default: don't fill
    """
    bw.penup()
    bw.goto(-sz,sz)
    bw.pendown()
    if fill_color is not None:
        bw.begin_fill()
        bw.fillcolor(fill_color)
    side = 2*sz
    bw.setheading(0)
    bw.color("red")
    bw.forward(side)
    bw.color("orange")
    bw.right(90)
    bw.forward(side)
    bw.color("yellow")
    bw.right(90)
    bw.forward(side)
    bw.color("green")
    bw.right(90)
    bw.forward(side)
    if fill_color is not None:
        bw.fillcolor(fill_color)
        bw.end_fill()

do_snapshots = not "no_snapshots" in tests

"""
        TESTS TESTS TESTS TESTS TESTS TESTS TESTS TESTS TESTS TESTS
        Chosen by string(s) in tests variable
        "no_long_test" - force no long tests default: do long tests
        "no_snapshots" - suppress snapshots  default: do snapshots for long tests
        
""" 
SlTrace.lg(f"\ntests: {tests}")

        

if "diagz_line" in tests:
    # Simple right to up diagonal from initial point(0,0)
    if do_snapshots:
        setup_snapshot("a_diagz_line")
    bw.color("green")
    bw.pendown()
    bw.goto(sz,sz)
    if do_snapshots:
        do_snapshot()

if "dots" in tests:
    """
    r         b


         g


    y         o
    """
    dsz = 30
    offset = 40      # offset from edge
    if do_snapshots:
        setup_snapshot("goto")
    bw.width(10)

    bw.penup()
    bw.goto(bw.x_min+offset, bw.y_max-offset)
    bw.pendown()
    bw.color("red")
    bw.dot(dsz)

    bw.penup()
    bw.goto(bw.x_max-offset, bw.y_min+offset)
    bw.pendown()
    bw.color("orange")
    bw.dot(dsz)

    bw.penup()
    bw.goto(bw.x_min+offset,bw.y_min+offset)
    bw.pendown()
    bw.color("yellow")
    bw.dot(dsz)

    bw.penup()
    bw.goto((bw.x_min+bw.x_max)/2, (bw.y_min+bw.y_max)/2)
    bw.pendown()
    bw.color("green")
    bw.dot(dsz)

    bw.penup()
    bw.goto(bw.x_max-offset, bw.y_max-offset)
    bw.pendown()
    bw.color("blue")
    bw.dot(dsz)
    if do_snapshots:
        do_snapshot()

def new_line(tu_x, tu_y, ch_h=12):
    """ Move to text new line, repositioning turtle
        also returning new x,y
    :tu_x: x position
    :tu_y: y position
    :ch_h: character height including line spacing default: 2
    :returns: (tu_x_new, tu_y_new)
    """
    bw.penup()
    tu_x_new = tu_x
    tu_y_new = tu_y - ch_h
    bw.goto(tu_x_new, tu_y_new)
    return (tu_x_new, tu_y_new)
    
def grid_text(ix, iy, inset = 0, do_fill = True):
    """ Create a grid box
    :ix: grid x index
    :iy: grid y index
    :inset: inset from full grid size
    :do_fill: fill rectangle
            default: True fill rectangle
    """
    tu_x1,tu_y1,tu_x2,tu_y2 = bw.get_cell_ullr_tur(ix, iy)
    w_x1,w_y1,w_x2,w_y2 = bw.get_cell_ullr_win(ix, iy)
    bw.penup()
    x1 = tu_x1 + inset 
    y1 = tu_y1 - inset 
    x2 = tu_x2 - inset 
    y2 = tu_y2 + inset
    bw.goto(x1,y1)      # upper left
    bw.pendown()
    if do_fill:
        bw.begin_fill()
    color = new_color()
    bw.color(color)
    bw.goto(x2,y1)      # upper right
    bw.goto(x2,y2)      # lower right
    bw.goto(x1,y2)      # lower left
    bw.goto(x1,y1)      # upper left
    bw.update()
    if do_fill:
        bw.end_fill()
    bw.update()
    overlapping = bw.find_overlapping(None, w_x1,w_y1,w_x2,w_y2)
    mx = abs(x1+x2)/2
    my = abs(y1+y2)/2
    bw.penup()
    mx = (x1+x2)/2
    cht = (abs(y2-y1)/2)
    my = y1-cht
    bw.goto(mx,my)
    bw.pendown()
    csize = 11
    font=("arial",csize,"normal")
    bw.color("black")
    bw.write(f"[ix:{ix}, iy:{iy}]", align="center", font=font)
    mx, my = new_line(mx,my, ch_h = csize+2)
    bw.write(f"tu:({tu_x1}, {tu_y1}   {tu_x2}, {tu_y2})", align="center", font=font)
    mx, my = new_line(mx,my, ch_h = csize+2)
    bw.write(f"in tu:({x1}, {y1}   {x2}, {y2})", align="center", font=font)
    mx, my = new_line(mx,my, ch_h = csize+2)
    bw.write(f"win:({w_x1}, {w_y1}   {w_x2}, {w_y2})", align="center", font=font)
    mx, my = new_line(mx,my, ch_h = csize+2)
    overlapping = bw.find_overlapping(None, w_x1,w_y1,w_x2,w_y2,
                                      include_annotations=True)
    bw.write(f"overlap:({overlapping})", align="center", font=font)
            
    bw.goto(mx,my)
    
    
    

if "grid_text" in tests:
    """
    0,0    1,0    2,0    3,0
    
    0,1    1,1    2,1    3,1
    
    0,2    1,2    2,2    3,2
    
    0,3    1,3    2,3    3,3
    ...
    """
    do_fill = True
    #do_fill = False
    if do_snapshots:
        setup_snapshot("grid_test")
    grid_x_mult = 1 # add iff ix%grid_x_mult == 0 
    grid_y_mult = 1 # add iff iy%grid_y_mult == 0
    inset = 10       # inset from rectangle
        
    for ix in range(bw.grid_width):
        for iy in range(bw.grid_height):
            if (ix % grid_x_mult == 0
                    and iy % grid_y_mult == 0):
                grid_text(ix, iy, inset=inset, do_fill=do_fill)
    if do_snapshots:
        do_snapshot()
    bw.onclick(btn_check)
    bw.mainloop()
    
    
if "goto" in tests:
    """
    y
    yr
    y r
    y  r
    y   r
    y    r
    ooooooo
    """
    if do_snapshots:
        setup_snapshot("goto")
    x_min = bw.x_min
    x_max = bw.x_max
    y_min = bw.y_min
    y_max = bw.y_max
    offset = 100      # offset from edge
    if do_snapshots:
        setup_snapshot("goto")
    bw.speed("fastest")
    bw.width(10)
    bw.penup()
    bw.goto(x_min+offset, y_max-offset)
    bw.pendown()
    bw.color("red")
    bw.goto(x_max-offset, y_min+offset)
    bw.color("orange")
    bw.goto(x_min+offset,y_min+offset)
    bw.color("yellow")
    bw.goto(x_min+offset, y_max-offset)
    if do_snapshots:
        do_snapshot()


if "horz_line" in tests:
    if do_snapshots:
        setup_snapshot("a_horz_line")
    bw.speed("fastest")
    bw.width(10)
    left = 200
    top = 100
    left = top = 0
    bw.penup()
    bw.color("red")
    bw.goto(left,top)
    bw.color("orange")
    bw.goto(sz/2,top)
    bw.color("green")
    bw.pendown()
    bw.goto(sz,top)
    bw.color("blue")
    bw.goto(2*sz,top)
    bw.color("indigo")
    bw.goto(3*sz,top)
    if do_snapshots:
        do_snapshot()
if "vert_line" in tests:
    if do_snapshots:
        setup_snapshot("a_vert_line")
    bw.pendown()
    bw.right(90)
    bw.color("red")
    bw.forward(sz/2)
    bw.color("blue")
    bw.forward(sz/2)
    if do_snapshots:
        do_snapshot()
if "diag_line" in tests:
    if do_snapshots:
        setup_snapshot("a_diag_line")
    bw.penup()
    bw.goto(-sz,sz)
    bw.color("green")
    bw.pendown()
    bw.goto(sz,-sz)
    if do_snapshots:
        do_snapshot()
if "triangle" in tests:
    for ft in ["","fill"]:
        if ft == "fill" and "NOFILL" in tests:
            continue # skip fill version
        
        if do_snapshots:
            setup_snapshot("triangle" " " + ft)
            bw.begin_fill()
        bw.penup()
        bw.goto(0,sz)
        bw.pendown()
        bw.pensize(wd)
        bw.color("red")
        bw.goto(sz,-sz)
        bw.color("green")
        bw.goto(-sz,-sz)
        bw.color("blue")
        bw.goto(0,sz)
        if ft == "fill":
            bw.fillcolor("dark gray")
            bw.end_fill()
        if do_snapshots:
            do_snapshot()
if "a_dot" in tests:
    if do_snapshots:
        setup_snapshot("a_dot")
    bw.dot(sz, color)
    if do_snapshots:
        do_snapshot()
    
if "square" in tests:
    for ft in ["","fill"]:
        if ft == "fill" and "NOFILL" in tests:
            continue # skip fill version

        if do_snapshots:
            setup_snapshot("square" " " + ft)
        if ft == "fill":
            add_square("violet")
        else:
            add_square()
        if do_snapshots:
            do_snapshot()

if "diamond" in tests:
    for ft in ["","fill"]:
        if ft == "fill" and "NOFILL" in tests:
            continue # skip fill version

        if do_snapshots:
            setup_snapshot("diamond in square" " " + ft)
        dsz = .7 * sz
        bw.pensize(25)
        if ft == "fill":
            add_square("violet")
        else:
            add_square()
        bw.penup()
        bw.goto(0,dsz)
        if ft == "fill":
            bw.begin_fill()
        bw.pendown()
        bw.color("red")
        bw.goto(dsz,0)
        bw.color("orange")
        bw.goto(0,-dsz)
        bw.color("yellow")
        bw.goto(-dsz,0)
        bw.color("green")
        bw.goto(0,dsz)
        if ft == "fill":
            bw.fillcolor("indigo")
            bw.end_fill()
        if do_snapshots:
            do_snapshot()
bw.mainloop()      
