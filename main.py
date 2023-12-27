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
frame.pack()

# Scrollbar(vertical)
scroll_v = Scrollbar(frame)
scroll_v.pack(side=RIGHT, fill=Y)

# Textarea
textarea = Text(frame, width=100, height=25, font=("Arial", 17), selectbackground="cyan", selectforeground="black"
                ,undo=True, yscrollcommand=scroll_v.set)
textarea.pack()
scroll_v.config(command=textarea.yview)

# Functionality

# Close the program
def closeApp():
    win.destroy()

# New file
def newFile():
   new = mb.askyesno(title="Are you sure?", message="Make sure to save the file before proceeding!")
   if new:
       win.title("Untitled - Notepad")
       textarea.delete(1.0, END)
   else:
       pass

# Open file
def openFile(): # Support for basically everything
   file = fd.askopenfilename(defaultextension='.txt', filetypes=[('All Files', '*.*'), ("Text File", "*.txt*")])
   if file != '': # If not null choose the opened file name as the title
       win.title(os.path.basename(file))
       textarea.delete(1.0, END)
       with open(file, "r") as file_: # Insert the contents of the file
           textarea.insert(1.0, file_.read())
           file_.close()
   else:
       file = None

# Menubar
menubar = Menu(win)
win.config(menu=menubar)

# File menu
file_menu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=newFile)
file_menu.add_command(label="Open", command=openFile)
file_menu.add_command(label="Save")
file_menu.add_command(label="Save As")
file_menu.add_separator()
file_menu.add_command(label="Print")
file_menu.add_separator()
file_menu.add_command(label="Close", command=closeApp)

# Edit menu
edit_menu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Cut")
edit_menu.add_command(label="Paste")
edit_menu.add_command(label="Delete")
edit_menu.add_separator()
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")
edit_menu.add_separator()
edit_menu.add_command(label="Select All")

# View menu
view_menu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Zoom")
view_menu.add_separator()

# Appearance menu
appearance_menu = Menu(menubar, tearoff=False)
customize = IntVar()
customize.set(1)
appearance_menu.add_radiobutton(label="Background", variable=customize, value=1)
appearance_menu.add_radiobutton(label="Text Color", variable=customize, value=2)
appearance_menu.add_radiobutton(label="Text Font", variable=customize, value=3)

view_menu.add_cascade(menu=appearance_menu, label="Appearance")

win.update()
win.mainloop()