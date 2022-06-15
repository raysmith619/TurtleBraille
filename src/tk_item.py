#tk_item.py
# Test generic item creation
import tkinter as tk
from select_trace import SlTrace

def get_tk_create_args(canvas, item_id):
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
    
def create_multi(canvas, sep_xy, itemType, *args, **kw):
    """ Create multiple items with separation
    This is a test to see if we can create a generic
    item creation given the item tag
    :sep_xy: separation x,y
    :itemType: tk Canvas item type string
    :args: positional args
    :kw: keyword args
    :returns: (tag1,tag2)
    """
    tag1 = canvas._create(itemType, args, kw)
    (itemType_2, args_2, kw_2) = get_tk_create_args(cv, tag1)
    for i in range(len(args_2)):
        if i%2==0:
            args_2[i] += sep_xy[0]      # Do separation
        else:
            args_2[1] += sep_xy[1]        
    tag2 = canvas._create(itemType_2, args_2, kw_2)
    return tag2, tag2

mw = tk.Tk()
cv = tk.Canvas(mw)
cv.pack()

rec = create_multi(cv, (20,50), "arc", 10,20,110,120, fill="red")
bitm = create_multi(cv, (20,50), "bitmap", 400,400, background="gray")
imag = create_multi(cv, (20,50), "image", 400,400)
line = create_multi(cv, (30,60), "line", 10,20,110,120, fill="orange",width=10)
oval = create_multi(cv, (50,100), "oval", 10,20,110,120, fill="yellow",width=10)
poly = create_multi(cv, (50,100), "polygon", 5,10,25,30,45,50,55,60,60,65,
                     fill="green",width=3)
rec = create_multi(cv, (20,50), "rectangle", 10,20,110,120, fill="red")
text = create_multi(cv, (20,50), "text", 200,200, fill="red", text="hello")
win = create_multi(cv, (20,50), "window", 200,200, height=50, width=100, state="normal")

# Test get_tk_create_args
cv_item_tags = cv.find_all()
for tag in cv_item_tags:
    itemType, args, kw = get_tk_create_args(cv, tag)
    SlTrace.lg(f"{tag:3}: type: {itemType} args:{args}")
    SlTrace.lg(f"    {kw}")
    
mw.mainloop()
