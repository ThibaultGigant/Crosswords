# -*- coding: utf-8 -*-

from random import randint, seed, choice


def est_solitaire(grid, ligne, colonne):
    """
    Dis si une case blanche est solitaire, forçant un mot à une lettre, ce qu'on ne veut pas
    :param grid: grille rendue par generate_random_grid
    :param ligne: ligne sur laquelle se trouve la case à vérifier
    :param colonne: colonne sur laquelle se trouve la case à vérifier
    :type grid: list[list[str]]
    :type ligne: int
    :type colonne: int
    :return: True si la case souhaitée est solitaire
    :rtype: bool
    """
    nb_noirs = 0
    if ligne - 1 < 0 or (ligne - 1 >= 0 and grid[ligne - 1][colonne] == "1"):
        nb_noirs += 1
    if ligne + 1 >= len(grid) or (ligne + 1 < len(grid) and grid[ligne + 1][colonne] == "1"):
        nb_noirs += 1
    if colonne - 1 < 0 or (colonne - 1 >= 0 and grid[ligne][colonne - 1] == "1"):
        nb_noirs += 1
    if colonne + 1 >= len(grid[0]) or (colonne + 1 < len(grid[0]) and grid[ligne][colonne + 1] == "1"):
        nb_noirs += 1
    return nb_noirs == 4


def generate_random_grid(taille_largeur, taille_hauteur, densite):
    """
    Génère une grille de taille, densité (nombre de cases noires/nombre de cases blanches), prédéfinies
    :param taille_largeur: largeur de la grille à générer (nombre de colonnes)
    :param taille_hauteur: hauteur de la grille à générer (nombre de lignes)
    :param densite: nombre de cases noires/nombre de cases blanches, flottant entre 0 et 1,
                    sert en réalité de probabilité d'avoir une case blanche
    :type taille_largeur: int
    :type taille_hauteur: int
    :type densite: float
    :return: Grille générée aléatoirement
    :rtype: list[list[str]]
    """
    # Création d'une grille totalement blanche
    grid = [["0" for _ in range(taille_largeur)] for _ in range(taille_hauteur)]

    # Rajout de cases noires aléatoirement dans la grille
    nb_noirs = 0
    while float(nb_noirs)/(taille_hauteur*taille_largeur) < densite:
        seed()
        ligne = randint(0, taille_hauteur-1)
        colonne = randint(0, taille_largeur-1)
        if grid[ligne][colonne] == "0":
            grid[ligne][colonne] = "1"
            nb_noirs += 1

    # Vérification qu'un blanc ne soit pas seul (on considère qu'il n'y a pas de mot à une lettre
    for i in range(taille_hauteur):
        for j in range(taille_largeur):
            if grid[i][j] == "0":
                if est_solitaire(grid, i, j):
                    # On choisit quelle case on modifie
                    choix = choice([-1, 1])
                    if randint(0, 1) == 0:  # on modifie une ligne au dessus ou en dessous si 0
                        if 0 <= i + choix < taille_hauteur:
                            grid[i + choix][j] = "0"
                        else:
                            grid[i - choix][j] = "0"
                    else:
                        if 0 <= j + choix < taille_largeur:
                            grid[i][j + choix] = "0"
                        else:
                            grid[i][j - choix] = "0"

    return grid


if __name__ == '__main__':
    for i in generate_random_grid(10, 10, 20.0/100):
        print(i)
