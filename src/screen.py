#!bin/env python3

__author__ = 'Advik Bommu'
__version__ = '1.0.0'

from tkinter import Tk
def set_screen(master: Tk, height_ofset: float=.6, width_ofset: float=.5) -> None:

    screen_width = master.winfo_screenwidth()
    screen_height = master.winfo_screenheight()

    app_height = int(screen_height * height_ofset)
    app_width = int(screen_width * width_ofset)
    app_gm_1 = int(screen_width * .25)
    app_gm_2 = int(screen_height * .1)
    master.geometry(f'{app_width}x{app_height}+{app_gm_1}+{app_gm_2}')