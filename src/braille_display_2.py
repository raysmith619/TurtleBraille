# braille_display_2.py  03Jun2022  crs  Convert to canvaScreens reading display
#                       19Apr2022  crs  Author
"""
Display graphics on window
Using RawTurtle, TurtleScreen
Doing our own scaling ??
Generate display by reading canvas items
Supports simple graphical point, line specification
Supports display of 6-point cells
on grid_width by grid_height grid
Supports writing out braille stream
"""
from math import sin, cos, pi, atan, sqrt
import turtle as tu
import tkinter as tk

from select_trace import SlTrace
from Lib.pickle import NONE

def pl(point_list):
    """ display routine for point list
    Convert points to integer, or .2f
    :point_list: list of points
    :returns s string of (x,y) ...
    """
    if not isinstance(point_list, list):
        point_list = [point_list]
    st = ""
    for point in point_list:
        st += "("
        for i in range(len(point)):
            p = point[i]
            if i > 0:
                st += ","
            if isinstance(p, float):
                st += f"{int(p)}"
            else:
                st += f"{p}"
        st += ")"
    return st 


class BrailleCell:
    """ braille cell info augmented for analysis
    """
    def __init__(self, dots=None,
                 color=None, color_bg=None,
                 ix=0, iy=0,
                 points=None):
        """ setup braille cell
        :dots: list of set dots default: none - blank
        :color: color str or tuple
        :ix: cell index(from 0) from left side
        :iy: cell index from bottom
        :points: initial set of points, if any
            default: empty
        """
        self.ix = ix    # Include to make self sufficient
        self.iy = iy
        self.dots = dots
        if color is None:
            color = "black"
        if color_bg is None: 
            color_bg = "white"
        self._color = color
        self._color_bg = color_bg
        if points is None:
            points = set()
        self.points = points 
        self._fill_perimiter_points = []
        
    def color_str(self, color=None):
        """ Return color string
        :color: color specification str or tuple
        """
        color_str = color
        if (color_str is None
             or (isinstance(color_str, tuple)
                  and len(color_str) == 0)
             ):
            color_str = self._color
        if isinstance(color_str,tuple):
            if len(color_str) == 1:
                color_str = color_str[0]
            else:
                color_str = "pink"  # TBD - color tuple work
        return color_str
        
        
class BrailleDisplay:
    """ Create and display graphics using Braille
    """
    dots_for_character = {
        " ": (),    # blank
        "a": (1),
        "b": (1,2),
        "c": (1,4),
        "d": (1,4,5),
        "e": (1,5),
        "f": (1,2,5),
        "g": (1,2,4,5),
        "h": (1,2,5),
        "i": (2,4),
        "j": (2,4,5),
        "k": (1,3),
        "l": (1,2,3),
        "m": (1,3,4),
        "n": (1,3,4,5),
        "o": (1,3,5),
        "p": (1,2,3,4),
        "q": (1,2,3,4,5),
        "r": (1,2,3,5),
        "s": (2,3,4),
        "t": (2,3,4,5),
        "u": (1,3,6),
        "v": (1,2,3,6),
        "w": (2,4,5,6),
        "x": (1,3,4,6),
        "y": (1,3,4,5,6),
        "z": (1,3,5,6),
        }
    
    
    def __init__(self, title="Braille Display",
                 canvas=None,
                 win_width=800, win_height=800,
                 grid_width=40, grid_height=25,
                 use_full_cells= True,
                 x_min=None, y_min=None,
                 line_width=1, color="black",
                 color_bg = None,
                 color_fill = None,
                 point_resolution=None):
        """ Setup display
        :title: display screen title
        :canvas: tkinter.Canvas instance
            default: create one
        :win_width: display window width in pixels
            default: 800
        :win_height: display window height in pixels
            default: 800
        :grid_width: braille width in cells
            default: 40
        :grid_height: braille width in cells
            default: 25
        :color: drawing color
                default: turtle default
        :color_fill: fill color
                default: drawing color
        :color_bg: background color
                default: turtle default
        :use_full_cells: Use full cells for point/lines
            e.g. place color letter in cell
            default: True - use full cells
        :x_min: x value for left side default: -win_width/2
        :y_min:  y value for bottom default: -win_height/2
        :line_width: line width
        :point_resolution: Distance between points below
            with, no difference is recognized
            default: computed so as to avoid gaps
                    between connected points
                    conservative to simplify/speed
                    computation
        """
        if title is None:
            title = "Braille Display"
        self.title = title
        self.win_width = win_width
        self.win_height = win_height
        if canvas is None:
            mw = tk.Tk()
            mw.withdraw()
            mw.geometry("800x800")
            canvas = tk.Canvas(mw)
            canvas.pack(expand=1, fill='both')
        screen = tu.TurtleScreen(canvas)
        #screen.screensize(win_width,win_height)
        self.rtu = tu.RawTurtle(canvas)          # For turtle screen
        self.screen = screen
        self.rt_canvas = canvas
        
        self.grid_width = grid_width
        self.cell_width = win_width/self.grid_width
        self.grid_height = grid_height
        self.cell_height = win_height/self.grid_height
        if point_resolution is None:
            point_resolution = int(min(self.cell_width,
                                  self.cell_height)-1)
        if point_resolution < 1:
            point_resolution = 1
        self.point_resolution = point_resolution
        self.use_full_cells = use_full_cells
        if x_min is None:
            x_min = -win_width/2
        self.x_min = x_min
        self.x_max = x_min + win_width
        if y_min is None:
            y_min = -win_height/2
        self.y_min = y_min
        self.y_max = y_min + win_height
        '''
        screen.setworldcoordinates(llx=self.x_min, lly=self.y_min,
                                   urx=self.x_max, ury=self.y_max)
        '''
        self.line_width = line_width
        self._color = color
        if self._color is not None:
            self.rtu.color(self._color)
        self._color_fill = color_fill
        if self._color_fill is not None:
            self.rtu.fillcolor(self._color_fill)
        self._color_bg = color_bg
        if self._color_fill is not None:
            self.rtu.pencolor(self._color_bg)
        self.cmds = []      # Commands to support redo
        self.cells = {}     # BrailleCell hash by (ix,iy)
        self.set_cell_lims()
        self.lfun_horz = False 
        self.lfun_vert = False 
        self.x = self.y = 0
        self.angle = 0          # degrees (angle)
        self.pt = self.p2 = (self.x, self.y)

        self.is_pendown = True 
        self.is_filling = False
        self.tracking_show_item_id = 0
        self.tk_item_samples = {}   # sample canvas items
                                    # for abbreviation
        self.annotate_tag = "ANN"   # Annotation flag for canvas
        
    def set_cell_lims(self):
        """ create cell window(canvas) bottom values through top
         so:
             cell_xs[0] = left edge, cell_xs[grid_width] = right edge
             cell_ys[0] = top edge, cell_ys[grid_height] = bottom edge
        """
         
        self.cell_xs = []
        self.cell_ys = []

        for i in range(self.grid_width):
            w_x = int(i*self.win_width/self.grid_width)
            self.cell_xs.append(w_x)
            SlTrace.lg(f"cell_xs[{i}] = {w_x}")
        self.cell_xs.append(self.win_width) # right edge
        SlTrace.lg(f"cell_xs[{i+1}] = {self.win_width}")
        
        for i in range(self.grid_height):
            w_y = int(i*self.win_height/self.grid_height)
            SlTrace.lg(f"cell_ys[{i}] = {w_y}")
            self.cell_ys.append(w_y)
        self.cell_ys.append(self.win_height)    # bottom edge
        SlTrace.lg(f"cell_ys[{i+1}] = {self.win_height}")
        
    def add_dot(self, size=None, *color):
        """ Add new point
        :size: diameter of dot
        :color: point color
        """
        SlTrace.lg(f"add_dot: ", "braille_cmd")
        self.rtu.dot(size, *color)
        if size is None:
            size = self.line_width
        pt = (self.x,self.y)
        if len(color)==0:
            color = self._color
            
        points = self.get_dot_points(pt=pt, size=size)
        self.populate_cells_from_points(points, color=color)
        
    def set_line_funs(self, p1, p2):
        """ Set line functions which provide determine
        x from y,  y from x to place (x,y) on line
        functions are self.line_x(y) and self.line_y(x)
        :p1: beginnin point (x,y)
        :p2: ending point (x,y)
        """
        x1,y1 = p1
        x2,y2 = p2
        self.lfun_x_diff = x2 - x1
        ###if abs(self.lfun_x_diff) < small:
        ###    self.lfun_x_diff = 0
        self.lfun_y_diff = y2 - y1
        ###if abs(self.lfun_y_diff) < small:
        ###    self.lfun_y_diff = 0
        self.lfun_dist = sqrt(self.lfun_x_diff**2
                              +self.lfun_y_diff**2)
        self.lfun_x_chg_gt = False
        if abs(self.lfun_x_diff) >= abs(self.lfun_y_diff):
            self.lfun_x_chg_gt = True
        if self.lfun_dist != 0: 
            self.lfun_sin = self.lfun_y_diff/self.lfun_dist
            self.lfun_cos = self.lfun_x_diff/self.lfun_dist
        else:
            self.lfun_sin = self.lfun_cos = 0
        
        self.lfun_p1 = p1
        self.lfun_p2 = p2
        self.lfun_horz = False 
        self.lfun_vert = False
        if self.lfun_x_diff == 0:
            self.lfun_vert = True 
        else:
            self.lfun_my = self.lfun_y_diff/self.lfun_x_diff
            self.lfun_cy = y1 - self.lfun_my*x1 
        if self.lfun_y_diff == 0:
            self.lfun_horz = True 
        else:
            self.lfun_mx = self.lfun_x_diff/self.lfun_y_diff 
            self.lfun_cx = x1 - self.lfun_mx*y1
        if self.lfun_x_diff == 0:
            if self.lfun_y_diff >= 0:
                self.lfun_rangle = pi/2
            else:
                self.lfun_rangle = -pi/2
        elif self.lfun_y_diff == 0:
            if self.lfun_x_diff >= 0:
                self.lfun_rangle = 0
            else:
                self.lfun_rangle = pi
        else:
            self.lfun_rangle = atan(self.lfun_my)
        #unit_normal (length 1 orthogonal to line)
        uno_rangle = self.lfun_unorm_rangle = self.lfun_rangle + pi/2
        self.lfun_unorm_sin = sin(uno_rangle)
        self.lfun_unorm_cos = cos(uno_rangle)
        self.lfun_unorm_x = self.lfun_unorm_cos
        self.lfun_unorm_y = self.lfun_unorm_sin
            
    def line_y(self, x):
        """ calculate pt y, given pt x
        having line setup from set_line_funs
        :x: pt x value
        :returns:  y value , None if undetermined
        """
        if self.lfun_horz:
            return self.lfun_p1[1]  # constant y
        
        if self.lfun_vert:
            return self.lfun_p1[1]  # Just pick first 
        
        y = self.lfun_my*x + self.lfun_cy
        return y

    def line_x(self, y):
        """ calculate pt x, given pt y
        having line setup from set_line_funs
        :x: pt x value
        :returns:  x value , None if undetermined
        """
        if self.lfun_horz:
            return self.lfun_p1[0]  # Just pick first 
        
        if self.lfun_vert:
            return self.lfun_p1[0]  # constant x
        
        x = self.lfun_mx*y + self.lfun_cx
        return x
        
        
    def get_line_cells(self, p1, p2, width=None):
        """ Get cells touched by line
        :p1: beginning point (x,y)
        :p2: end point (x,y)
        :width: line thickness in pixels
            default: previous line width
        :returns: list of cells included by line
        """
        SlTrace.lg(f"\nget_line_cells: p1({p1}) p2({p2}", "cell")
        self.set_line_funs(p1=p1, p2=p2)
        x1,y1 = p1
        x2,y2 = p2
        xtrav = x2-x1
        xtrav_abs = abs(xtrav)
        ytrav = y2-y1   # y goes from y1 to y2
        ytrav_abs = abs(ytrav)
        if xtrav_abs > ytrav_abs:
            tstart = x1
            tend = x2
        else:
            tstart = y1
            tend = y2
        tdir = tend - tstart  # just the sign
        trav_step = 1   # cautious
        if tdir < 0:
            trav_step *= -1
        cells = set()
        point_cells = self.get_point_cells(p1)
        cells.update(point_cells)
        tloc = tstart
        pt = p1
        while True:
            pt_x,pt_y = pt
            if tdir > 0:    # going up
                if tloc > tend:
                    break
            else: # going down
                if tloc < tend:
                    break
            if xtrav_abs >  ytrav_abs:
                pt_x += trav_step
                tloc = pt_x
                pt_y = self.line_y(pt_x)
            else:
                pt_y += trav_step
                tloc = pt_y
                pt_x = self.line_x(pt_y)
            pt = (pt_x, pt_y)
            pt_cells = self.get_point_cells(pt)
            cells.update(pt_cells)
        SlTrace.lg(f"line_cells: {cells}\n", "cell")
        return list(cells)
                
        
        
    def get_point_cell(self, pt):
        """ Get cell in which point resides
        If on an edge returns lower cell
        If on a corner returns lowest cell
        :pt: x,y pair location in window coordinates
        :returns: ix,iy cell pair
        """
        x,y = pt
        ix = int((x-self.x_min)/self.win_width*self.grid_width)
        iy = int((y-self.y_min)/self.win_height*self.grid_height)
        return (ix,iy)
        
    def get_point_cells(self, pt, width=None):
        """ Get cells touched by point
        For speed we select all cells within x+/-.5 line width
        and y +/- .5 line width
        For now, ignore possibly interveining cells for
        lines wider than a cell
        :p1: beginning point (x,y)
        :width: line thickness in pixels
            default: previous line width
        :returns: list of cells included by point
        """
        if pt is None:
            pt = self.p2
            
        if width is None:
            width = self.line_width
        
        self.line_width = width
        cell_pt = self.get_point_cell(pt) 
        cells_set = set()     # start with point
        cells_set.add(cell_pt)
        x0,y0 = pt
        for p in [(x0-width,y0+width),   # Add 4 corners
                  (x0+width,y0+width),
                  (x0+width,y0-width),
                  (x0-width,y0)]:
            cell = self.get_point_cell(p)
            SlTrace.lg(f"get_point_cells: p({p}): cell:{cell}", "cell")
            cells_set.add(cell)
        #SlTrace.lg(f"get_point_cells: cells_set:{cells_set}", "cell")
        lst = list(cells_set)
        SlTrace.lg(f"get_point_cells: list:{lst}", "cell")
        return list(cells_set) 

    def update_cell(self, braille_cells=None,
                    ix=None, iy=None, pt=None,
                    color=None, canvas_item=None):
        """ Add / update cell
            if the cell is already present it is updated:
                pt, if present is added
                color is replaced
        cell grid ix,iy:
        :braille_cells: dictionary of braille cells to be augmented
                    default: self.cells
        :ix: cell x grid index 
        :iy: cell y grid index
        OR
        :pt: (x,y) point coordinate of point
            added to cell
        
        :color: cell color
        :returns: new/updated BrailleCell
        """
        if braille_cells is None:
            braille_cells = self.cells
        if color is None:
            color = self._color
        if ix is not None and iy is None:
            raise Exception(f"iy is missing ix={ix}")
        if iy is not None and ix is None:
            raise Exception(f"iy is missing ix={iy}")
        if ix is not None:
            cell_ixiy = (ix,iy)
        else:
            if pt is None:
                raise Exception(f"pt is missing")
            cell_ixiy = self.get_point_cell(pt)
        if cell_ixiy in braille_cells:
            cell = braille_cells[cell_ixiy]
        else:
            cell = BrailleCell(ix=cell_ixiy[0],
                        iy=cell_ixiy[1], color=color)
            braille_cells[cell_ixiy] = cell
        if pt is not None:
            cell.points.add(pt) 
        if color is not None:
            color = color
            cell._color = color
            dots = self.braille_for_color(color)
            cell.dots = dots
        cell.canvas_item = canvas_item      # Remember last canvas item
        return cell
                
    def get_dot_points(self, pt, size=None):
        """ Get fill points included by dot
        :pt: beginning point (x,y)
        :size: dot thickness in pixels
            default: previous line width
        :returns: set of fill ponints
        """
        if size is None:
            size = self.line_width
        if pt is None:
            pt = self.p2
        pt_x,pt_y = pt
        pt_sep = self.point_resolution
        radius = size/2
        npt = int(radius*2*pi/pt_sep)
        point_list = []
        for i in range(npt):
            rangle = i*2*pi/npt
            dx = radius*cos(rangle)
            dy = radius*sin(rangle)
            x = pt_x + dx
            y = pt_y + dy
            point = (int(x),int(y))
            point_list.append(point)
        point_set = self.fill_points(point_list)
        return point_set 

    def fill_cells(self, point_list, point_resolution=None):
        """ Convert set of points to cells
        :points_list:
        :point_resolution: 
            default: self.point_resolution
        :returns: set of cells filling enclosed region
        """
        points = self.fill_points(point_list=point_list,
                                   point_resolution=None)
        cells = self.points_to_cells(points)
        return cells 

    def points_to_cells(self, points):
        """ Convert points to cells
        :points: list, set iterable of points (x,y)
        :returns: set of cells
        """
        cells = set()
        for point in points:
            cell = self.get_point_cell(point)
            cells.add(cell)
        return cells

    """ begin_fill, end_fill support
    """
    def add_to_fill(self, *points):
        """ Add points to fill perimiter
        :points: points to add
        """
        for point in points:
            self._fill_perimiter_points.append(point)
    
            
    def fill_points(self, point_list, point_resolution=None):
        """ Fill surrounding points assuming points are connected
        and enclose an area. - we will, eventualy, do
        "what turtle would do".
        Our initial technique assumes a convex region:
            given every sequential group of points (pn,
            pn+1,pn+2), pn+1 is within the fill region.
        We divide up the fill region into triangles:
            ntriangle = len(point_list)-2
            for i in rage(1,ntriangle):
                fill_triangle(pl[0],pl[i],pl[i+1])
            
        :point_list: list (iterable) of surrounding points
        :point_resolution: distance under which cells containing
                each point will cover region with no gaps
                default: self.point_resolution
        :returns: set of points (ix,iy) whose cells
                cover fill region
        """
        if point_resolution is None:
            point_resolution = self.point_resolution
        SlTrace.lg(f"fill_points: {pl(point_list)} res:{point_resolution}", "xpoint")
        fill_point_set = set()
        if len(point_list) < 3:
            return set()
         
        p1 = point_list[0]
        for i in range(2,len(point_list)):
            p2 = point_list[i]
            p3 = point_list[i-1]
            points = self.get_points_triangle(p1,p2,p3,
                                    point_resolution=point_resolution)
            fill_point_set.update(points)
        return fill_point_set

    def get_points_triangle(self,p1,p2,p3, point_resolution=None):
        """ Get points in triangle
        The goal is that, when each returned point is used in generating the
        including cell, the resulting cells completely fill the triangle's
        region with minimum number of gaps and minimum fill outside the
        triangle. Strategy fill from left to right with vertical fill lines
        separated by a pixel distance of point_resolution which will be
        converted to fill points.
        
        Strategy

                                       * pxs[1]
                                    *   *
                                  *      *        
                                *       |*
                              *         | *
                            * |         |  *
                          *   |         |  *
                        *|    |         |   *
                      *  |    |  more   |   *
                    *    |    |   lines |    *
                 *  |    |    |         |    *
        pxs[0] *    |    |    |         |    |*  
                 *  |    |    |         |    |*
                    *    |    |         |    | *
                      *  |    |         |    | *
                         *    |         |    |  *
                             *          |    |  *
                                *       |    |  *
                                   *    |    |   *
                                      * |    |   *
                                         *   |    *
                                           * |    |*
                                             *    |*
                                                *  *
                                                    *  pxs[2]

        Begin by adding points directly included by the
        triangle's three edges.  Then continue with
        the following.
        
        Construct a series of vertical fill lines separated
        by point_resolution such that the fill points from
        these lines will appropriately cover the triangle.
 
        Organize the triangle vertex points by ascending x
        coordinate value into list pxs:
                pxs[0]: pxs[0].x <= pxs[1].x minimum x
                pxs[1]: pxs[1].x <= pxs[2].x
                pxs[2]: pxs[2].x             maximum x
        
        Construct a list of x-coordinate values separated by
        point_resolution: xs
            pxs[0].x < xs[i] < pxs[2].x
        
        Construct a list of point pairs, each point being
        the end point of a vertical fill line with x coordinate
        in xs[i].  The vertical fill line end points will be
        stored in a coordinated pair of lists:
            pv_line_02 - end points on psx[0]-pxs[2]
            pv_line_012 - end points on pxs[0]-pxs[1]-pxs2]
        Each pair of end points is constructed for an
        x-coordinate found in xs[i] as such:
            1. One end point will be on the pxs[0]-pxs[2] line
               with x-coordinate of xs[i], and stored in
               list pv_line_02[i].
            2. The other end point will be, also with
               x-coordinate xs[i] on
                A. pxs[0]-pxs[1] line when xs[i] < pxs[1].x
                B. pxs[1]-pxs[2] line when xs[i] >= pxs[1].x
                    
        Each vertical fill line segment constructed from
        end points pv_line_02[i] and pv_line_012[i] is used
        to generate fill points at a separation of a distance
        point_resolution.
        :p1,p2,p3: triangle points (x,y) tupple
        :point_resolution:  maximum pint separation to avoid
            gaps default: self.point_resolution
        :returns: set of fill points
        """
        SlTrace.lg(f"get_points_triangle:{pl(p1)} {pl(p2)} {pl(p3)}", "xpoint")
        fill_points = set()
        if point_resolution is None:
            point_resolution = self.point_resolution
        por = point_resolution
        # Include the edge lines
        lep = self.get_line_points(p1, p2, point_resolution=por)
        fill_points.update(lep)
        lep = self.get_line_points(p2, p3, point_resolution=por)
        fill_points.update(lep)
        lep = self.get_line_points(p3, p1, point_resolution=por)
        fill_points.update(lep)
        x_min_p = p1
        x_min = p1[0]
        
        # Find x_min, max_x
        # Create pxs a list of the points
        # in ascending x order
        pxs = [x_min_p]    # point to process
                                # starting with min
        for p in [p2,p3]:
            x = p[0]
            if x < x_min:
                x_min = x 
                x_min_p = p
                pxs.insert(0,p)
            elif len(pxs) > 1 and x < pxs[1][0]:
                pxs.insert(1,p)
            else:
                pxs.append(p)
        # Generate list of x values separated by point_resolution
        # starting at x = x_min ending at or after max_x
        #
        xs = []
        x = x_min
        while x <= pxs[2][0]:
            xs.append(x)
            x += point_resolution
            
        SlTrace.lg(f"pxs:{pxs}", "xpoint")
        
        # Start including the three edges as perimiter   
        line_01_points = self.get_line_points(pxs[0], pxs[1],
                                point_resolution=point_resolution)
        line_02_points = self.get_line_points(pxs[0],pxs[2],
                                point_resolution=point_resolution)
        line_12_points = self.get_line_points(pxs[1], pxs[2],
                                point_resolution=point_resolution)
        # Place the edge points in the fill area
        fill_points.update(line_01_points)
        fill_points.update(line_02_points)
        fill_points.update(line_12_points)
        
        # proceed from left (x_min) to right (max_x)
        pv_line_02 = []
        pv_line_012 = []
        # populate vertical fill line line_02 end points
        self.set_line_funs(pxs[0],pxs[2])
        for i in range(len(xs)):
            x = xs[i]
            y = self.line_y(x)
            pv_line_02.append((x,y))
        
        # populate vertical fill line_012 end points
        self.set_line_funs(pxs[0],pxs[1])
        on_line_12 = False   # on or going to be
        last_line_01_x = pxs[1][0]
        for i in range(len(xs)):
            x = xs[i]
            if on_line_12 or x >= last_line_01_x:
                if not on_line_12:
                    self.set_line_funs(pxs[1], pxs[2])
                    on_line_12 = True  
            y = self.line_y(x)
            p = (x,y)
            pv_line_012.append(p)
        
        # Processing vertical fill lines
        for i in range(len(xs)):
            p1 = pv_line_02[i] 
            p2 = pv_line_012[i] 
            vline_points = self.get_line_points(p1,p2,
                                point_resolution=point_resolution)
            fill_points.update(vline_points)
        return fill_points

    def get_drawn_line_points(self, p1, p2, width=None,
                              point_resolution=None):
        """ Get drawn line fill points
        Find perimeter of surrounding points of a rectangle
        For  simplicity we consider vertical width
        :p1: beginning point
        :p2: end point
        :width: width of line
            default: self.line_width
        :point_resolution: fill point spacing
            default: self.point_resolution
        :returns: set of fill points
        """
        ###pts = self.get_line_points(p1,p2)
        ###return set(pts)
        
        if width is None:
            width = self.line_width
        if point_resolution is None:
            point_resolution = self.point_resolution
        pr = point_resolution
        SlTrace.lg(f"get_drawn_Line_points {p1} {p2}"
                   f" width: {width} res: {pr}", "xpoint")
        p1x,p1y = p1
        p2x,p2y = p2
        self.set_line_funs(p1, p2)
        
        dx = self.lfun_unorm_x*width/2 # draw width offsets
        dy = self.lfun_unorm_y*width/2
        pp1 = (p1x+dx,p1y+dy) # upper left corner
        pp2 = (p2x+dx,p2y+dy) # upper right corner
        pp3 = (p2x-dx,p2y-dy) # lower right corner
        pp4 = (p1x-dx,p1y-dy) # lower left corner
        perim_list = [pp1, pp2, pp3, pp4]
        filled_points = self.fill_points(perim_list)
        return filled_points
    
    def get_line_points(self, p1, p2, point_resolution=None):
        """ Get spaced points on line from p1 to p2
        :p1: p(x,y) start
        :p2: p(x,y) end
        :point_resolution: maximum separation
        :returns: list of points from p1 to p2
                separated by point_resolution pixels
        """
        SlTrace.lg(f"\nget_line_points: p1={pl(p1)} p2={pl(p2)}", "xpoint")
        self.set_line_funs(p1=p1, p2=p2)
        if p1 == p2:
            return [p1,p2]
        
        if point_resolution is None:
            point_resolution = self.point_resolution
        x1,y1 = p1
        x2,y2 = p2
        p_chg = point_resolution
        
        pt = p1
        point_list = [p1]       # Always include end points
        p_len = 0.               # Travel length
        while True:
            pt_x,pt_y = pt
            p_len += p_chg
            SlTrace.lg(f"pt={pl(pt)} p_len={p_len:.5}", "xpoint")
            if p_len > self.lfun_dist:
                break
            
            pt_x = int(x1 + p_len*self.lfun_cos)
            pt_y = int(y1 + p_len*self.lfun_sin)
            pt = (pt_x,pt_y)
            point_list.append(pt)
        
        # at end point, if not already there
        if pt != point_list[-1]:
            point_list.append(pt)
            
        SlTrace.lg(f"return: {point_list}", "xpoint")
        return point_list
    
    def populate_cells_from_points(self, points, color=None):
        """ Populate display cells, given points, color
        :points: set/list of points(x,y) tuples
        :color: cell color
                default: self._color
        """
        SlTrace.lg(f"populate_cells_from_points: add: "
                   f" {len(points)} points before:"
                   f" {len(self.cells)}", "point")
        if color is None:
            color = self._color
        
        for point in points:
            SlTrace.lg(f"point:{point}", "point")
            self.update_cell(pt=point, color=color)
        SlTrace.lg(f"populate_cells: cells after: {len(self.cells)}", "xpoint")

    def color_str(self, color):
        """ convert turtle colors arg(s) to color string
        :color: turtle color arg
        """
        color_str = color
        if (color_str is None
             or (isinstance(color_str, tuple)
                  and len(color_str) == 0)
             ):
            color_str = self._color
        if isinstance(color_str,tuple):
            if len(color_str) == 1:
                color_str = color_str[0]
            else:
                color_str = "pink"  # TBD - color tuple work
        return color_str
    
    def braille_for_color(self, color):
        """ Return dot list for color
        :color: color string or tuple
        :returns: list of dots 1,2,..6 for first
                letter of color
        """
        
        if color is None:
            color = self._color
        if color is None:
            color = ("black")
        color = self.color_str(color)
        c = color[0]
        dots = self.braille_for_letter(c)
        return dots
    
    def braille_for_letter(self, c):
        """ convert letter to dot number seq
        :c: character
        :returns: dots tupple (1,2,3,4,5,6)
        """
        if c not in BrailleDisplay.dots_for_character:            c = " " # blank
        dots = BrailleDisplay.dots_for_character[c]
        return dots
        
    def complete_cell(self, cell, color=None):
        """ create/Fill braille cell
            Currently just fill with color letter (ROYGBIV)
        :cell: (ix,iy) cell index or BrailleCell
        :color: cell color default: current color
        """
        if color is None:
            color = self._color
        dots = self.braille_for_color(color)
        bc = BrailleCell(ix=cell[0],iy=cell[1], dots=dots, color=color)
        self.cells[cell] = bc

    def display_braille_window(self, title, show_points=False):
        """ Display current braille in a window
        :title: window title
        :show_points: Show included points instead of braille dots
                default: False - show braille dots
        """
        mw = tk.Tk()
        if title is not None and title.endswith("-"):
            title += " Braille Window"
        mw.title(title)
        mw.geometry("800x800")
        self.braille_mw = mw
        canvas = tk.Canvas(mw, width=self.win_width, height=self.win_height)
        canvas.pack(expand=1, fill='both')
        self.braille_canvas = canvas
        self.overlay_tk_window(canvas)
        for ix in range(self.grid_width):
            for iy in range(self.grid_height):
                cell_ixy = (ix,iy)
                if cell_ixy in self.cells:
                    self.display_cell(self.cells[cell_ixy],
                                      show_points=show_points)
        mw.update()     # Make visible

    def print_cells(self, title=None):
        """ Display current braille in a window
        """
        if title is not None:
            print(title)
        for ix in range(self.grid_width):
            for iy in range(self.grid_height):
                cell_ixy = (ix,iy)
                if cell_ixy in self.cells:
                    SlTrace.lg(f"ix:{ix} iy:{iy} {cell_ixy}"
                          f" rect: {self.get_cell_ullr_tur(ix,iy)}"
                          f"  win rect: {self.get_cell_ullr_win(ix,iy)}")
        SlTrace.lg("")



    def show_canvas_item(self, item_id,
                          canvas=None, prefix=None):
        """ display changing values for item
        """
        if canvas is None:
            canvas = self.rt_canvas
        if prefix is None:
            prefix = ""
        self.tracking_show_item_id = item_id
        iopts = canvas.itemconfig(item_id)
        itype = canvas.type(item_id)
        coords = canvas.coords(item_id)
        if itype in self.tk_item_samples:
            item_sample_iopts = self.tk_item_samples[itype]
        else:
            item_sample_iopts = None
        SlTrace.lg(f"{prefix} {item_id}: {itype} {coords}")
        for key in iopts:
            val = iopts[key]
            is_changed = True     # assume entry option changed
            if item_sample_iopts is not None:
                is_equal = True # Check for equal item option
                sample_val = item_sample_iopts[key]
                if len(val) == len(sample_val):
                    for i in range(len(val)):
                        if val[i] != sample_val[i]:
                            is_equal = False
                            break
                    if is_equal:
                        is_changed = False
            if is_changed: 
                SlTrace.lg(f"    {key} {val}")
            self.tk_item_samples[itype] = iopts

    def populate_cells_from_canvas(self):
        """ populate cells covered by canvas objects
        """
        canvas = self.rt_canvas
        for ix in range(self.grid_width):
            for iy in range(self.grid_height):
                cx1,cy1,cx2,cy2 = self.get_cell_ullr_win(ix=ix, iy=iy)
                items_over = canvas.find_overlapping(cx1,cy1,cx2,cy2)
                folp_str = f"ix:{ix}, iy:{iy} canvas.find_overlapping(cx1={cx1},cy1={cy1},cx2={cx2},cy2={cy2})"
                if len(items_over) > 0:
                    top_item = items_over[-1]
                    canvas_item = top_item
                    itype = canvas.type(canvas_item)
                    if False and itype != "line": # TFD
                        continue
                    color_tuple = canvas.itemconfigure(canvas_item, "fill")
                    color = color_tuple[-1]
                    if color == "":
                        color = self._color
                    point_win = (cx1+cx2)/2,(cy1+cy2)/2
                    point_tur = self.cvt_win_pt_to_tur(point_win)
                    SlTrace.lg(f"{folp_str} item:{canvas_item} {color}")
                    SlTrace.lg(f"    point:{point_tur} color={color}"
                               f" coords:{canvas.coords(canvas_item)}", "point")
                    self.update_cell(pt=point_tur, color=color, canvas_item=canvas_item)
        SlTrace.lg(f"populate_cells(canvas): cells after: {len(self.cells)}", "xpoint")

    def print_tk_canvas_opts(self, canvas=None, title=None):
        """ log canvas options
        :canvas: Canvas object
        :title: optional title
        """
        if title is None:
            title = "Canvas options"
        
        SlTrace.lg(title)
        if canvas is None:
            canvas = self.rt_canvas
        tk_opts = canvas.configure()
        for tk_opt in sorted(tk_opts):
            SlTrace.lg(f"    {tk_opt}: {tk_opts[tk_opt]}")
        
    def print_tk_items(self, title=None):
        """ Display current braille in a window
        """
        self.tk_item_samples = {}
        if title is not None:
            SlTrace.lg(title)
        else:
            title = ""
        canvas = self.rt_canvas
        self.print_tk_canvas_opts(canvas=canvas, title=title+" canvas options")
        for item in sorted(canvas.find_all()):
            self.show_canvas_item(item)
        SlTrace.lg("")

    def display(self, title=None, braille_window=True, braille_print=True,
               print_cells=False,
               points_window=False,
               tk_items=False,
               tk_window_copy=False, tk_window_selected=False,
               overlay_braille=False,
               all=False):
        """ display grid
        :braille_window: True - make window display of braille
                        default:True
        :braille_print: True - print braille
                        default: True
        :print_cells: True - print out non-empty cells
                        default: False
        :title: text title to display
                    default:None - no title
        :points_window: make window showing display points
                        instead of braille dots
                    default: False - display dots
        :tk_items: True - display tkinter obj in cell
                    default: False
        :tk_window_copy: True - display copy of tk window
                    from scaning tk canvas items
                    default: False
        :tk_window_selected: True - show tk window with selected (by braille cell)
                    shown
                    default: False
        :overlay_braille:  Place braille view over the primary tk display
                    default: False - no overlay
        :all: True - display/print all windows - shorthand for seeing all
                    default: False
        """
        self.populate_cells_from_canvas()
        if overlay_braille:
            self.overlay_braille_window()
        if all or braille_window:
            tib = title
            if tib is not None and tib.endswith("-"):
                tib += " Braille Window"
            self.display_braille_window(title=tib)
        if all or points_window:
            tib = title
            if tib is not None and tib.endswith("-"):
                tib += " Display Points"
            self.display_braille_window(title=tib, show_points=points_window)
        if all or braille_print:
            tib = title
            if tib is not None and tib.endswith("-"):
                tib += " Braille Print Output"
            self.print_braille(title=tib)
        if all or print_cells:
            tib = title
            if tib is not None and tib.endswith("-"):
                tib += " Braille Cells"
            self.print_cells(title=tib)
        if all or tk_items:
            tib = title
            if tib is not None and tib.endswith("-"):
                tib += " Tk Cells"
            self.print_tk_items(title=tib)
        if all or tk_window_copy:
            tib = title
            if tib is not None and tib.endswith("-"):
                tib += " tk_window_copy"
            self.display_tk_window_copy(title=tib)
        if all or tk_window_selected:
            tib = title
            if tib is not None and tib.endswith("-"):
                tib += " tk_window_selected"
            self.display_tk_window_selected(title=tib)

    def get_tk_create_args(self, canvas, item_id):
        """ Create Canvas._create args given canvas and item id
        :canvas: canvas object
        :item_id: item id
        :returns: (itemType, args, kw)
            itemType: item type e.g. "rectangle"
            args: tuple of positional args
            kw: keyword dictionary
        """
        iopts = canvas.itemconfig(item_id)
        itemType = canvas.type(item_id)
        coords = canvas.coords(item_id)
        args = list(coords)     # args start with coords by default
        kw = {}
        for iopt in iopts:
            val = iopts[iopt]
            if isinstance(val, tuple):
                val = val[-1]
            kw[iopt] = val
        return itemType, args, kw

    def show_canvas_diff_item(self, key, canvas1, canvas2, show_eq=False,
                               prefix=None):
        """ Show difference between canvas items
        :key: option key
        :canvas1: first canvas
        :canvas2: second canvas
        :show_eq: show even if equal
                default: don't show if equal
        :prefix: optional line prefix
        """
        if prefix is None:
            prefix = ""
        opt1 = canvas1.configure(key)
        opt2 = canvas2.configure(key)
        if opt1 == opt2 and not show_eq:
            return
        diff_str  = f"{prefix}{key}:" 
        if len(opt1) != len(opt2):
            diff_str += f"len1{len(opt1)} != len2{len(opt2)}"
            SlTrace.lg(diff_str)
            self.show_canvas_item_opt(key, canvas1)
            self.show_canvas_item_opt(key, canvas2)
        else:
            for i in range(len(opt1)):
                val1 = opt1[i]
                val2 = opt2[i]
                if val1 != val2:
                    diff_str += f"  {val1}!={val2}"
                else:
                    diff_str += f"  {val1}"
        SlTrace.lg(diff_str)

    def show_canvas_item_OLD(self, item_id, canvas=None, prefix=None):
        """ Show canvas item
        :item_id: canvas item id
        :canvas: canvas object
                default: self.rt_canvas
        :prefix: optional prefix for each line
        """
        self.tracking_show_item_id = item_id
        if prefix is None:
            prefix = ""
        prefix += f" {item_id}:"
        if canvas is None:
            canvas = self.rt_canvas
        canvas_item = canvas.find_withtag(item_id)

        
        opts_keys = canvas_item.keys() 
        for key in opts_keys:
            self.show_canvas_item_opt(key, canvas=canvas,
                                      prefix=prefix)
        

    def show_canvas_item_opt(self, key, canvas, prefix=None):
        """ Show canvas item's option
        :key: option key
        :canvas: canvas
        """
        opt = canvas.configure(key)
        if prefix is None:
            prefix = ""
        opt_str  = f"{prefix}{key}:"
        for i in range(len(opt)):
            val = opt[i]
            opt_str += f"  {val}"
        SlTrace.lg(opt_str)
        
                
    def show_canvas_diff(self, canvas1, canvas2, title=None):
        """ Show canvas changes
        :canvas2, canvas2: canvases to compare
        :title: optional title
        """
        if title is not None:
            SlTrace.lg(title)
        # First - canvas options
        opts1 = canvas1.configure()
        opts1_keys = opts1.keys()
        opts2 = canvas2.configure()
        opts2_keys = sorted(opts2.keys())
        opts_keys = sorted(list(set(opts1_keys).union(set(opts2_keys))))
        opts_keys1 = sorted(list(set(opts1_keys).difference(set(opts2_keys))))
        if len(opts_keys1) > 0:
            SlTrace.lg("Only in canvas1:" + ",".join(opts_keys1))
        opts_keys2 = sorted(list(set(opts2_keys).difference(set(opts1_keys))))
        if len(opts_keys2) > 0:
            SlTrace.lg("Only in canvas2:" + ",".join(opts_keys2))
        for key in opts_keys:
            #SlTrace.lg(f"key:{key}")
            if key in opts1_keys and key in opts2_keys:
                self.show_canvas_diff_item(key, canvas1, canvas2, prefix= "  ")
            elif key in opts1_keys:
                self.show_canvas_item_opt(key, canvas1, prefix = "1 ")
            elif key in opts2_keys:
                self.show_canvas_item_opt(key, canvas2, prefix = "2 ")

    def get_cnf(self, widget=None):
        """ Get cnf
        :widget: desired widget default self.rt_canvas
        :returns: cnf for creation eg. copy of Canvas
        """
        if widget is None:
            widget = self.rt_canvas
        cnf = {}
        opts = widget.configure()
        for opt_key in opts:
            opt = opts[opt_key]
            if len(opt) == 2:
                continue        # skip associations
            if opt_key == "class":
                continue        # Not found
            if opt_key == "colormap":
                continue        # Not found
            if opt_key == "container":
                continue        # Not found
            if opt_key == "padx":
                continue        # Not found
            if opt_key == "pady":
                continue        # Not found
            if opt_key == "visual":
                continue        # Not found
            opt_val = opt[-1]
            cnf[opt_key] = opt_val
        return cnf
                        
    def overlay_braille_window(self, dst_canvas=None, tk_canvas=None,
                               show_points=False):
        """ Overlay braille markings on given canvas
            Can be a blank canvas or can be the tk_canvas. Will ignore all
            existing annotation items such as braille cells
        :dst_canvas: destination for braille markings
                    default: tk_canvas
        :tk_canvas: source of tk items
                    default: self.rt_canvas
        :show_points: display (estimated) sample points from canvas
                    default: False - no sample points
        """
        if tk_canvas is None:
            tk_canvas = self.rt_canvas
        if dst_canvas is None:
            dst_canvas = tk_canvas
        # ignore annotation items, e.g. braille cells
        annotated_items = tk_canvas.find_withtag(self.annotate_tag)
        annotated_set = set(annotated_items)
        braille_cells = {}
        for ix in range(self.grid_width):
            for iy in range(self.grid_height):
                cx1,cy1,cx2,cy2 = self.get_cell_ullr_win(ix=ix, iy=iy)
                items_over_raw = tk_canvas.find_overlapping(cx1,cy1,cx2,cy2)
                items_over = []
                for item in items_over_raw:
                    if item not in annotated_set:
                        items_over.append(item)     # Look at nonannotated
                folp_str = f"ix:{ix}, iy:{iy} canvas.find_overlapping(cx1={cx1},cy1={cy1},cx2={cx2},cy2={cy2})"
                if len(items_over) > 0:
                    top_item = items_over[-1]
                    canvas_item = top_item
                    itype = tk_canvas.type(canvas_item)
                    ###if False and itype != "line": # TFD
                    ###    continue
                    color_tuple = tk_canvas.itemconfigure(canvas_item, "fill")
                    color = color_tuple[-1]
                    if color == "":
                        color = self._color
                    point_win = (cx1+cx2)/2,(cy1+cy2)/2
                    point_tur = self.cvt_win_pt_to_tur(point_win)
                    SlTrace.lg(f"{folp_str} item:{canvas_item} {color}")
                    SlTrace.lg(f"    point:{point_tur} color={color}"
                               f" coords:{tk_canvas.coords(canvas_item)}", "point")
                    self.update_cell(braille_cells=braille_cells,
                                     pt=point_tur, color=color,
                                      canvas_item=canvas_item)
        for cell_ixy in braille_cells:
            self.display_cell(braille_cells[cell_ixy],
                              canvas = dst_canvas,
                              show_points=show_points)
            
                        
    def overlay_tk_window(self, canvas):
        """ Overlay a copy of tk window on given canvas
        """
        tk_canvas = self.rt_canvas
        tk_canvas = self.rt_canvas
        tk_canvas_items = sorted(tk_canvas.find_all())
        for item_tag in tk_canvas_items:
            itemType, args, kw = self.get_tk_create_args(tk_canvas, item_tag)
            if itemType == "image":
                continue                # ignore
            canvas._create(itemType, args, kw)
                        
    def display_tk_window_copy(self, title=None):
        """ Display a copy of tk window
        """
        mw = tk.Tk()
        if title is not None and title.endswith("-"):
            title += " tk_window_copy"
        mw.title(title)
        tk_cnf = self.get_cnf()
        canvas = tk.Canvas(mw, cnf=tk_cnf)
        canvas.config(width=self.win_width,
                      height=self.win_height)
        canvas.pack()
        tk_canvas = self.rt_canvas
        self.show_canvas_diff(tk_canvas, canvas, title="window_copy")
        self.print_tk_canvas_opts(canvas=canvas, title=title+" canvas opts")
        self.tk_item_samples = {}
        if title is not None:
            SlTrace.lg(title)
        tk_canvas = self.rt_canvas
        tk_canvas_items = sorted(tk_canvas.find_all())
        SlTrace.lg("tk_window_copy tags")
        for item_tag in tk_canvas_items:
            itemType, args, kw = self.get_tk_create_args(tk_canvas, item_tag)
            if itemType == "image":
                continue                # ignore
            SlTrace.lg(f"{item_tag:3}: type: {itemType} args:{args}")
            SlTrace.lg(f"    {kw}")
            canvas._create(itemType, args, kw)

    def display_tk_window_selected(self, title=None):
        """ Display a copy of tk window
        """
        mw = tk.Tk()
        if title is not None and title.endswith("-"):
            title += " tk_window_selected"
        mw.title(title)
        tk_cnf = self.get_cnf()
        canvas = tk.Canvas(mw, cnf=tk_cnf)
        canvas.pack()
        canvas.config(width=self.win_width,
                      height=self.win_height)
        self.tk_item_samples = {}
        if title is not None:
            SlTrace.lg(title)
        tk_canvas = self.rt_canvas
        self.print_tk_canvas_opts(canvas=canvas, title=title+" canvas options")
        for item_tag in sorted(tk_canvas.find_all()):
            itemType, args, kw = self.get_tk_create_args(tk_canvas, item_tag)
            canvas._create(itemType, args, kw)

    def clear_display(self):
        """ Clear display for possible new display
        """
        self.clear()
        
    def snapshot(self, title=None, clear_after=False):
        """ Take snapshot of current braille_screen
        :title: title of snapshot
        :clear_after: clear braille screen after snapshot
        """
        
    
    
    def display_cell(self, cell, canvas=None, show_points=False):
        """ Display cell
        :cell: BrailleCell
        :canvas: canvas on wich to display the cell
                default: self.tk_canvas
        :show_points: show points instead of braille
                default: False --> show braille dots
        """
        ix = cell.ix
        iy = cell.iy 
        if canvas is None:
            canvas = self.braille_canvas
        cx1,cy1,cx2,cy2 = self.get_cell_ullr_win(ix=ix, iy=iy)
        canvas.create_rectangle(cx1,cy1,cx2,cy2,
                                tags=self.annotate_tag)
        
        color = self.color_str(cell._color)
        if show_points:
            dot_size = 1            # Display cell points
            dot_radius = dot_size//2
            if dot_radius < 1:
                dot_radius = 1
                dot_size = 2
            for pt in cell.points:
                dx,dy = self.cvt_tur_pt_to_win(pt)
                x0 = dx-dot_radius
                y0 = dy+dot_size 
                x1 = dx+dot_radius 
                y1 = dy
                canvas.create_oval(x0,y0,x1,y1, fill=color,
                                                tags=self.annotate_tag)
            self.braille_mw.update()    # So we can see it now 
            return
            
        dots = cell.dots
        grid_width = cx2-cx1
        grid_height = cy1-cy2       # y increases down
        # Fractional offsets from lower left corner
        # of cell rectangle
        ll_x = cx1      # Lower left corner
        ll_y = cy2
        ox1 = ox2 = ox3 = .3 
        ox4 = ox5 = ox6 = .7
        oy1 = oy4 = .15
        oy2 = oy5 = .45
        oy3 = oy6 = .73
        dot_size = .25*grid_width   # dot size fraction
        dot_radius = dot_size//2
        dot_offset = {1: (ox1,oy1), 4: (ox4,oy4),
                      2: (ox2,oy2), 5: (ox5,oy5),
                      3: (ox3,oy3), 6: (ox6,oy6),
                      }
        for dot in dots:
            offsets = dot_offset[dot]
            off_x_f, off_y_f = offsets
            dx = ll_x + off_x_f*grid_width
            dy = ll_y + off_y_f*grid_height
            x0 = dx-dot_radius
            y0 = dy+dot_size 
            x1 = dx+dot_radius 
            y1 = dy
            canvas.create_oval(x0,y0,x1,y1, fill=color, 
                                tags=self.annotate_tag)

    def update(self):
        self.mw.update()
                
    def get_cell_ullr_win(self, ix, iy):
        """ Get cell's window rectangle x, y  upper left, x,  y lower right
        :ix: cell x index
        :iy: cell's  y index
        :returns: window(0-max): (w_left_x,w_upper_y,
                                  w_right_x,w_lower_y) where
            w_left_x,w_upper_y: are upper left coordinates
            w_right_x,w_lower_y: are lower right coordinates
        """
        ixmax = len(self.cell_xs)-2  # last element is upper bound
        iymax = len(self.cell_ys)-2
        w_left_x = self.cell_xs[0]          # left edge
        w_upper_y = self.cell_ys[0]      # top edge
        w_right_x = self.cell_xs[ixmax-1]
        w_lower_y = self.cell_ys[iymax-1]
        
        if ix >= 0:
            if ix <= ixmax:
                w_left_x = self.cell_xs[ix]
                w_right_x = self.cell_xs[ix+1]
            else:
                w_left_x = self.cell_xs[ixmax]
                w_right_x = self.cell_xs[ixmax+1]
        if iy >= 0:
            if iy <= iymax:
                w_upper_y = self.cell_ys[iy]
                w_lower_y = self.cell_ys[iy+1]
            else:
                w_upper_y = self.cell_ys[iymax]
                w_lower_y = self.cell_ys[iymax+1]
        return (w_left_x,w_upper_y, w_right_x,w_lower_y)

    def cvt_tur_x_to_win(self, tur_x):
        """ Convert turtle (canvas) x coordinate to window x
        :tur_x: turtle x coordinate
        :returns: window x coordinate
        """
        win_x = tur_x - self.x_min
        ###win_x = tur_x
        SlTrace.lg(f"cvt_tur_x_to_win({tur_x}) => {win_x}")
        return win_x 

    def cvt_tur_y_to_win(self, tur_y):
        """ Convert turtle (canvas) y coordinate to window y
        :tur_y: window y coordinate
        :returns: window y coordinate
        """
        win_y = -tur_y + self.y_max
        ###win_y = tur_y
        SlTrace.lg(f"cvt_tur_y_to_win({tur_y}) => {win_y}")
        return win_y 

    def cvt_win_x_to_tur(self, win_x):
        """ Convert window (canvas) x coordinate to turtle x
        :win_x: window x coordinate
        :returns: turtle x coordinate
        """
        tur_x = win_x + self.x_min
        ###tur_x = win_x
        SlTrace.lg(f"cvt_win_x_to_tur({win_x}) => {tur_x}")
        return tur_x 

    def cvt_win_y_to_tur(self, win_y):
        """ Convert window (canvas) y coordinate to turtle y
        :win_y: window y coordinate
        :returns: turtle y coordinate
        """
        tur_y = -win_y + self.y_max
        ###tur_y = win_y
        SlTrace.lg(f"cvt_win_y_to_tur({win_y}) => {tur_y}")
        return tur_y 
        
                
    def cvt_tur_pt_to_win(self, pt):
        """ Get point in window coordinates
        :pt: (x,y) point in turtle coordinates
        :returns: (x,y)
        """
        tu_x,tu_y = pt
        w_x = self.cvt_tur_x_to_win(tu_x)
        w_y = self.cvt_tur_y_to_win(tu_y)
        SlTrace.lg(f"cvt_tur_pt_to_win({pt}) => {(w_x,w_y)}")
        return (w_x,w_y)

    def cvt_win_pt_to_tur(self, point):
        """ Convert window(canvas) to turtle point coord
        :point: window x,y coordinate
        :returns: turtle x,y coordinate
        """
        w_x,w_y = point
        x = self.cvt_win_x_to_tur(w_x)
        y = self.cvt_win_y_to_tur(w_y)
        SlTrace.lg(f"cvt_win_pt_to_tur({point}) => {(x,y)}")
        return (x,y)
                    
        
    def get_cell_ullr_tur(self, ix, iy):
        """ Get cell's turtle rectangle x, y  upper left, x,  y lower right
        :ix: cell x index
        :iy: cell's  y index
        :returns: (tur_left_x,tur_upper_y, tur_right_x,tur_lower_y)
        """
        w_left_x,w_upper_y, w_right_x,w_lower_y = self.get_cell_ullr_win(ix,iy)
        tur_left_x,tur_upper_y = self.cvt_win_pt_to_tur((w_left_x,w_upper_y))
        tur_right_x,tur_lower_y = self.cvt_win_pt_to_tur((w_right_x,w_lower_y))
        return (tur_left_x,tur_upper_y, tur_right_x,tur_lower_y)
                    
    def print_braille(self, title=None):
        """ Output braille
        """
        if title is not None:
            print(title)
        for iy in range(self.grid_height):
            line = ""
            for ix in range(self.grid_width):
                cell_ixy = (ix,iy)
                if cell_ixy in self.cells:
                    cell = self.cells[cell_ixy]
                    color = cell.color_str()
                    line += color[0]
                else:
                    line += " "
            line.rstrip()
            print(line)

    """
    turtle commands
    These commands:
        1. call turtle via self.rtu, self.screen
        4. return turtle call return
    """
    def backward(self, length):
        return self.forward(-length)
    
    def color(self, *args):
        rt = self.rtu.color(*args)
        return rt

    def pencolor(self, *args):
        rt = self.rtu.pencolor(*args)
        return rt
        
    def fillcolor(self, *args):
        rt = self.rtu.fillcolor(*args)
        return rt
        
    def dot(self, size=None, *color):
        self.rtu.dot(size, *color)
    
    def filling(self):
        return self.rtu.filling()
    
    def begin_fill(self):
        self.rtu.begin_fill()
         
                
    def end_fill(self):
        self.rtu.end_fill()
    
    def forward(self, length):
        """ Make step forward, updating location
        """
        self.forward_pre(length)
        self.rtu.forward(length)
        self.forward_post(length) 
    
    def goto(self, x, y=None):
        self.goto_pre(x,y)
        #convert to canvas x,y
        '''
        w_x = self.cvt_tur_x_to_win(x) 
        if y is None:
            w_y = None 
        else:
            w_y = self.cvt_tur_y_to_win(y)
            w_y -= self.win_height
        self.rtu.goto(w_x,w_y)
        '''
        '''
        x = x + self.x_max/2 + 1*(self.cell_xs[1]-self.cell_xs[0])          # Fudge
        y = y + self.y_min/2 - 2*(self.cell_ys[1]-self.cell_ys[0])          # Fudge
        '''
        ''''''
        x += self.x_max/2 + 10*(self.cell_xs[1]-self.cell_xs[0])
        y -= (self.y_max/2 + 4*(self.cell_ys[1]-self.cell_ys[0]))
        '''''' 
        self.rtu.goto(x,y)
        self.goto_post(x,y) 

    # tracking
    def get_tk_ids(self, canvas=None):
        """ Get camvas ids in sorted order
        :canvas: canvas object
                default: self.screen.getcanvas
        :returns: ids in ascending order [] if none
        """
        if canvas is None:
            canvas = self.rt_canvas
        canvas_ids = canvas.find_all()
        item_ids = []
        if len(canvas_ids) > 0:
            item_ids = sorted(canvas_ids)
        return item_ids
    
    def get_tk_id(self, canvas=None):
        """ Get last id, 0 if none
        :returns: last item id
                0 if none
        """
        canvas_ids = self.get_tk_ids(canvas)
        if len(canvas_ids) > 0:
            item_id = canvas_ids[-1]
        else:
            item_id = 0
        return item_id

    def forward_pre(self, length):
        """ do precall setup
        """
        self.tracking_forward_length = length 
        self.tracking_forward_item_id = self.get_tk_id()
        # List items before forward
        for item_id in range(self.tracking_show_item_id+1,
                        self.tracking_forward_item_id):
            self.show_canvas_item(item_id)
        
        SlTrace.lg(f"forward({length})"
                f" prev id: {self.tracking_forward_item_id}")
    # tracking
    def forward_post(self, length):
        """ do postcall setup
        """
        prefix = f"==>"
        _ = length
        post_id = self.get_tk_id()
        SlTrace.lg(f"   post_id:{post_id}")
        for item_id in range(self.tracking_show_item_id+1,
                        post_id+1):
            self.show_canvas_item(item_id, prefix=prefix)

    def goto_pre(self, x, y=None):
        """ do precall setup
        """
        self.tracking_goto_x = x 
        self.tracking_goto_y = y 
        self.tracking_goto_item_id = self.get_tk_id()
        # List items before goto
        for item_id in range(self.tracking_show_item_id+1,
                        self.tracking_goto_item_id):
            self.show_canvas_item(item_id)
        
        SlTrace.lg(f"goto({x}, {y})"
                f" prev id: {self.tracking_goto_item_id}")
    # tracking
    def goto_post(self, x, y=None):
        """ do postcall setup
        """
        prefix = f"==>"
        post_id = self.get_tk_id()
        SlTrace.lg(f"   post_id:{post_id}")
        for item_id in range(self.tracking_show_item_id+1,
                        post_id+1):
            self.show_canvas_item(item_id, prefix=prefix)
        
    def heading(self):
        rt = self.rtu.heading()
        return rt 
            
    def setpos(self, x, y=None):
        return self.goto(x, y=y) 
    def setposition(self, x, y=None):
        return self.goto(x, y=y) 
    
    def left(self, angle):
        self.rtu.left(angle)
    
    def pendown(self):
        self.rtu.pendown()
    
    def penup(self):
        self.rtu.penup()
    
    def right(self, angle):
        self.rtu.right(angle)

    def setheading(self, to_angle):
        self.rtu.setheading(to_angle)
    
    def seth(self, to_angle):
        return self.setheading(to_angle)
        
    def speed(self, speed):
        rt = self.rtu.speed(speed)
        return self.rtu.speed(speed)
    
    def mainloop(self):
        return self.screen.mainloop()
    def done(self):
        return self.mainloop()
    
    def pensize(self, width=None):
        rt = self.rtu.pensize(width=width)
        return rt

    def clear(self):
        rt = self.screen.clear()
        return rt
    
    def reset(self):
        rt = self.screen.reset()
        #self.setworldcoordinates()
        return rt

    def setworldcoordinates(self,
            x_min=None, y_min=None,
            x_max=None, y_max=None):
        """ Set world coordinates
        default: x_min,y_min (lower left)
                 x_max,y_max (upper right)
        """
        if x_min is None:
            x_min= self.x_min
        if y_min is None:
            y_min= self.y_min
        if x_max is None:
            x_max= self.x_max
        if y_max is None:
            y_max= self.y_max
        
        self.screen.setworldcoordinates(x_min,y_min,
                                         x_max,y_max)
        return rt 
            
    def width(self, width=None):
        return self.pensize(width=width)

        
if __name__ == "__main__":
    import braille_display_test_2

