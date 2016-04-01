# -*- coding: utf-8 -*-

import sys
from os import getcwd
from random import *

sys.path.append(getcwd())
from unicodedata import normalize
from data_gestion.classes import Grid, Tree


def read_dictionary(file_name):
    """
    Lit un fichier texte listant tous le dictionnaire de mots disponibles pour compléter les grilles
    :param file_name: chemin relatif du fichier contenant le dictionnaire de mots
    :type file_name: str
    :raises: IOError
    :return: dictionnaire contenant tous les mots, triés par nombre de lettres des mots
    :rtype: dict[int, Tree]
    """
    try:
        fp = open(file_name, "r")
    except:
        raise IOError("File not found")

    # dictionnaire à compléter avec les mots du fichier et à retourner
    dico = {}  # type: dict[int, Tree]

    # lecture ligne par ligne
    try:
        ligne = fp.readline()
        while ligne:
            mot = ligne.strip().upper()
            # Pour supprimer les accents
            mot = normalize("NFKD", mot).encode("ascii", "ignore").decode("ascii")
            if len(mot) in dico:
                if not dico[len(mot)].contains(mot):
                    dico[len(mot)].add_word(mot)
            else:
                dico[len(mot)] = Tree(mot)
            ligne = fp.readline()
    except:
        raise IOError("Wrong file format")

    fp.close()
    return dico


def read_grid(file_name, dictionary=None):
    """
    Lit un fichier texte contenant une grille à compléter
    :param file_name: chemin relatif du fichier contenant la grille
    :param dictionary: dictionnaire contenant tous les mots, triés par nombre de lettres des mots
    :type file_name: str
    :type dictionary: dict
    :return: Objet Grid complété selon la grille contenue dans le fichier
    :rtype: Grid
    :raises: IOError
    """
    try:
        fp = open(file_name, "r")
    except:
        raise IOError("File not found")

    # récupération des données sur la largeur et la hauteur de la grille
    width, height = list(map(int, fp.readline().split()))

    # récupération de la grille à proprement parler
    grid = []
    for _ in range(height):
        line = fp.readline().split()
        if len(line) != width:
            raise IOError("Wrong file format: wrong number of items in a line")
        else:
            for i in range(len(line)):
                line[i] = normalize("NFKD", line[i]).encode("ascii", "ignore").decode("ascii").upper()
            grid.append(line)

    fp.close()
    return Grid(grid, dictionary)

def read_values(file_name):
    """
    Lit un fichier texte listant tous le dictionnaire de mots disponibles pour compléter les grilles suivie de leurs poids
    :param file_name: chemin relatif du fichier contenant le dictionnaire de mots
    :type file_name: str
    :raises: IOError
    :return: dictionnaire contenant tous les mots
    :rtype: dict[mot, int]
    """
    try:
        fp = open(file_name, "r")
    except:
        raise IOError("File not found")

    # dictionnaire à compléter avec les mots du fichier et à retourner
    dico = {}

    # lecture ligne par ligne
    try:
        ligne = fp.readline()
        while ligne:
            word = ligne.strip().upper()
            word = normalize("NFKD", word).encode("ascii", "ignore").decode("ascii")
            dico[word] = randint(0,10)/10
            ligne = fp.readline()
    except:
        raise IOError("Wrong file format")

    fp.close()
    return dico

if __name__ == '__main__':
    dico = read_dictionary(sys.argv[1])
    print(dico)
    print(read_grid(sys.argv[2], dico))
    print("Nombre de mots : " + str(sum([i.cardinality() for i in dico.values()])))
    for i in dico.values():
        aff = i.list_words()
        print(aff)
