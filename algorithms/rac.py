import sys
from os import getcwd
sys.path.append(getcwd())
from data_gestion.classes import Grid, Tree
from data_gestion.file_gestion import *
from copy import deepcopy

def backtrack(V, i, heuristic_function):
    """
    Backtracking avec forward checking
    :param grid: grille sur laquelle appliquer l'algorithme
    :param i: instanciation courante
    :type grid: Grid
    :return: Ensemble de solutions réalisables
    :rtype: list[Grid]
    """
    #V = grid.words # Ensemble des variables à instancier
    if not V:
        print("sortie")
        return i
    else:
        xk = heuristic_function(V) # Prochaine variable à instancier
        V.remove(xk)
        Dk = deepcopy(xk.domain) # Domaine de la variable à instancier
        print("pour le mot " + str(xk.id) + " " + str(xk.domain.cardinality()))
        for v in xk.domain.list_words():
            xk.domain = Tree(v) # Affectation de v à la variable
            if xk.respect_binary_constraints():
                i += [(xk, v)]
                return backtrack(V[:], i, heuristic_function)
            else:
                print("no")
                xk.domain = Dk
                print(xk.domain.list_words())


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
    #for word in grid.words:
    #    print(word.domain.list_words())

    V = grid.words # Ensemble des variables à instancier
    if not V:
        return i
    else:
        xk = heuristic_function(V) # Prochaine variable à instancier
        Dk = xk.domain.list_words() # Domaine de la variable à instancier
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
    :return:
    """
    if words:
        return words[0]

if __name__ == '__main__':
    dico = read_dictionary(sys.argv[1])
    grid = read_grid(sys.argv[2], dico)
    V = grid.words
    print(backtrack(V, [], heuristic_function=heuristic_next))
    #forward_checking(grid, [], heuristic_function=heuristic_next)