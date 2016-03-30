# -*- coding: utf-8 -*-

import sys
from os import getcwd
from copy import deepcopy
from random import choice
from time import time

sys.path.append(getcwd())
from data_gestion.classes import Grid, Tree, Word
from data_gestion.file_gestion import *
from algorithms.arc_consistency import ac3


def backtrack(V, heuristic_function, uniq=True):
    """
    Backtracking avec forward checking
    :param V: Ensemble de variables non instanciées
    :param heuristic_function: fonction heuristique qui détermine quel mot sera instancié à chaque itération
    :param uniq: True si un mot ne peut apparaître qu'une fois dans la grille, False sinon
    :type V: list[Word]
    :type uniq: bool
    :return: Ensemble de solutions réalisables
    :rtype: bool
    """
    # V = grid.words # Ensemble des variables à instancier
    if not V:
        return True

    xk = heuristic_function(V)  # Prochaine variable à instancier
    V.remove(xk)
    words = xk.domain.list_words()
    # print("Tentative d'instanciation du mot " + str(xk.id) + " parmi les mots : " + str(words))
    if words == [""]:
        return False
    # On garde en mémoire les domaines qui pourraient être modifiés
    domains = {word: deepcopy(word.domain) for word, ind1, ind2 in xk.binary_constraints}  # type: dict[Word, Tree]
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
            same_size_words = [w for w in V if w.length == xk.length]
            same_modif = []
            for w in same_size_words:
                if w.domain.remove_word(word) and w not in modif:
                    same_modif.append(w)

        # print("Après modification")
        # for w in domains.keys():
        #     print(str(w.id) + " : " + str(w.domain.list_words()) + str(w.domain.cardinality()))

        # Appel récursif, on vérifie que l'instanciation courante donne une solution stable
        if any([w.domain.cardinality() == 0 for w in modif]) or not backtrack(V[:], heuristic_function, uniq):
            # if not backtrack(V[:], heuristic_function, uniq):
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
    xk.domain = deepcopy(domains[xk])
    return False


def heuristic_next(words):
    """
    Retourne la première variable parmi celles qui ne sont pas encore instanciée
    :param domain: liste de mots
    """
    return words[0]


def heuristic_max_constraints(words):
    """
    Retourne le mot qui a le plus de contraintes binaires
    :param words: liste de mots
    :type words: list[Word]
    :rtype: Word
    """
    nb_constraints = [len(i.binary_constraints) for i in words]
    max_constraints = max(nb_constraints)
    indices = [i for i, j in enumerate(nb_constraints) if j == max_constraints]
    return words[choice(indices)]


def heuristic_min_domain(words):
    """
    Retourne le mot qui a le plus petit domaine
    :param words: liste de mots
    :type words: list[Word]
    :rtype: Word
    """
    domains_size = [word.domain.cardinality() for word in words]
    min_domain = min(domains_size)
    indices = [i for i, j in enumerate(domains_size) if j == min_domain]
    return words[choice(indices)]


def heuristic_constraints_and_size(words):
    """
    Retourne le mot qui a le plus de contraintes binaires,
    en cas d'égalité celui d'entre eux qui a le plus petit domaine,
    en cas d'égalité on en choisit un au hasard
    :param words: liste de mots
    :type words: list[Word]
    :rtype: Word
    """
    nb_constraints = [len(i.binary_constraints) for i in words]
    max_constraints = max(nb_constraints)
    indices = [i for i, j in enumerate(nb_constraints) if j == max_constraints]
    if len(indices) > 1:
        return heuristic_min_domain([words[i] for i in indices])
    return words[choice(indices)]


def heuristic_size_and_constraints(words):
    """
    Retourne le mot qui a le plus de contraintes binaires,
    en cas d'égalité celui d'entre eux qui a le plus petit domaine,
    en cas d'égalité on en choisit un au hasard
    :param words: liste de mots
    :type words: list[Word]
    :rtype: Word
    """
    domains_size = [word.domain.cardinality() for word in words]
    min_domain = min(domains_size)
    indices = [i for i, j in enumerate(domains_size) if j == min_domain]
    if len(indices) > 1:
        return heuristic_max_constraints([words[i] for i in indices])
    return words[choice(indices)]


if __name__ == '__main__':
    t1 = time()
    dico = read_dictionary(sys.argv[1])
    print("Temps de création du dictionnaire : " + str(time()-t1))
    t = time()
    grid = read_grid(sys.argv[2], dico)
    print("Temps de création de la grille: " + str(time()-t))
    t = time()
    ac3(grid)
    V = grid.words
    # print(V)
    # res = backtrack(V[:], heuristic_max_constraints)
    # res = backtrack(V[:], heuristic_constraints_and_size, False)
    # res = backtrack(V[:], heuristic_next, True)
    # res = backtrack(V[:], heuristic_min_domain, False)
    res = backtrack(V[:], heuristic_size_and_constraints, True)
    print("Temps de calcul de l'algo : " + str(time()-t))
    print("Temps total : " + str(time()-t1))
    print(res)
    if res:
        print([(w.id, w.domain.list_words()) for w in V])
