# -*- coding: utf-8 -*-

try:
    from tkinter import *
except:
    from Tkinter import *

import sys
from os import getcwd
sys.path.append(getcwd())

from data_gestion.classes import Grid
from ihm.grille import CellGrid
from ihm.right_frame import RightFrame


class MainWindow(Frame):
    """
    Classe qui contiendra la fenêtre principale
    """
    def __init__(self, master, grid=None):
        Frame.__init__(self, master)
        self.parent = master
        self.grid = grid  # type: Grid
        self.left_frame = None
        self.right_frame = RightFrame(self)
        self.pack_elements()

    def pack_left_frame(self):
        if self.left_frame:
            self.left_frame.pack(side=LEFT)

    def pack_right_frame(self):
        if self.right_frame:
            self.right_frame.pack(side=RIGHT)

    def pack_elements(self):
        self.pack_left_frame()
        self.pack_right_frame()

    def set_left_frame(self, frame):
        """
        Permet le changement de la partie gauche de la fenêtre
        :param frame: widget à placer à la place du panneau gauche
        """
        if self.left_frame:
            self.left_frame.destroy()
        self.left_frame = frame
        self.pack_left_frame()

    def display_grid(self):
        """
        Affiche la grille en attribut dans le panneau gauche et les options correspondantes dans le panneau droit
        """
        if self.grid:
            self.set_left_frame(CellGrid(self, self.grid))
        # self.right_frame.set_to_loaded_grid()


def launch():
    root = Tk()
    # root.resizable(width=False, height=False)

    main_window = MainWindow(root)
    main_window.pack()

    root.mainloop()


if __name__ == '__main__':
    launch()
