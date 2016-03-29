# -*- coding: utf-8 -*-

try:
    from tkinter import *
except:
    from Tkinter import *

import sys
from os import getcwd
sys.path.append(getcwd())

# from ihm.right_frame import RightFrame


class MenuPersistant(Frame):
    """
    Menu qui sera toujours présent en bas à droite
    """
    def __init__(self, master):
        Frame.__init__(self, master, borderwidth=2, relief=RIDGE)
        self.parent = master  # type: RightFrame
        self.choice_buttons()

    def choice_buttons(self):
        """
        Affiche les boutons permettant de choisir l'action à réaliser au départ :
        ouvrir un fichier, créer une grille, ou faire des statistiques
        Ce sera le menu principal...
        """
        open_button = Button(self, text="Ouvrir une grille existante", command=self.parent.parent.loaded_grid)
        create_button = Button(self, text="Générer une grille", command=self.parent.choix_generer)
        stats_button = Button(self, text="Faire des statistiques")
        open_button.pack()
        create_button.pack()
        stats_button.pack()
