from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from tkcode import CodeEditor
from screen import set_screen
from read_config import get_config
from renderer import render
# from threading import Thread
from logger import Logger

import webbrowser
import os
import shutil
import tempfile


logger = Logger()
logger.init(telemetry=get_config('logging'))
logger.log('info', 'Starting up...')
try:
    SAVED = False
    FILE_PATH = None

    root = Tk()
    root.title(get_config('app-title'))
    root.option_add("*tearOff", 0 if get_config('menubar-tearoff') is False else 1)
    menubar = Menu(root)
    run_btn_img = ImageTk.PhotoImage(Image.open('assets/run.png'))

    def run_code():
        logger.log('info', 'Running code...')
        code = str(code_editor.get(1.0, END))
        try:
            logger.log('debug', f'Code: \n\t{code}')
        except Exception as e:
            logger.log('error', f'{e}')
        global temf
        temf = os.path.join(tempfile.gettempdir(), get_config('app-title'))
        os.makedirs(temf, exist_ok=True)
        temfil = os.path.join(temf, 'index.html')
        with open(temfil, 'wb') as f:
            f.write(code.encode('utf-16'))
        render(temfil)
        shutil.rmtree(temf)
        logger.log('info', 'Code ran successfully')

    def saveas():
        global SAVED
        global FILE_PATH
        filename = filedialog.asksaveasfilename(
            defaultextension='.html',
            filetypes=[
                (get_config('file-extensions_name'),
                    get_config('file-extensions')
                ),
                ('All files', 
                '*.*',
                ),
                ],
            )
        if filename:
            with open(filename, 'wb') as f:
                f.write(code_editor.get(1.0, END).encode('utf-16'))
                SAVED = True
                root.title(get_config('app-title') + ' - ' + filename)
                FILE_PATH = filename
        else: SAVED = False

    def new():
        def new_():
            code_editor.delete(1.0, END)
        global SAVED
        if SAVED == False:
            msg = messagebox.askyesnocancel('File loss warning', 'You have unsaved changes.\nAre you sure you want to continue?')
            if msg is True:
                new_()
                SAVED = False

    def save():
        global SAVED
        global FILE_PATH
        if SAVED is False:
            saveas()
        else:
            code = code_editor.get(1.0, END)
            with open(FILE_PATH, 'wb') as f:
                f.write(code.encode('utf-16'))

    def open_file():
        def open_f():
            global FILE_PATH
            filename = filedialog.askopenfilename(
            defaultextension='.html',
            filetypes=[
                (get_config('file-extensions_name'),
                    get_config('file-extensions')
                    ),
                ('All files', '*.*')
            ]
            
        )
            code_editor.delete(1.0, END)
            with open(filename, 'rb') as f:
                code_editor.insert(1.0, f.read().decode('utf-16'))
                root.title(get_config('app-title') + ' - ' + filename)
                FILE_PATH = filename
        global SAVED
        global FILE_PATH
        if SAVED is False:
            a = messagebox.askyesnocancel('File loss warning', 'You have unsaved changes.\nAre you sure you want to continue?')
            if a is True:
                open_f()
        elif SAVED is True:
            open_f()

    def close():
        global FILE_PATH
        global SAVED
        if SAVED is False:
            msg = messagebox.askyesnocancel('File loss warning', 'You have unsaved changes.\nAre you sure you want to exit?')
            if msg is True:
                root.destroy()
            
        elif SAVED is True:
            root.destroy()

    file_menu = Menu(menubar)
    file_menu.add_command(label="New", command=new)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save)
    file_menu.add_command(label="Save as", command=saveas)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=close)

    help_menu = Menu(menubar)
    help_menu.add_command(label="Help", command=lambda: webbrowser.open('https://github.com/Griphitor'))
    help_menu.add_command(label="About", command=lambda: webbrowser.open('https://github.com/Griphitor/Griphitor-Rewrite/blob/Master/README.md'))
    help_menu.add_command(label="Report a bug", command=lambda: webbrowser.open('https://github.com/Griphitor/Griphitor-Rewrite/issues/new?assignees=Advik-B&labels=bug&template=bug_report.md'))
    help_menu.add_command(label="Suggest a feature", command=lambda: webbrowser.open('https://github.com/Griphitor/Griphitor-Rewrite/issues/new?assignees=&labels=enhancement&template=feature_request.md'))

    # menubar.add_cascade(label="File", menu=file_menu)
    # menubar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menubar)

    code_editor = CodeEditor(root)
    # code_editor.pack(fill=BOTH, expand=1)

    menubar.add_cascade(menu=file_menu, label="File")
    menubar.add_cascade(menu=help_menu, label="Help")

    root.iconbitmap(get_config('app-icon'))
    root.config(menu=menubar)
    screen_width = int((root.winfo_screenwidth() * .2) // 2)
    screen_height = int((root.winfo_height() * .2) // 2)
    logger.log('info', 'Screen width: ' + str(screen_width))
    logger.log('info', 'Screen width: ' + str(screen_width))
    themes = get_config('themes')
    logger.log('debug', 'Themes: ' + str(themes))
    error = None
    for theme in themes:
        if get_config('theme').__add__('.json') == theme.split('/')[-1]:
            theme_name = theme
    try:
        logger.log('debug', 'Using theme: %s from %s' % (theme_name.split('/')[-1], theme_name))
    except NameError:
        error = 1

    if error == 1:
        raise ValueError('The theme %s is not found' % get_config('theme'))
    code_editor = CodeEditor(

        root,
        width=int((screen_width // 2) * 1.15),
        height=screen_height,
        language="html",
        highlighter=theme_name,
        autofocus=True,
        blockcursor=get_config('block-cursor'),
        insertofftime=0,
        padx=10,
        pady=10,
        font=[get_config('code_font'), get_config('code_font_size')],)

    botton_frame = LabelFrame(root, background='red', width=screen_width)
    run_btn = ttk.Button(
        botton_frame,
        text="Run",
        command=run_code,
        compound=RIGHT,
        )

    code_editor.grid(row=0, column=0, sticky="nsew")
    botton_frame.grid(row=1, column=0, sticky="w", pady=10)
    run_btn.pack()

    root.update()
    set_screen(root, width_ofset=.72, height_ofset=.62)
    root.mainloop()
except Exception as e:
    logger.log('error', 'Error: ' + str(e))

finally:
    logger.log('debug', 'Exiting')
    logger.quit()