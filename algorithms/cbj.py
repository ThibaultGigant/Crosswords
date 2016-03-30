import sys
from os import getcwd
from copy import deepcopy
from random import choice
from time import time

sys.path.append(getcwd())
from data_gestion.classes import Grid, Tree, Word
from data_gestion.file_gestion import *
from algorithms.rac2 import *

def CBJ(grid, heuristic_function, uniq=True):
    """
    Conflict BackJumping
    :param grid: grille sur laquelle on lance l'algorithme
    :param heuristic_function: fonction heuristique qui détermine quel mot sera instancié à chaque itération
    :return: Ensemble de variables "en conflit"
    """
    if not grid.uninstanciated_words:
        return []

    conflit = []
    nonBJ = True

    xk = heuristic_function(grid.uninstanciated_words)  # Prochaine variable à instancier
    grid.uninstanciated_words.remove(xk)
    grid.instanciated_words.append(xk)
    words = xk.domain.list_words()

    if words == [""]:
        return False

    #domains = {word: deepcopy(word.domain) for word, ind1, ind2 in xk.binary_constraints}
    domain = deepcopy(xk.domain)

    for word in words:
        if nonBJ:
            xk.domain = Tree(word)
            conflit_local = xk.consistant()

            if not conflit_local:
                conflit_fils = CBJ(grid, heuristic_function, uniq)
                if xk in conflit_fils:
                    conflit += conflit_fils
                else:
                    conflit = conflit_fils
                    nonBJ = False

                    xk.domain = domain
            else:
                conflit += conflit_local
    return conflit

if __name__ == '__main__':
    t1 = time()
    dico = read_dictionary(sys.argv[1])
    print("Temps de création du dictionnaire : " + str(time()-t1))
    t = time()
    grid1 = read_grid(sys.argv[2], dico)
    print("Temps de création de la grille: " + str(time()-t))
    t = time()

    res = CBJ(grid1, heuristic_size_and_constraints, True)

    print("Temps de calcul de l'algo : " + str(time()-t))
    print("Temps total : " + str(time()-t1))
    print(res)
