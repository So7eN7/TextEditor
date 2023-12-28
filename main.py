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

# Scrollbar(horizontal)
scroll_h = Scrollbar(frame, orient="horizontal")
scroll_h.pack(side=BOTTOM, fill=X)

# Textarea
DEFAULT_FONT_SIZE = 17
TEXT_WRAP = "none"
textarea = Text(frame, width=100, height=25, font=("Arial", DEFAULT_FONT_SIZE), selectbackground="cyan", selectforeground="black"
            ,undo=True, yscrollcommand=scroll_v.set, wrap=TEXT_WRAP)
textarea.pack()
scroll_v.config(command=textarea.yview)
scroll_h.config(command=textarea.xview)

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

# Cutting text function

# Selected text
global selection

def cutText():
    #textarea.event_generate("<<Cut>>")

    if textarea.selection_get():
        selection = textarea.selection_get()
        textarea.delete("sel.first", "sel.last")  # Deleting text and adding it unto the clipboard
        win.clipboard_clear()
        win.clipboard_append(selection)

# Copying text function

def copyText():
    #textarea.event_generate("<<Copy>>")
    if textarea.selection_get():
        selection = textarea.selection_get()  # Putting the text unto the clipboard
        win.clipboard_clear()
        win.clipboard_append(selection)

# Pasting text function

def pasteText():
    #textarea.event_generate("<<Paste>>")
    if selection:
        position = textarea.index(INSERT)
        textarea.insert(position, selection)  # Insert the text at the position of the cursor (after click)

# Select everything

def selectAll():
    textarea.event_generate("<<Control-Keypress-A>>")

# Print file

def printFile():
    textarea.event_generate("<<Control-Keypress-P>>")

# Zooming functions

def zoomIn():
    textarea.config(font=("Arial", DEFAULT_FONT_SIZE + 5))

def defaultZoom():
    textarea.config(font=("Arial", DEFAULT_FONT_SIZE))

def zoomOut():
    textarea.config(font=("Arial", DEFAULT_FONT_SIZE - 5))

def textWrap():
    TEXT_WRAP = WORD
    textarea.config(wrap=TEXT_WRAP)

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

# Terminal launch

def launchTerminal():
    #termwin = Toplevel()
    termf = Frame(win, height=400, width=500)
    termf.pack(fill=BOTH, expand=YES)
    wid = termf.winfo_id()
    os.system('cmd -into %d -geometry 40x20 -sb &' % wid)

# Menubar
menubar = Menu(win)
win.config(menu=menubar)

# File menu
file_menu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=newFile, accelerator="(Ctrl+n)")
file_menu.add_command(label="Open", command=openFile, accelerator="(Ctrl+o)")
file_menu.add_command(label="Save", command=saveFile, accelerator="(Ctrl+s)")
file_menu.add_command(label="Save As", command=saveAsFile, accelerator="(Ctrl+a+s)")
file_menu.add_separator()
file_menu.add_command(label="Print", command=printFile, accelerator="(Ctrl+p)")
file_menu.add_separator()
file_menu.add_command(label="Close", command=closeApp)

# Edit menu
edit_menu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Copy", command=copyText, accelerator="(Ctrl+c)")
edit_menu.add_command(label="Cut", command=cutText, accelerator="(Ctrl+x)")
edit_menu.add_command(label="Paste", command=pasteText, accelerator="(Ctrl+v)")
edit_menu.add_command(label="Delete")
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=textarea.edit_undo, accelerator="(Ctrl+z)")
edit_menu.add_command(label="Redo", command=textarea.edit_redo, accelerator="(Ctrl+y)")
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=selectAll, accelerator="(Ctrl+a)")

# View menu
view_menu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Zoom in", command=zoomIn)
view_menu.add_command(label="Default zoom", command=defaultZoom)
view_menu.add_command(label="Zoom out", command=zoomOut)
view_menu.add_separator()
view_menu.add_checkbutton(label="Text Wrap", command=textWrap)
view_menu.add_separator()
view_menu.add_command(label="Terminal", command=launchTerminal)
view_menu.add_separator()
# Appearance menu
appearance_menu = Menu(menubar, tearoff=False)
customize = IntVar()
customize.set(1)
appearance_menu.add_command(label="Background", command=changeBackground)
appearance_menu.add_command(label="Text Color", command=changeForeground)
appearance_menu.add_command(label="Text Highlight", command=changeHighlight)
appearance_menu.add_separator()
appearance_menu.add_radiobutton(label="Light mode", command=lightTheme, value=1, variable=customize)
appearance_menu.add_radiobutton(label="Dark mode", command=darkTheme, value=2, variable=customize)
appearance_menu.add_radiobutton(label="Ultra Dark mode", command=ultraDarkTheme, value=3, variable=customize)

view_menu.add_cascade(menu=appearance_menu, label="Appearance")

# Key binds
win.bind("<<Control-Keypress-X>>", cutText)
win.bind("<<Control-Keypress-C>>", copyText)
win.bind("<<Control-Keypress-V>>", pasteText)
win.bind("<<Control-Keypress-A>>", selectAll)
win.bind("<<Control-Keypress-N>>", newFile)
win.bind("<<Control-Keypress-O>>", openFile)
win.bind("<<Control-Keypress-S>>", saveFile)
win.bind("<<Control-Keypress-P>>", printFile)

win.update()
win.mainloop()