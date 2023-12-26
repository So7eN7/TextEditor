# Modules
from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import tkinter.colorchooser as cc
import os

# Main Window
win = Tk()
win.title("Untitled - Notepad")
win.geometry("800x500")
win.resizable()

# Main Frame to set our text area
frame = Frame(win)
frame.pack(pady=7)

# Scrollbar(vertical)
scroll_v = Scrollbar(frame)
scroll_v.pack(side=RIGHT, fill=Y)

# Textarea
textarea = Text(frame, width=100, height=25, font=("Arial", 17), selectbackground="cyan", selectforeground="black"
                ,undo=True, yscrollcommand=scroll_v.set)
textarea.pack()
scroll_v.config(command=textarea.yview)

win.update()
win.mainloop()