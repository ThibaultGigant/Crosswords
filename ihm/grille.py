# -*- coding: utf-8 -*-

try:
    from tkinter import *
except:
    from Tkinter import *

import sys
from os import getcwd

sys.path.append(getcwd())
from data_gestion.file_gestion import read_dictionary, read_grid
from data_gestion.classes import Grid

cell_size = 30
colors = {0: "white", 1: "black"}


class CellGrid(Canvas):
    """
    Classe pour l'affichage de la grille entière
    """
    def __init__(self, master, nb_lignes, nb_colonnes, taille, Grille):
        Canvas.__init__(self, master, width=taille * (nb_colonnes + 2), height=taille * (nb_lignes + 2))
        self.parent = master
        self.taille = taille
        self.grid = []
        self.creation_cellules(nb_lignes, nb_colonnes, Grille)
        self.draw()
        self.config(scrollregion=[0, 0, taille * (nb_colonnes + 2), taille * (nb_lignes + 2)])

    def creation_cellules(self, nb_lignes, nb_colonnes, Grille):
        for l in range(nb_lignes):
            line = []
            for col in range(nb_colonnes):
                line.append(Cell(self, col, l, Grille[l][col]))
            self.grid.append(line)

    def draw(self):
        for l in self.grid:
            for cell in l:
                cell.draw()
        self.scale(ALL, -1, -1, cell_size, cell_size)


class Cell:
    """
    Classe qui affiche une cellule de la grille aux coordonnées voulues avec la valeur voulue
    """
    def __init__(self, master, x, y, value):
        self.master = master  # type: CellGrid
        self.abs = x
        self.ord = y
        self.fill = "black" if value == "1" else "white"
        self.value = value

    def set_value(self, value):
        self.value = value
        self.draw()

    def draw(self):
        if self.master is not None:
            xmin = self.abs
            xmax = xmin + 1
            ymin = self.ord
            ymax = ymin + 1
            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=self.fill, outline="gray")
            if self.value not in ["0", "1"]:
                self.master.create_text(self.abs + 1/2, self.ord + 1/2, text=self.value)


def grille(root, G):
    """
    Crée la grille à afficher
    :param root: parent de la grille, la fenêtre principale
    :param G: grille
    :type G: Grid
    :return: Widget contenant la grille
    :rtype: CellGrid
    """
    return CellGrid(root, G.get_height(), G.get_width(), cell_size, G.grid)


if __name__ == '__main__':
    dico = read_dictionary(sys.argv[1])
    grid = read_grid(sys.argv[2], dico)
    root = Tk()

    # Affichage en plein écran (décommenter si besoin)
    # w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    # root.geometry("%dx%d+0+0" % (w, h))
    grille = grille(root, grid)
    grille.pack()
    grille.update()

    root.mainloop()
