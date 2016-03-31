# -*- coding: utf-8 -*-

import sys
from os import getcwd
from copy import deepcopy
from time import time, sleep

sys.path.append(getcwd())
from data_gestion.classes import Grid, Word
from data_gestion.file_gestion import *
from algorithms.arc_consistency import ac3
from algorithms.heuristics import *


def backtrack(grid, heuristic_function, uniq=True, stop=False, mainwindow=None):
    """
    Backtracking avec forward checking
    :param grid: grille sur laquelle on lance l'algorithme
    :param heuristic_function: fonction heuristique qui détermine quel mot sera instancié à chaque itération
    :param uniq: True si un mot ne peut apparaître qu'une fois dans la grille, False sinon
    :type grid: Grid
    :type uniq: bool
    :return: Ensemble de solutions réalisables
    :rtype: bool
    """
    # On vérifie qu'il reste des mots à instancier
    # print("Nombre de mots non-instanciés : " + str(len(grid.uninstanciated_words)))
    if not grid.uninstanciated_words:
        return True

    xk = heuristic_function(grid.uninstanciated_words)  # Prochaine variable à instancier
    grid.uninstanciated_words.remove(xk)
    grid.instanciated_words.append(xk)
    words = xk.domain.list_words()
    # print("Tentative d'instanciation du mot " + str(xk.id) + " parmi les mots : " + str(words))
    if words == [""]:
        grid.uninstanciated_words.insert(0, xk)
        grid.instanciated_words.remove(xk)
        return False

    # On garde en mémoire les domaines qui pourraient être modifiés
    domains = {word: deepcopy(word.domain) for word, ind1, ind2 in xk.binary_constraints}
    domains[xk] = deepcopy(xk.domain)

    for word in words:
        # print("Instanciation de " + str(xk.id) + " à " + word)
        xk.domain = Tree(word)  # Affectation de word à la variable

        # forward check avec récupèration des mots dont les domaines ont été modifiés
        # print("Avant modification")
        # for w in domains.keys():
        #     print(str(w.id) + " : " + str(w.domain.list_words()) + str(w.domain.cardinality()))
        modif = xk.update_related_variables_domain()

        # Si on veut qu'il y ait qu'une fois un mot dans une grille,
        # il faut le retirer du domaine des autres mots de même taille
        if uniq:
            same_size_words = [w for w in grid.uninstanciated_words if w.length == xk.length]
            same_modif = []
            for w in same_size_words:
                if w.domain.remove_word(word) and w not in modif:
                    same_modif.append(w)

        if stop:
            if mainwindow:
                mainwindow.grid = grid
                mainwindow.display_grid()
            sleep(0.1)
            # input("Appuyez sur la touche ENTREE pour continuer...")

        # print("Après modification")
        # for w in domains.keys():
        #     print(str(w.id) + " : " + str(w.domain.list_words()) + str(w.domain.cardinality()))

        # Appel récursif, on vérifie que l'instanciation courante donne une solution stable
        # if any([w.domain.cardinality() == 0 for w in modif]) or not backtrack(grid, heuristic_function, uniq, stop):
        if not backtrack(grid, heuristic_function, uniq, stop, mainwindow):
            # print("Rétablissement des domaines à partir du mot " + str(xk.id))
            # rétablissement des domaines
            for w in modif:
                w.domain = deepcopy(domains[w])
            if uniq:
                for w in same_modif:
                    w.domain.add_word(word)
        else:
            return True
    # print("Retour arrière depuis " + str(xk.id))
    grid.uninstanciated_words.insert(0, xk)
    grid.instanciated_words.remove(xk)
    xk.domain = deepcopy(domains[xk])
    return False


if __name__ == '__main__':
    t1 = time()
    dico = read_dictionary(sys.argv[1])
    print("Temps de création du dictionnaire : " + str(time()-t1))
    t = time()
    grid1 = read_grid(sys.argv[2])
    grid1.set_dictionary(dico)
    print("Temps de création de la grille: " + str(time()-t))
    t = time()
    ac3(grid1)

    # res = backtrack(grid1, heuristic_max_constraints)
    # res = backtrack(grid1, heuristic_constraints_and_size, False)
    # res = backtrack(grid1, heuristic_next, True)
    # res = backtrack(grid1, heuristic_min_domain, False)
    res = backtrack(grid1, heuristic_size_and_constraints, True)

    print("Temps de calcul de l'algo : " + str(time()-t))
    print("Temps total : " + str(time()-t1))
    print(res)
    if res:
        instanciation = [(w.id, w.domain.list_words()) for w in grid1.instanciated_words]
        instanciation.sort(key=lambda x: x[0])
        print(instanciation)
