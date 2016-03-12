import sys
from unicodedata import normalize


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


if __name__ == '__main__':
    dico = read_dictionary(sys.argv[1])
    print(dico)
    print(sum([len(value) for value in dico.values()]))
