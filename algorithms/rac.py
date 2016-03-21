import sys
from os import getcwd
from copy import deepcopy
from random import choice

sys.path.append(getcwd())
from data_gestion.classes import Grid, Tree, Word
from data_gestion.file_gestion import *


def backtrack(V, i, heuristic_function):
    """
    Backtracking avec forward checking
    :param V: Ensemble de variables non instanciées
    :param i: instanciation courante
    :type V: list[Word]
    :return: Ensemble de solutions réalisables
    :rtype: bool
    """
    # V = grid.words # Ensemble des variables à instancier
    print("Nombre de variables à instancier : " + str(len(V)))
    if not V:
        print("sortie")
        return True

    xk = heuristic_function(V)  # Prochaine variable à instancier
    words = xk.domain.list_words()
    if words[0] == "":
        return False
    # On garde en mémoire les domaines qui pourraient être modifiés
    domains = [(word, deepcopy(word.domain)) for word, ind1, ind2 in xk.binary_constraints]
    V.remove(xk)
    for word in words:
        xk.domain = Tree(word)  # Affectation de word à la variable
        xk.respect_binary_constraints()  # forward check
        i.append((xk, word))
        if backtrack(V[:], i, heuristic_function):
            return True
        else:
            i.remove((xk, word))
            for w, domain in domains:
                w.domain = domain
    return False


def consistance_locale(grid, assignment):
    consistant = True
    constraints = grid.constraints

    for constraint in constraints:
        word1, word2, index1, index2 = constraint
        if (word1 == assignment):
            consistant = word1.respect_binary_constraint(word2, index1, index2)
        if (word2 == assignment):
            consistant = word2.respect_binary_constraint(word1, index2, index1)
        if not consistant:
            break
    return consistant


def forward_checking(grid, i, heuristic_function):
    """
    Algorithme de forward checking
    :param grid: grille sur laquelle appliquer l'algorithme
    :param i: instanciation courante
    :param heuristic_function: fonction qui choisit le mot à instancier à chaque tour de boucle
    :type grid: Grid
    :return:
    :rtype: list[Grid]
    """
    # for word in grid.words:
    #    print(word.domain.list_words())

    V = grid.words  # Ensemble des variables à instancier
    if not V:
        return i
    else:
        xk = heuristic_function(V)  # Prochaine variable à instancier
        Dk = xk.domain.list_words()  # Domaine de la variable à instancier
        for v in Dk:
            if check_forward(xk, v, V[1:]):
                i += [(xk, v)]
                return forward_checking(grid, i, heuristic_function)
    return None


def check_forward(xk, v, V):
    """
    Verifie la consistance après instanciation
    :param xk: Variable à instancier
    :param v: Valeur de l'instanciation
    :param V: Ensemble des variables à instancier
    :return:
    """
    consistant = True
    for xj in V:
        if consistant:
            Dj = xj.domain.list_words()
            for v2 in Dj:
                if not consistance((xj, v2), (xk, v)):
                    Dj.remove(v2)
        if not xj.domain.list_words():
            consistant = False
    return consistant


def consistance(assign1, assign2):
    return True


def heuristic_next(words):
    """
    Retourne la première variable parmi celles qui ne sont pas encore instanciée
    :param domain: liste de mots
    """
    return words[0]


def heuristic_fewest_conditions(words):
    """
    Retourne le mot qui a le plus de contraintes binaires
    :param words: list de mots
    :type words: list[Word]
    """
    nb_constraints = [len(i.binary_constraints) for i in words]
    min_constraints = min(nb_constraints)
    indices = [i for i, j in enumerate(nb_constraints) if j == min_constraints]
    return words[choice(indices)]


if __name__ == '__main__':
    dico = read_dictionary(sys.argv[1])
    grid = read_grid(sys.argv[2], dico)
    V = grid.words
    print(V)
    instanciation = []
    print(backtrack(V, instanciation, heuristic_fewest_conditions))
    print([(i.id, j) for i,j in instanciation])
    # forward_checking(grid, [], heuristic_function=heuristic_next)
