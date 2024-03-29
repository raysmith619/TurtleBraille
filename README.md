# TurtleBraille
We are migrating from generating braille via direct imitating turtle commands (resource_lib/src/*braille*/) to Canvas "Scraping". The older method intercepts each Turtle command and builds a set of points which are used to create the list of braille cells.  The target method directs most graphic calls directly to their turtle counter parts creating the associated tkinter canvas items with no additional processing. After all graphic calls are processed, the candidate Braille cell regions of the canvas are checked for object overlap. Regions that have overlapping items are used to generate visible Braille cells.  
Our rationalle is to avoid an intimite understanding of each Turtle command and its translation into tkinter commands.  The Canvas "Scrapping" method may also facilitate post processing magnification or other scale changes.
# NOTE - in construction
Not functional yet - scaling problems
## Example
## Simple Turtle Display with braille display overlay - erroneous Braille view
The Braille view, overlayed, is scaled incorrectly, especially the vertical view is flipped.
![Incorrect Display](Docs/TurtleBraille_combo_err.PNG)
## Simple working braille display
The Braille view, only braille, from working resource_lib code, correctly displayed.
![Incorrect Display](Docs/TurtleBraille_braille_win_good.PNG)

## Problem
Somewhere in the new code we are scaling incorrectly.  Just to get the display to position for viewing I had to hack the Turtle goto function as shown in the code snippet below.  If I could think of a way to make the code smaller I would send it to something like ***stackoverflow*** and pose the question.
### Code Snippet
```
        
class BrailleDisplay:
    """ Create and display graphics using Braille
    """
    def __init__(self, title="Braille Display",
                 canvas=None,
                 win_width=800, win_height=800,
                 point_resolution=None):
        """ Setup display
...     """
        screen = tu.TurtleScreen(canvas)
        self.rtu = tu.RawTurtle(canvas)          # For turtle screen
...
    
    def goto(self, x, y=None):
        x += self.x_max/2 + 10*(self.cell_xs[1]-self.cell_xs[0])  # HACK to position viewing
        y -= (self.y_max/2 + 4*(self.cell_ys[1]-self.cell_ys[0])) # HACK to position viewing
        self.rtu.goto(x,y)
```
### Attempted Solutions
#### Changing turtle coordinates to restrict to nonegative values
##### Results
Less negative tkinter canvas coordinates but not much success over all.
#### Avoiding direct call to goto
##### Code changeing goto call:
```
    def goto(self, x, y=None):
        """ mimic turtle rtu without explicit goto call
        because explicit goto appears to mess up tkinter
        coordinates
        """
        self.goto_pre(x,y)
        old_heading = self.rtu.heading()
        cur_x, cur_y = self.rtu.position()
        angle = self.rtu.towards(x=x, y=y)
        distance = self.rtu.distance(x=x, y=y)
        new_heading = old_heading+angle
        self.setheading(new_heading)
        self.rtu.forward(distance)
        self.rtu.setheading(old_heading)
        
        self.goto_post(x,y) 
```
##### Results
Main display works but no change

#### Implementing goto with direct tkinter calls
##### goto routine
```    
    def goto(self, x, y=None):
        """ mimic turtle rtu without explicit goto call
        because explicit goto appears to mess up tkinter
        coordinates by direct canvas.create_line() calls
        """
        self.goto_pre(x,y)
        color = self.rtu.pencolor()
        width = self.rtu.pensize()
        isdown = self.rtu.isdown()
        cur_x, cur_y = self.rtu.position()
        
        if isdown:
            canvas = self.rt_canvas
            win_cur_x, win_cur_y = self.cvt_tur_pt_to_win((cur_x,cur_y))
            win_x,win_y = self.cvt_tur_pt_to_win((x,y))
            canvas.create_line(win_cur_x, win_cur_y, win_x, win_y,
                               fill=color, width=width)
        if isdown:
            self.rtu.penup()
        self.rtu.setposition(x,y)
        if isdown:
            self.rtu.pendown()
        self.mw.update()
        
        self.goto_post(x,y) 
```
##### Results
###### Simple display of results
####### 4 Square display including Braille Overlay wich down to right
![](Docs/four_square_with_braille_overlay_offset.PNG)

Some of the numbers displayed in black are annotations of interesting features.
The code creating the annotations within the squares is, with description added to right:
```
    bw.write(f"[ix:{ix}, iy:{iy}]", align="center", font=font)      ### Braille cell indexes
    mx, my = new_line(mx,my, ch_h = csize+2)
    bw.write(f"tu:({tu_x1}, {tu_y1}   {tu_x2}, {tu_y2})", align="center", font=font)   ### cell turtle coordinates
    mx, my = new_line(mx,my, ch_h = csize+2)
    bw.write(f"in tu:({x1}, {y1}   {x2}, {y2})", align="center", font=font)         ### inset to keep items inside
    mx, my = new_line(mx,my, ch_h = csize+2)
    bw.write(f"win:({w_x1}, {w_y1}   {w_x2}, {w_y2})", align="center", font=font)   ### Window(canvas) coords of squares
    mx, my = new_line(mx,my, ch_h = csize+2)
    overlapping = bw.find_overlapping(None, w_x1,w_y1,w_x2,w_y2, 
                                      include_annotations=True)
    bw.write(f"overlap:({overlapping})", align="center", font=font)                 ### overlapping items
            
    bw.goto(mx,my)

```
Some other marks outside the squares are displays of Braille Cell index, and the canvas id found via findoverlapping call - e.g. for the lower left green square, indexes: 1,1, canvas id: 40.

####### 4 Square display including Braille Overlay
![](Docs/four_square_with_braille_window.PNG)

###### Summary
Some improvements but we can't get past some subtle turtle / tkinter interaction

#### Supporting Software
##### CanvasView (resource_lib/src/canvas_view.py)
CanvasView, based on tkinter.Canvas, aids the access and viewing of canvas items. CanvasView.show_item enables the listing of canvas items added since the previous show_item call.  Except for 'fill' and 'width', only options changed from the previous canvas item type are displayed.  Optionally, conversions between turtle and window(canvas) coordinate values are shown.
###### Sample log output Showing Canvas change between turtle.goto calls
```
 goto(-190, 190) prev id: 5
    post_id:5
 ==> 1: None []
 ==> 2: image [0.0, 0.0]
     win: x1:0.0, y1:0.0 x2:, y2:
 
 ...removed to facilite viewing
 goto(-77, 190) prev id: 6
 cvt_tur_x_to_win(-190) => 10
 cvt_tur_y_to_win(190) => 10
 cvt_tur_pt_to_win((-190, 190)) => (10, 10)
 cvt_tur_x_to_win(-77) => 123
 cvt_tur_y_to_win(190) => 10
 cvt_tur_pt_to_win((-77, 190)) => (123, 10)
    post_id:7
 ==> 1: None []
 ==> 2: image [0.0, 0.0]
     win: x1:0.0, y1:0.0 x2:, y2:
 ...removed to facilite viewing
 ==> 7: line [10.0, 10.0, 123.0, 10.0]
     win: x1:10.0, y1:10.0 x2:123.0, y2:10.0
     capstyle ('capstyle', '', '', 'butt', 'butt')
     fill ('fill', '', '', 'black', 'red')
     width ('width', '', '', '1.0', '1.0')

```

