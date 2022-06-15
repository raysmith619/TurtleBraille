# TurtleBraille
Migrating from resource_lib/turtle_braille/ to Canvas "Scraping" to generate Braille from intercepting each Turtle command and building as set of points to convert.  The rationalle is to avoid an intimite understanding of each Turtle command and its translation into tkinter commands.
# NOTE - in construction
Not functional yet - scalling problems
## Example
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


![Incorrect Display](Docs/TurtleBraille_combo_err.PNG)
