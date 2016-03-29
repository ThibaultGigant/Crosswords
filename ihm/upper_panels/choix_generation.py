# -*- coding: utf-8 -*-

try:
    from tkinter import *
except:
    from Tkinter import *

import sys
from os import getcwd
sys.path.append(getcwd())
from data_gestion.generation import generate_random_grid
from data_gestion.classes import Grid


class ChoixGeneration(Frame):
    """
    Widgets liés aux possibilités pour la génération d'une grille
    """
    def __init__(self, master):
        Frame.__init__(self, master)
        self.parent = master
        # Variables nécessaires à la génération
        self.width_var = IntVar()
        self.height_var = IntVar()
        self.densite_var = IntVar()  # la densité sera en pourcent, donc Int suffit

        self.choice_buttons()

    def choice_buttons(self):
        """
        Affiche les boutons permettant de choisir les caractéristiques de la grille à générer
        """
        # Déclaration des variables

        self.width_var.set(10)
        self.height_var.set(10)
        self.densite_var.set(20)

        # Déclaration des widgets
        label_caracteristiques = Label(self, text="Caractéristiques de la grille à générer :")
        label_largeur = Label(self, text="Largeur :")
        scale_largeur = Scale(self, from_=2, to=30, orient=HORIZONTAL, length=200, showvalue=0, variable=self.width_var)
        spinbox_largeur = Spinbox(self, from_=2, to=30, state="readonly", width=3, textvariable=self.width_var)
        label_hauteur = Label(self, text="Hauteur :")
        scale_hauteur = Scale(self, from_=2, to=30, orient=HORIZONTAL, length=200, showvalue=0, variable=self.height_var)
        spinbox_hauteur = Spinbox(self, from_=2, to=30, state="readonly", width=3, textvariable=self.height_var)
        label_densite = Label(self, text="Densité (en %) :")
        scale_densite = Scale(self, from_=0, to=100, orient=HORIZONTAL, length=200, showvalue=0, variable=self.densite_var)
        spinbox_densite = Spinbox(self, from_=0, to=100, state="readonly", width=3, textvariable=self.densite_var)
        button_generer = Button(self, text="Générer la grille", command=self.generer)

        # Placement des widgets
        label_caracteristiques.grid(row=0, column=0, columnspan=3)
        label_largeur.grid(row=1, column=0, sticky=E)
        scale_largeur.grid(row=1, column=1)
        spinbox_largeur.grid(row=1, column=2)
        label_hauteur.grid(row=2, column=0, sticky=E)
        scale_hauteur.grid(row=2, column=1)
        spinbox_hauteur.grid(row=2, column=2)
        label_densite.grid(row=3, column=0, sticky=E)
        scale_densite.grid(row=3, column=1)
        spinbox_densite.grid(row=3, column=2)
        button_generer.grid(row=4, column=0, columnspan=3)

    def generer(self):
        """
        Génère une grille et la fait afficher par la main window
        """
        grid = generate_random_grid(self.width_var.get(), self.height_var.get(), self.densite_var.get()/100.0)
        self.parent.parent.grid = Grid(grid)
        self.parent.parent.loaded_grid()

