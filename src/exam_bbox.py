#exam_bbox.py    12Jun2022
import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, width=400, height=400, background='white')
canvas.pack(fill="both", expand=True)

canvas.create_oval(10, 10, 50, 50, fill="red")
canvas.create_oval(30, 20, 80, 90, fill="blue")

bbox = canvas.bbox("all")
canvas.create_rectangle(bbox, outline="black")

root.mainloop()
