import sys
from unicodedata import normalize
from classes import Grid


def read_dictionary(file_name):
    """
    Lit un fichier texte listant tous le dictionnaire de mots disponibles pour compléter les grilles
    :param file_name: chemin relatif du fichier contenant le dictionnaire de mots
    :type file_name: str
    :raises: IOError
    :return: dictionnaire contenant tous les mots, triés par nombre de lettres des mots
    :rtype: dict
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
            mot = ligne.strip().lower()
            # Pour supprimer les accents
            mot = normalize("NFKD", mot).encode("ascii", "ignore").decode("ascii")
            if len(mot) in dico:
                dico[len(mot)].add(mot)
            else:
                dico[len(mot)] = {mot}
            ligne = fp.readline()
    except:
        raise IOError("Wrong file format")

    fp.close()
    return dico


def read_grid(file_name, dictionary):
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
    for i in range(height):
        line = fp.readline().split()
        if len(line) != width:
            raise IOError("Wrong file format: wrong number of items in a line")
        else:
            grid.append(line)

    fp.close()
    return Grid(grid, dictionary)


if __name__ == '__main__':
    dico = read_dictionary(sys.argv[1])
    print(dico)
    print(read_grid(sys.argv[2], dico))
    print(sum([len(i) for i in dico.values()]))
