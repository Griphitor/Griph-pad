from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkcode import CodeEditor
from screen import set_screen
from read_config import get_config
from renderer import render
from threading import Thread

import os
import shutil
import tempfile

root = Tk()
root.title(get_config('app-title'))
root.option_add("*tearOff", 0 if get_config('menubar-tearoff') is False else 1)

menubar = Menu(root)

def run_code():
    code = code_editor.get(1.0, END)
    global temf
    temf = os.path.join(tempfile.gettempdir(), get_config('app-title'))
    os.makedirs(temf, exist_ok=True)
    temfil = os.path.join(temf, 'index.html')
    with open(temfil, 'w+') as f:
        f.write(code)
    render(temfil)
    shutil.rmtree(temf)
    

    
file_menu = Menu(menubar)
file_menu.add_command(label="New")
file_menu.add_command(label="Open")
file_menu.add_command(label="Save")
file_menu.add_command(label="Save as")
file_menu.add_separator()
file_menu.add_command(label="Exit")

help_menu = Menu(menubar)
help_menu.add_command(label="Help")
help_menu.add_command(label="About")
run_btn = Button(root, text="Run", command=run_code)

menubar.add_cascade(menu=file_menu, label="File")
menubar.add_cascade(menu=help_menu, label="Help")

root.iconbitmap(get_config('app-icon'))
root.config(menu=menubar)
screen_width = int(root.winfo_screenwidth() * .1)
screen_height = int(root.winfo_height() * .1)
code_editor = CodeEditor(

    root,
    width=screen_width,
    height=10,
    language="html",
    highlighter=get_config('theme'),
    autofocus=True,
    blockcursor=False,
    insertofftime=0,
    padx=10,
    pady=10,
    font=[get_config('code_font'), get_config('code_font_size')],
)

code_editor.grid(row=0, column=0, sticky="nsew")
run_btn.grid(row=1, column=0, sticky="w")

root.update()
set_screen(root)
root.mainloop()
