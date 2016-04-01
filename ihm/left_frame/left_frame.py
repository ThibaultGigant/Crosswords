# -*- coding: utf-8 -*-

try:
    from tkinter import *
except:
    from Tkinter import *

import sys
from os import getcwd
sys.path.append(getcwd())

from ihm.left_frame.grille import CellGrid
# from ihm.main_window import MainWindow


class LeftFrame(Frame):
    """
    Frame de gauche, qui comportera une grille et éventuellement des boutons
    """

    def __init__(self, master, grid):
        Frame.__init__(self, master)
        self.parent = master
        self.upper_panel = CellGrid(self, grid)
        self.lower_panel = None
        self.pack_elements()

    def pack_upper_panel(self):
        if self.upper_panel:
            self.upper_panel.pack(side=TOP, pady=30, fill=BOTH)

    def pack_lower_panel(self):
        if self.lower_panel:
            self.lower_panel.pack(side=BOTTOM, pady=10)

    def pack_elements(self):
        self.pack_upper_panel()
        self.pack_lower_panel()

    def clean_upper_panel(self):
        """
        Détruit le upper_panel pour le remplacer
        """
        if self.upper_panel:
            self.upper_panel.destroy()

    def clean_lower_panel(self):
        """
        Détruit le lower_panel pour le remplacer
        """
        if self.lower_panel:
            self.lower_panel.destroy()

    def change_grid(self, grid):
        """
        Change la grille
        """
        self.clean_upper_panel()
        self.upper_panel = CellGrid(self, grid)
        self.pack_upper_panel()

    def set_button_next(self, event):
        """
        Affiche un bouton "Next" en bas de la frame, permettant (si demandé) d'afficher itération par itération
        :param event: event à changer pour passer à l'itération suivante
        """
        self.clean_lower_panel()
        self.lower_panel = Button(self, text="Next", command=event.set)
        self.pack_lower_panel()

    def set_done_true(self):
        """
        Affiche un texte indiquant que la solution a été trouvée
        """
        self.clean_lower_panel()
        self.lower_panel = Label(self, text="Solution trouvée !")
        self.pack_lower_panel()

    def set_done_false(self):
        """
        Affiche un texte indiquant qu'aucune solution n'a été trouvée
        """
        self.clean_lower_panel()
        self.lower_panel = Label(self, text="Aucune solution trouvée :-(")
        self.pack_lower_panel()

