import sys
from os import getcwd
sys.path.append(getcwd())
from data_gestion.classes import Grid, Tree

def backtrack(grille, heuristic_function):
    """
    Algorithme de backtracking avec forward checking
    :param grille: grille sur laquelle appliquer l'algorithme
    :param heuristic_function: fonction qui choisit le mot à instancier à chaque tour de boucle
    :type grille: Grid
    :return: Ensemble de solutions réalisables
    :rtype: list[Grid]
    """
    return 0


def forward_checking():
    return 0