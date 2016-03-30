import sys
from os import getcwd
from copy import deepcopy
from time import time

sys.path.append(getcwd())
from data_gestion.classes import Grid, Tree, Word
from data_gestion.file_gestion import *
from algorithms.arc_consistency import ac3
from algorithms.heuristics import *


def CBJ(grid, heuristic_function, uniq=True):
    """
    Conflict BackJumping
    :param grid: grille sur laquelle on lance l'algorithme
    :param heuristic_function: fonction heuristique qui détermine quel mot sera instancié à chaque itération
    :type grid: Grid
    :return: Ensemble de variables "en conflit" s'il y en a
    """
    if not grid.uninstanciated_words:
        return []

    conflit = []
    print("Mots restants à instancier : " + str(len(grid.uninstanciated_words)))

    xk = heuristic_function(grid.uninstanciated_words)  # Prochaine variable à instancier
    grid.uninstanciated_words.remove(xk)
    grid.instanciated_words.append(xk)

    # domains = {word: deepcopy(word.domain) for word, ind1, ind2 in xk.binary_constraints}
    domain = deepcopy(xk.domain)

    words = xk.domain.list_words()
    for word in words:
        # print("Essai instanciation mot " + str(xk.id) + " en " + word)
        xk.domain = Tree(word)
        conflit_local = xk.consistant()

        if uniq:
            same_words = grid.is_word_already_in(word)
            conflit_local += [w for w in same_words if (w != xk and w not in conflit_local)]

        if not conflit_local:
            conflit_fils = CBJ(grid, heuristic_function, uniq)
            if not conflit_fils:  # Si il n'y a pas de conflit local ni de conflit fils, on a trouvé une bonne instance
                return []

            if xk in conflit_fils:
                conflit += [w for w in conflit_fils if (w != xk and w not in conflit)]
            else:
                conflit = conflit_fils
                break
        else:
            conflit += [w for w in conflit_local if w not in conflit]

    xk.domain = domain
    grid.instanciated_words.remove(xk)
    grid.uninstanciated_words.insert(0, xk)
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
    for w in grid1.words:
        print(w.domain.list_words())
    res = CBJ(grid1, heuristic_size_and_constraints, True)

    print("Temps de calcul de l'algo : " + str(time()-t))
    print("Temps total : " + str(time()-t1))
    print(res)
    if not res:
        instanciation = [(w.id, w.domain.list_words()) for w in grid1.instanciated_words]
        instanciation.sort(key=lambda x: x[0])
        print(instanciation)
