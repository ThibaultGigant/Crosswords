# -*- coding: utf-8 -*-

try:
    from tkinter import *
except:
    from Tkinter import *

import sys
from os import getcwd
sys.path.append(getcwd())

from ihm.menu_persistant import MenuPersistant
from ihm.upper_panels.choix_algo import ChoixAlgo
from ihm.upper_panels.choix_generation import ChoixGeneration
from ihm.upper_panels.solving import SolvingButtons
from ihm.upper_panels.choix_bnb import ChoixBnB


class RightFrame(Frame):
    """
    Frame de droite, qui comportera un panneau changeant et un panneau persistant
    """

    def __init__(self, master):
        Frame.__init__(self, master)
        self.parent = master
        self.upper_panel = None
        self.lower_panel = MenuPersistant(self)
        self.pack_elements()

    def pack_upper_panel(self):
        if self.upper_panel:
            self.upper_panel.pack(side=TOP, padx=10, pady=30)

    def pack_lower_panel(self):
        if self.lower_panel:
            self.lower_panel.pack(side=BOTTOM, pady=10, padx=10, fill=X)

    def pack_elements(self):
        self.pack_upper_panel()
        self.pack_lower_panel()

    def clean_upper_panel(self):
        """
        Détruit le upper_panel pour le remplacer
        """
        if self.upper_panel:
            self.upper_panel.destroy()

    def set_to_loaded_grid(self):
        """
        Change le panneau droit pour qu'il corresponde aux options pour une grille pré-chargée
        """
        self.clean_upper_panel()
        self.upper_panel = ChoixAlgo(self)
        if self.parent.left_frame:
            self.parent.left_frame.clean_lower_panel()
        self.pack_upper_panel()

    def choix_generer(self):
        """
        Affiche dans le panneau supérieur les options nécessaires à la génération d'une grille
        """
        self.clean_upper_panel()
        self.parent.clean_left_frame()
        self.upper_panel = ChoixGeneration(self)
        self.pack_upper_panel()

    def choix_bnb(self):
        """
        Affiche dans le panneau supérieur les options pour le Branch & Bound
        """
        self.clean_upper_panel()
        self.upper_panel = ChoixBnB(self)
        if self.parent.left_frame:
            self.parent.left_frame.clean_lower_panel()
        self.pack_upper_panel()

    def set_to_solving(self, event):
        """
        Affiche dans le panneau de droite les widgets pendant la résolution d'une grille
        """
        self.clean_upper_panel()
        self.upper_panel = SolvingButtons(self, event)
        self.pack_upper_panel()

    def set_to_solving_bnb(self):
        """
        Affiche dans le panneau de droite une demande d'attente de la part de l'utilisateur pendant l'exécution du B&B
        """
        self.clean_upper_panel()
        self.upper_panel = Frame(self)
        label = Label(self.upper_panel, text="Veuillez patienter, le calcul de la solution s'effectue)")
        label.pack()
        self.pack_upper_panel()

    def set_to_solved_bnb(self, solved):
        """
        Affiche dans le panneau de droite si un résultat a été trouvé lors de l'exécution du B&B
        """
        self.clean_upper_panel()
        self.upper_panel = Frame(self)
        if solved:
            label = Label(self.upper_panel, text="Solution Trouvée !")
        else:
            label = Label(self.upper_panel, text="Aucune solution trouvée :-(")
        label.pack()
        self.pack_upper_panel()

