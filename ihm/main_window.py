# -*- coding: utf-8 -*-

try:
    from tkinter import *
except:
    from Tkinter import *

import sys
from os import getcwd
sys.path.append(getcwd())

from data_gestion.classes import Grid
from ihm.left_frame.left_frame import LeftFrame
from ihm.right_frame import RightFrame


class MainWindow(Frame):
    """
    Classe qui contiendra la fenêtre principale
    """
    def __init__(self, master, grid=None):
        Frame.__init__(self, master)
        self.parent = master
        self.grid = grid  # type: Grid
        self.left_frame = None  # type: LeftFrame
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
        if self.grid and not self.left_frame:
            self.set_left_frame(LeftFrame(self, self.grid))
        elif self.grid and self.left_frame:
            self.left_frame.change_grid(self.grid)

    def update_grid(self):
        """
        Met à jour la grille en fonction des modifications
        """
        self.left_frame.upper_panel.update_words()

    def display_done(self, done):
        """
        Affiche dans le panneau gauche le résultat de l'algorithme : solution trouvée ou pas
        """
        if self.left_frame:
            if done:
                self.left_frame.set_done_true()
            else:
                self.left_frame.set_done_false()

    def clean_left_result(self):
        """
        Efface le résultat précédent du panneau gauche
        """
        self.left_frame.clean_lower_panel()

    def clean_left_frame(self):
        """
        Efface le panneau gauche
        """
        self.grid = None
        self.set_left_frame(None)


def launch():
    root = Tk()
    root.title("Crosswords CSP")
    # root.resizable(width=False, height=False)

    main_window = MainWindow(root)
    main_window.pack()

    root.mainloop()


if __name__ == '__main__':
    launch()
