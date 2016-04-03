# -*- coding: utf-8 -*-

import sys, time
from os import getcwd
sys.path.append(getcwd())
from data_gestion.classes import Grid
from data_gestion.file_gestion import *


def ac3(grid):
    """
    Exécute l'algorithme AC3 sur la grille passée en paramètre
    :param grid: grille sur laquelle exécuter l'algorithme
    :type grid: Grid
    :return: False si la grille n'est pas arc consistante, True sinon
    """
    constraints = grid.constraints
    garbage_constraints = []

    while constraints:
        word1, word2, index1, index2 = constraints.pop(0)
        garbage_constraints.append((word1, word2, index1, index2))
        modif = word1.respect_binary_constraint(word2, index1, index2)
        if modif[0]:
            constraints += [cons for cons in garbage_constraints if (cons[0] == word1 or cons[1] == word1)]
        if modif[1]:
            constraints += [cons for cons in garbage_constraints if (cons[0] == word2 or cons[1] == word2)]

    return all([word.domain.cardinality() > 0 for word in grid.words])


if __name__ == '__main__':
    t = time.time()
    dico = read_dictionary(sys.argv[1])
    print("Création dico: " + str(time.time()-t) + " secondes")
    grid = read_grid(sys.argv[2], dico)

    print("Avant AC3")
    print([i.domain.cardinality() for i in grid.words])
    t = time.time()
    ac3(grid)
    print("Calcul AC3: " + str(time.time()-t) + " secondes")
    print("Après AC3")
    print([i.domain.cardinality() for i in grid.words])
