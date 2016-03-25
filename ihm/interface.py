# -*- coding: utf-8 -*-

try:
    from tkinter import *
except:
    from Tkinter import *
import sys

cell_size = 30
colors = {0: "white", 1: "black"}


class CellGrid(Canvas):
    def __init__(self, master, ligne, colonne, taille, Grille):
        Canvas.__init__(self, master, width=taille * colonne, height=taille * ligne)
        self.taille = taille
        self.grid = []
        for l in range(ligne):
            line = []
            for col in range(colonne):
                line.append(Cell(self, col, l, taille, Grille[l][col]))
            self.grid.append(line)
        self.draw()

    def draw(self):
        for l in self.grid:
            for cell in l:
                cell.draw()


class Cell():
    def __init__(self, master, x, y, size, value):
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.fill = "white"
        self.value = value

    def setValue(self, value):
        self.value = value

    def draw(self):
        if self.master != None:
            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size
            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill=colors[int(self.value)], outline="gray")


def grille(root, G):
    resGrille = CellGrid(root, len(G), len(G[0]), cell_size, G)
    resGrille.pack()
    resGrille.update()
    # resGrille.postscript(file="grille.ps", colormode='color')
    Label(root, text="\n").pack()
    # b1=Button(root, text="Afficher parcours", width=20, command=lambda:chemin(root,D1,D2,F1,F2,direction,resGrille,C))
    # b1.pack()
    Label(root, text="\n").pack()


def read_file(file_name):
    """
    Lit un fichier texte contenant une grille à compléter
    :param file_name: chemin relatif du fichier contenant la grille
    :type file_name: str
    """
    try:
        fp = open(file_name, "r")
    except:
        raise IOError("File not found")

    # récupération des données sur la largeur et la hauteur de la grille
    width, height = list(map(int, fp.readline().split()))

    # récupération de la grille à proprement parler
    grid = []
    for i in range(height):
        line = fp.readline().split()
        if len(line) != width:
            raise IOError("Wrong file format: wrong number of items in a line")
        else:
            grid.append(line)

    fp.close()
    return width, height, grid


if __name__ == '__main__':
    M, N, G, = read_file(sys.argv[1])
    root = Tk()
    grille(root, G)
    root.mainloop()
