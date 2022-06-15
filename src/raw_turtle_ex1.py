import tkinter
from turtle import RawTurtle

class MyApp():

    def __init__(self, parent):
        self.p = parent
        self.f = tkinter.Frame(self.p).pack()
        self.c = tkinter.Canvas(self.f, height=640, width=1000)
        self.c.pack()
        self.t = RawTurtle(self.c, shape='square', visible=False)
        self.main(5)

    def main(self, size):
        self.t.size = size  # does nothing if stamping with pen up
        self.t.penup()
        self.t.shapesize(5, 1.5, 2)
        self.t.fillcolor('black')  # the default
        self.t.stamp()

if __name__ == '__main__':
    root = tkinter.Tk()
    frame = MyApp(root)
    root.mainloop()