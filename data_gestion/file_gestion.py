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


def read_valued_dictionary(file_name):
    """
    Lit un fichier texte listant tous le dictionnaire de mots disponibles pour compléter les grilles, avec leur valuation
    :param file_name: chemin relatif du fichier contenant le dictionnaire de mots
    :type file_name: str
    :raises: IOError
    :return: dictionnaire contenant tous les mots, triés par nombre de lettres des mots, et dictionnaire de valuation
    :rtype: dict[int, Tree], dict[str, float]
    """
    try:
        fp = open(file_name, "r")
    except:
        raise IOError("File not found")

    # dictionnaire à compléter avec les mots du fichier et à retourner
    dico_domaines = {}  # type: dict[int, Tree]
    dico_values = {}

    # lecture ligne par ligne
    try:
        ligne = fp.readline()
        while ligne:
            mot, valeur = ligne.split()
            mot = mot.strip().upper()
            valeur = float(valeur)
            # Pour supprimer les accents
            mot = normalize("NFKD", mot).encode("ascii", "ignore").decode("ascii")
            if len(mot) in dico_domaines:
                if not dico_domaines[len(mot)].contains(mot):
                    dico_domaines[len(mot)].add_word(mot)
            else:
                dico_domaines[len(mot)] = Tree(mot)
            if mot not in dico_values:
                dico_values[mot] = valeur
            else:
                dico_values[mot] = (dico_values[mot] + valeur)/2
            ligne = fp.readline()
    except:
        raise IOError("Wrong file format")

    fp.close()
    return dico_domaines, dico_values


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


def read_text_frequency(file_name):
    """
    Lit un fichier texte et calcule la fréquence d'apparition de chaque mot. Renvoie deux dictionnaires :
    - le dictionnaire des domaines
    - le dictionnaire des valeurs de chaque mot
    :param file_name: chemin relatif ou absolu du fichier à lire
    :type file_name: str
    :return: les deux dictionnaires (domaines et valeurs)
    """
    # ouverture du fichier
    try:
        fp = open(file_name, "r")
    except:
        raise IOError("File not found")

    # dictionnaire à compléter avec les mots du fichier et à retourner
    dico_domains = {}  # type: dict[int, Tree]
    dico_valeurs = {}

    # lecture ligne par ligne
    try:
        ligne = fp.readline()
        while ligne:
            ligne = ligne.split()
            for word in ligne:
                # Pour supprimer les caractères indésirables
                mot = word.strip(" @#&\"\'\\…∞~ß◊©≈‹≤≥‡•“‘{¶«¡Çø}—(§!)-_^¨*€%`£=+:/;.,?[]|1234567890\n\t").upper()
                if mot:
                    # Pour supprimer les accents
                    mot = normalize("NFKD", mot).encode("ascii", "ignore").decode("ascii")
                    if len(mot) > 1:
                        # Ajout du mot au dictionnaire des domaines
                        if len(mot) in dico_domains:
                            if not dico_domains[len(mot)].contains(mot):
                                dico_domains[len(mot)].add_word(mot)
                        else:
                            dico_domains[len(mot)] = Tree(mot)
                        # Ajout du mot au dictionnaire des valeurs
                        if mot in dico_valeurs:
                            dico_valeurs[mot] += 1
                        else:
                            dico_valeurs[mot] = 1

            ligne = fp.readline()
    except:
        raise IOError("Wrong file format")

    # Normalisation des fréquences
    nb_mots = sum(dico_valeurs.values())
    for cle in dico_valeurs.keys():
        dico_valeurs[cle] /= nb_mots

    fp.close()
    return dico_domains, dico_valeurs


def write_dictionnary(file_name, dico_domains, dico_values=None):
    """
    Ecrit les mots d'un dictionnaire dans un fichier, éventuellement avec sa valuation
    """
    # ouverture du fichier
    try:
        fp = open(file_name, "w")
    except:
        raise IOError("File not found")

    for taille in dico_domains:
        for word in dico_domains[taille].list_words():
            if dico_values:
                fp.write(word + " " + str(dico_values[word]) + "\n")
            else:
                fp.write(word + "\n")

    fp.close()


def write_partially_solved_grid(file_name, grid):
    """
    Ecrit le contenu d'une grille partiellement remplie dans un fichier dont le chemin relatif ou absolu est donné
    On écrira (en plus des cases noires et blanches), les cases où on est sûr de la lettre
    :param file_name: chemin relatif ou absolu du fichier dans lequel écrire
    :param grid: grille qu'on veut sauvegarder
    :type file_name: str
    :type grid: Grid
    """
    grille = grid.grid
    for word in grid.instanciated_words:
        w = word.domain.list_words()[0]
        for i in range(word.length):
            x, y = word.list_coordinates[i]
            if grille[x][y] in ["0", "1"]:
                grille[x][y] = w[i]
    fp = open(file_name, "w")
    fp.write(str(grid.get_width()) + " " + str(grid.get_height()) + "\n")
    for ligne in grille:
        fp.write(" ".join(ligne) + "\n")
    fp.close()


def test_lecture_grille():
    dico = read_dictionary(sys.argv[1])
    print(dico)
    print(read_grid(sys.argv[2], dico))
    print("Nombre de mots : " + str(sum([i.cardinality() for i in dico.values()])))
    for i in dico.values():
        aff = i.list_words()
        print(aff)


def test_lecture_frequence():
    filename = sys.argv[1]
    dicodomains, dicovaleurs = read_text_frequency(filename)
    print(dicovaleurs)
    filename = sys.argv[2]
    write_dictionnary(filename, dicodomains)


def test_lecture_valued_dico():
    filename = sys.argv[1]
    dicodomains, dicovaleurs = read_valued_dictionary(filename)
    print(dicovaleurs)


if __name__ == '__main__':
    # test_lecture_grille()
    test_lecture_frequence()
    # test_lecture_valued_dico()


