import sys
from os import getcwd
from copy import deepcopy
from time import time, sleep

sys.path.append(getcwd())
from data_gestion.classes import Grid, Tree, Word
from data_gestion.file_gestion import *
from algorithms.arc_consistency import ac3
from algorithms.heuristics import *


def CBJ(grid, heuristic_function, uniq=True, stop=False, mainwindow=None):
    """
    Conflict BackJumping
    :param grid: grille sur laquelle on lance l'algorithme
    :param heuristic_function: fonction heuristique qui détermine quel mot sera instancié à chaque itération
    :type grid: Grid
    :return: Ensemble de variables "en conflit" s'il y en a
    :rtype: set
    """
    # print("Mots restants à instancier : " + str(len(grid.uninstanciated_words)))
    if not grid.uninstanciated_words:
        instanciation = [(w.id, w.domain.list_words()) for w in grid1.instanciated_words]
        instanciation.sort(key=lambda x: x[0])
        # print(instanciation)
        return set([])

    conflit = set([])

    xk = heuristic_function(grid.uninstanciated_words)  # Prochaine variable à instancier
    grid.uninstanciated_words.remove(xk)
    grid.instanciated_words.append(xk)

    domain = deepcopy(xk.domain)

    words = xk.domain.list_words()
    for word in words:
        # print("Essai instanciation mot " + str(xk.id) + " en " + word)
        xk.domain = Tree(word)

        if stop:
            if mainwindow:
                mainwindow.grid = grid
                mainwindow.display_grid()
            sleep(0.1)
            # input("Appuyez sur la touche ENTREE pour continuer...")

        conflit_local = set(xk.consistant(grid.instanciated_words))

        if uniq:
            same_words = set(grid.is_word_already_in(word))
            same_words.remove(xk)
            if same_words:
                # print("On a trouvé des mots pareil : " + str([w.id for w in same_words]) + " !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                conflit_local = conflit_local.union(same_words)

        # print([w.id for w in conflit_local])
        if not conflit_local:
            conflit_fils = CBJ(grid, heuristic_function, uniq)
            # print("conflit fils de " + str(xk.id) + " : " + str(conflit_fils))

            if xk in conflit_fils:
                conflit_fils.remove(xk)
                conflit = conflit.union(conflit_fils)
            else:
                # print("No conflit local pour " + str(xk.id) + " et il n'est pas dans " + str([w.id for w in conflit_local]))
                conflit = conflit_fils
                break
        else:
            # print("Ajout conflit entre mot " + str(xk.id) + " et " + str([w.id for w in conflit_local]))
            conflit = conflit.union(conflit_local)

    if conflit:
        xk.domain = domain
        grid.instanciated_words.remove(xk)
        grid.uninstanciated_words.insert(0, xk)
    # print("back from " + str(xk.id) + " avec conflit : " + str([w.id for w in conflit]))
    return conflit

if __name__ == '__main__':
    t1 = time()
    dico = read_dictionary(sys.argv[1])
    print("Temps de création du dictionnaire : " + str(time()-t1))
    t = time()
    grid1 = read_grid(sys.argv[2], dico)
    print("Temps de création de la grille: " + str(time()-t))
    t = time()
    ac3(grid1)
    res = CBJ(grid1, heuristic_next, True)

    print("Temps de calcul de l'algo : " + str(time()-t))
    print("Temps total : " + str(time()-t1))
    print(res)
    if not res:
        instanciation = [(w.id, w.domain.list_words()) for w in grid1.instanciated_words]
        instanciation.sort(key=lambda x: x[0])
        print(instanciation)
