import sys
from os import getcwd
from copy import deepcopy
from random import choice

sys.path.append(getcwd())
from data_gestion.classes import Grid, Tree, Word
from data_gestion.file_gestion import *
from algorithms.arc_consistency import ac3

def CBJ(V, heuristic_function):
    if not V:
        return []

    conflit = []
    nonBJ = True

    xk = heuristic_function(V)  # Prochaine variable à instancier
    V.remove(xk)
    words = xk.domain.list_words()

    if words == [""]:
        return False

    domains = {word: deepcopy(word.domain) for word, ind1, ind2 in xk.binary_constraints}  # type: dict[Word, Tree]
    domains[xk] = deepcopy(xk.domain)

    for word in words:
        if nonBJ:
            xk.domain = Tree(word)
            #modif = xk.update_related_variables_domain()

            conflit_local = consistante(V)
            if not conflit_local:
                conflit_fils = CBJ(V[:])
                if xk in conflit_fils:
                    conflit += conflit_fils
                else:
                    conflit = conflit_fils
                    nonBJ = False
            else:
                conflit += conflit_local
    return conflit


def consistante(V):
    return True

