# Modules
from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb
import tkinter.colorchooser as cc
import tkinter.font as font
import os
from collections import deque
# Main Window
win = Tk()
win.title("Untitled - Notepad")
win.geometry("800x500")
win.resizable()

# For undo/redo
stack = deque(maxlen=17)

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

# Syntax tags

textarea.tag_configure("red", foreground="red")
textarea.tag_configure("green", foreground="green")
textarea.tag_configure("blue", foreground="blue")
textarea.tag_configure("gold", foreground="gold")
textarea.tag_configure("pink", foreground="pink")

tags = ["red", "green", "blue", "gold", "pink"]

# Syntax wordlists (for highlighting)

wordlist_python = [["import", "from", "as"],
                   ["class", "def", "for", "while","else", "elif", "if"],
                   ["int", "str", "float", "bool", "print"],
                   ["tkinter", "collections", "sys", "os", "string"],
                   ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]]

wordlist_cpp = [["#include", "#ifdef", "#pragma", "#define", "endif"],
                ["int", "void", "float", "double", "bool", "namespace", "using"],
                ["class", "template", "public", "private", "string", "protected", "virtual"],
                ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                ["NULL", "__define__"]]

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
        mb.showerror(title="Error", message="File cannot be empty!")
    else: # Change the title of the program and write the file
        win.title(os.path.basename(file))
        with open(file, "w") as f:
            f.write(textarea.get(1.0, END))
            f.close()

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

# Clear function (for undo/redo purposes)

def clear():
    textarea.delete("1.0", END)

# Stack cursor for our undo block
stack_cursor = 0

# Will stackify the deque that will hold our inputs
def stackify(stack_cursor=stack_cursor):
    stack.append(textarea.get("1.0", "end-1c"))
    if stack_cursor < 16:  # Preventing overflow
        stack_cursor += 1

# Printing the input stack in our terminal

def printStack():
    i = 0
    for s in stack:
        print(str(i) + " " + s)
        i += 1

# Undo function
def undo(stack_cursor=stack_cursor):
    clear()
    if stack_cursor > 0:  # If not empty go back (into the stack)
        stack_cursor -= 1

    textarea.insert("0.0", stack[stack_cursor])  # Insert what's left

# Redo function

def redo(stack_cursor=stack_cursor):
    clear()
    if stack_cursor < 9:  # Preventing overflow
        stack_cursor += 1

    textarea.insert("0.0", stack[stack_cursor])  # Insert what's left

# Select everything

def selectAll():
    textarea.event_generate("<<Control-Keypress-A>>")

# Print the input stack

def printWordStack():
    printStack()

# Zooming functions

def zoomIn():
    textarea.config(font=("Arial", DEFAULT_FONT_SIZE + 13))

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

def boldFont():
    textarea.config(font=("Arial", DEFAULT_FONT_SIZE, font.BOLD))

def italicFont():
    textarea.config(font=("Arial", DEFAULT_FONT_SIZE, font.ITALIC))

# Syntax Highlighting

# def defaultHighlighting():
#     textarea.config(bg="white", fg="black")

# Python highlighting

def pythonHighlighting():
    START = "1.0"  # Constants
    END = "end"
    for wordlist in wordlist_python:
        num = int(wordlist_python.index(wordlist))
        for word in wordlist:  # Finding all the keywords
            textarea.mark_set("match_start", START)
            textarea.mark_set("match_end", START)
            textarea.mark_set("search_limit", END)

            rcount = IntVar()

            while True:  # The reason that we search from match_end is to resume the search not to be stuck on one word
                index = textarea.search(word, "match_end", "search_limit", count=rcount, regexp=False)
                if index == "":
                    break
                if rcount.get() == 0:
                    break

                textarea.mark_set("match_start", index)   # Setting the colors
                textarea.mark_set("match_end", "%s+%sc" % (index, rcount.get()))
                #  percent sign is a placeholder for the index
                textarea.tag_add(tags[num], "match_start", "match_end")

# C++ highlighting

def cppHighlighting():
    START = "1.0"
    END = "end"
    for wordlist in wordlist_cpp:  # Same as above but the wordlist is changed
        num = int(wordlist_cpp.index(wordlist))
        for word in wordlist:
            textarea.mark_set("match_start", START)
            textarea.mark_set("match_end", START)
            textarea.mark_set("search_limit", END)

            rcount = IntVar()

            while True:
                index = textarea.search(word, "match_end", "search_limit", count=rcount, regexp=False)
                if index == "":
                    break
                if rcount.get() == 0:
                    break

                textarea.mark_set("match_start", index)
                textarea.mark_set("match_end", "%s+%sc" % (index, rcount.get()))

                textarea.tag_add(tags[num], "match_start", "match_end")

# Terminal launch

def launchTerminalCMD():
    #termwin = Toplevel()
    # termf = Frame(win, height=400, width=500)
    # termf.pack(fill=BOTH, expand=YES)
    # wid = termf.winfo_id()
    # os.system('cmd -into %d -geometry 40x20 -sb &' % wid)
    os.system("start cmd")

def launchTerminalPowerShell():
    os.system("start powershell")

# Although all these are barebone and WIP this one is really really WIP

def launchTerminalBash():
    os.system("start bash")

# show info

def showInfo():
    mb.showinfo(title="About TextEditor", message="Hopefully i won't forget about this and make it way better (another gui hopefully)")

# show help

def showHelp():
    commands = """
    File menu
    -----------------------
    - New = Opens a new file
    - Open = Opens a file that you choose
    - Save/Save as = Saves the file
    - Print = Will print the input stack in terminal
    - Close = Closes the file
    -----------------------
    Edit menu
    -----------------------
    - Copy = Copies the highlighted text
    - Cut = Cuts the highlighted text
    - Paste = Pastes the text from the clipboard
    - Delete = Deletes the highlighted text
    - Undo = Undo the action
    - Redo = Redo the action
    - Select-All = Select everything in the text area
    -----------------------
    View menu
    -----------------------
    - Zoom = 3 zooming options
    - Text wrap = Enables the text wrap  
    -----------------------
    Appearance menu 
    -----------------------
    - Themes = 3 modes (light - dark - ultra dark)
    - Background = Change the background color
    - Text color = Change the text color
    - Highlight color = Change the highlight color
    - Bold = Enables bold font
    - Italic = Enables italic font
    -----------------------
    Syntax Highlight menu
    -----------------------
    - Default = Default(light theme)
    - Python = Highlighting for python
    - CPP = Highlighting for C++
    -----------------------
    Terminal menu
    -----------------------
    - Launch cmd = Windows command prompt
    - Launch PowerShell = Windows powershell
    - Launch bash = Bash in cmd (might open WSL)
    -----------------------
    """

    mb.showinfo(title="Commands", message=commands)

# Show updates

def showUpdates():
    mb.showinfo(title="Upcoming", message="Bugfixes and QoL")


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
file_menu.add_command(label="Print(stack)", command=printWordStack, accelerator="(Ctrl+p)")
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
edit_menu.add_command(label="Undo", command=undo, accelerator="(Ctrl+z)")
edit_menu.add_command(label="Redo", command=redo, accelerator="(Ctrl+y)")
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
appearance_menu.add_separator()
appearance_menu.add_checkbutton(label="Bold", command=boldFont)
appearance_menu.add_checkbutton(label="Italic", command=italicFont)
appearance_menu.add_separator()
view_menu.add_cascade(menu=appearance_menu, label="Appearance")

# Syntax Highlighting menu
syntax_menu = Menu(menubar, tearoff=False)
syntax = IntVar()
syntax.set(1)
syntax_menu.add_radiobutton(label="Default", value=1, variable=syntax)
syntax_menu.add_radiobutton(label="Python", command=pythonHighlighting, value=2, variable=syntax)
syntax_menu.add_radiobutton(label="CPP", command=cppHighlighting, value=3, variable=syntax)
appearance_menu.add_cascade(menu=syntax_menu, label="Syntax Highlighting")
# Terminal menu

terminal_menu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="Terminal", menu=terminal_menu)
terminal_menu.add_command(label="Launch cmd", command=launchTerminalCMD)
terminal_menu.add_command(label="Launch PowerShell", command=launchTerminalPowerShell)
terminal_menu.add_separator()
terminal_menu.add_command(label="Launch bash", command=launchTerminalBash)

# About menu

about_menu = Menu(menubar, tearoff=False)
menubar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="Info", command=showInfo)
about_menu.add_command(label="Help", command=showHelp)
about_menu.add_separator()
about_menu.add_command(label="Updates", command=showUpdates)

# Key binds
win.bind("<<Control-Keypress-X>>", cutText)
win.bind("<<Control-Keypress-C>>", copyText)
win.bind("<<Control-Keypress-V>>", pasteText)
win.bind("<<Control-Keypress-A>>", selectAll)
win.bind("<<Control-Keypress-N>>", newFile)
win.bind("<<Control-Keypress-O>>", openFile)
win.bind("<<Control-Keypress-S>>", saveFile)
win.bind("<<Control-Keypress-P>>", printWordStack)
win.bind("<Key>", lambda event: stackify())

win.update()
win.mainloop()