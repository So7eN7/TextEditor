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
   if new: # If ok is pressed delete everything and make a new file
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

# Save file

def saveFile():
    file = textarea.get(1.0, 'end-1c')  # Getting the inputs except the \n
    if file == "": # If file is empty show error
        file = None
        mb.showerror(title="Error", message="File cannot be empty!")
    else: # Change the title of the program and write the file
        win.title(os.path.basename(file))
        file = open(file, "w")
        file.write(textarea.get(1.0, END))
        file.close()

# Save as function

def saveAsFile():  # Open the save as window
    file = fd.asksaveasfilename(defaultextension="Untitled", initialfile="Untitled.txt",
                                filetypes=[("Text File", "*.txt*"), ("PDF", "*.pdf*")])
    if file:  # If save was successful change the title and write the file
        win.title(os.path.basename(file))
        file = open(file, "w")
        file.write(textarea.get(1.0, END))
        file.close()

# Default light theme

def lightTheme():
    textarea.config(bg="white", fg="black")

# Default dark theme

def darkTheme():
    textarea.config(bg="#0b213d", fg="white")

# Default ultra dark theme
def ultraDarkTheme():
    textarea.config(bg="black", fg="white")

# Change background color

def changeBackground():
    bg_color = cc.askcolor()
    textarea.config(bg=bg_color[1])

# Change text color

def changeForeground():
    fg_color = cc.askcolor()
    textarea.config(fg=fg_color[1])

# Change highlight color

def changeHighlight():
    highlight_color = cc.askcolor()
    textarea.config(selectbackground=highlight_color[1])

# Menubar
menubar = Menu(win)
win.config(menu=menubar)

# File menu
file_menu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=newFile)
file_menu.add_command(label="Open", command=openFile)
file_menu.add_command(label="Save", command=saveFile)
file_menu.add_command(label="Save As", command=saveAsFile)
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
appearance_menu.add_radiobutton(label="Background", variable=customize, value=1, command=changeBackground)
appearance_menu.add_radiobutton(label="Text Color", variable=customize, value=2, command=changeForeground)
appearance_menu.add_radiobutton(label="Text Highlight", variable=customize, value=3, command=changeHighlight)
appearance_menu.add_radiobutton(label="Text Font", variable=customize, value=4)
appearance_menu.add_separator()
appearance_menu.add_command(label="Light mode", command=lightTheme)
appearance_menu.add_command(label="Dark mode", command=darkTheme)
appearance_menu.add_command(label="Ultra Dark mode", command=ultraDarkTheme)

view_menu.add_cascade(menu=appearance_menu, label="Appearance")

win.update()
win.mainloop()