# -*- coding: utf-8 -*-

from time import time
import sys
from data_gestion.file_gestion import read_dictionary, read_grid
from algorithms.arc_consistency import ac3
from copy import deepcopy
from algorithms import rac, rac2
from ihm.main_window import launch

from tkinter import *


def test_rapidite_rac1et2():
    dico = read_dictionary(sys.argv[1])
    print("Dictionnaire créé : ")
    t = time()
    grid1 = read_grid(sys.argv[2], dico)
    ac3(grid1)
    print("Temps de création de la grille: " + str(time()-t))

    times1 = []
    for i in range(10):
        print("Itération " + str(i))
        grid = deepcopy(grid1)
        V = grid.words
        t = time()
        # print(V)
        # res = backtrack(V[:], heuristic_max_constraints)
        # res = backtrack(V[:], heuristic_constraints_and_size, False)
        res = rac.backtrack(V[:], rac.heuristic_next, True)
        # res = backtrack(V[:], heuristic_min_domain, False)
        # res = backtrack(V[:], heuristic_size_and_constraints, True)
        times1.append(time()-t)
        print("Temps de calcul de l'algo : " + str(time()-t))
        print(res)

    times2 = []
    for i in range(10):
        print("Itération " + str(i))
        grid = deepcopy(grid1)
        t = time()
        # print(V)
        # res = backtrack(V[:], heuristic_max_constraints)
        # res = backtrack(V[:], heuristic_constraints_and_size, False)
        res = rac2.backtrack(grid, rac2.heuristic_next, True)
        # res = backtrack(V[:], heuristic_min_domain, False)
        # res = backtrack(V[:], heuristic_size_and_constraints, True)
        times2.append(time()-t)
        print("Temps de calcul de l'algo : " + str(time()-t))
        print(res)

    print("Temps pris par l'algo 1 : " + str(sum(times1)))
    print("Temps pris par l'algo 2 : " + str(sum(times2)))


if __name__ == '__main__':
    launch()
