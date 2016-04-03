# -*- coding: utf-8 -*-

import sys
from os import getcwd
from os.path import join
from time import time, sleep

sys.path.append(getcwd())
from data_gestion.classes import Grid, deepcopy
from data_gestion.file_gestion import *
from algorithms.arc_consistency import ac3
from algorithms.heuristics import *


def backtrack(grid, heuristic_function, uniq=True, stop=None, mainwindow=None, first_call=True):
    """
    Backtracking avec forward checking
    :param grid: grille sur laquelle on lance l'algorithme
    :param heuristic_function: fonction heuristique qui détermine quel mot sera instancié à chaque itération
    :param uniq: True si un mot ne peut apparaître qu'une fois dans la grille, False sinon
    :param stop: threading.Event qui permet d'arrêter le processus à chaque itération
    :param mainwindow: Fenêtre principale, permettant d'accéder au panneau gauche et afficher la grille
    :param first_call: True si c'est l'appel de départ ou non, sert surtout à renvoyer un affichage particulier si on trouve une solution ou non
    :type grid: Grid
    :type uniq: bool
    :return: Ensemble de solutions réalisables
    :rtype: bool
    """
    # On vérifie qu'il reste des mots à instancier, sinon on a trouvé une solution
    if not grid.uninstanciated_words:
        # Affichage graphique
        if mainwindow:
            mainwindow.display_grid()
            sleep(0.1)
            mainwindow.display_done(True)
        return True

    # Pour le stepbystep c'est plus "pratique"
    if first_call:
        # Affichage si demandé
        if mainwindow:
            # mainwindow.grid = grid
            mainwindow.display_grid()
            sleep(0.1)
        if stop:
            stop.wait()
            stop.clear()

    xk = heuristic_function(grid.uninstanciated_words)  # Prochaine variable à instancier
    grid.uninstanciated_words.remove(xk)
    grid.instanciated_words.append(xk)
    words = xk.domain.list_words()
    # print("Tentative d'instanciation du mot " + str(xk.id) + " parmi les mots : " + str(words))
    if words == [""]:
        grid.uninstanciated_words.insert(0, xk)
        grid.instanciated_words.remove(xk)
        if first_call and mainwindow:
            mainwindow.display_done(False)
        return False

    # On garde en mémoire les domaines qui pourraient être modifiés
    domains = {word: deepcopy(word.domain) for word, ind1, ind2 in xk.binary_constraints}
    domains[xk] = deepcopy(xk.domain)

    for word in words:
        xk.domain = Tree(word)  # Affectation de word à la variable

        # forward check avec récupèration des mots dont les domaines ont été modifiés
        modif = xk.update_related_variables_domain()

        # Si on veut qu'il y ait qu'une fois un mot dans une grille,
        # il faut le retirer du domaine des autres mots de même taille
        if uniq:
            same_size_words = [w for w in grid.uninstanciated_words if w.length == xk.length]
            same_modif = []
            for w in same_size_words:
                if w.domain.remove_word(word) and w not in modif:
                    same_modif.append(w)

        # Affichage si demandé
        if mainwindow:
            # mainwindow.grid = grid
            mainwindow.display_grid()
            sleep(0.1)
        if stop:
            stop.wait()
            stop.clear()

        # Appel récursif, on vérifie que l'instanciation courante donne une solution stable
        if any([w.domain.cardinality() == 0 for w in modif]) or not backtrack(grid, heuristic_function, uniq, stop, mainwindow, first_call=False):
            # if not backtrack(grid, heuristic_function, uniq, stop, mainwindow, first_call=False):
            # rétablissement des domaines
            for w in modif:
                w.domain = deepcopy(domains[w])
            if uniq:
                for w in same_modif:
                    w.domain.add_word(word)
        else:
            return True
    grid.uninstanciated_words.insert(0, xk)
    grid.instanciated_words.remove(xk)
    xk.domain = deepcopy(domains[xk])
    if first_call and mainwindow:
        mainwindow.display_done(False)
    return False


def launch_rac():
    """
    Lancement classique
    """
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
    # res = backtrack(grid1, heuristics_max_constraints_with_instanciated, True)
    # res = backtrack(grid1, heuristic_min_domain, False)
    res = backtrack(grid1, heuristic_size_and_constraints, True)

    print("Temps de calcul de l'algo : " + str(time()-t))
    print("Temps total : " + str(time()-t1))
    print(res)
    if res:
        instanciation = [(w.id, w.domain.list_words()) for w in grid1.instanciated_words]
        instanciation.sort(key=lambda x: x[0])
        print(instanciation)


def grandes_instances():
    dir = "Data/Grilles"
    files = [
        "randomGrid10x10.txt",
        "randomGrid20x20.txt",
        "randomGrid25x25.txt",
        "randomGrid30x30.txt"
    ]

    dico = read_dictionary("Data/Dictionnaires/135000-mots-fr.txt")
    for f in files:
        print(f)
        grid = read_grid(join(dir, f), dico)
        t = time()
        res = backtrack(grid, heuristic_size_and_constraints)
        print("Grille " + f + " calculée en " + str(time()-t) + " secondes")
        if res:
            write_partially_solved_grid(join("Data/Results/Grilles_Resolues", f), grid)
        else:
            print("Grille " + f + " non résolue")


def store_grilles_enonce():
    dir_files = "Data/Grilles"
    files = [
        "gridA.txt",
        "gridB.txt",
        "gridC.txt"
    ]
    dir_dicos = "Data/Dictionnaires"
    dicos = [
        "ANDROIDE.txt",
        "850-mots-us.txt",
        "22600-mots-fr.txt",
        "58000-mots-us.txt",
        "133000-mots-us.txt",
        "135000-mots-fr.txt"
    ]
    for f in files:
        print(f)
        for dico_file in dicos:
            dico = read_dictionary(join(dir_dicos, dico_file))
            grid = read_grid(join(dir_files, f), dico)
            t = time()
            res = backtrack(grid, heuristic_size_and_constraints)
            print("Grille " + f + " calculée en " + str(time()-t) + " secondes avec le dico " + str(dico_file))
            if res:
                write_partially_solved_grid(join("Data/Results/Grilles_Resolues", f), grid)
            else:
                print("Grille " + f + " non résolue")


if __name__ == '__main__':
    # launch_rac()
    grandes_instances()
