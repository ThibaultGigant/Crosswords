# -*- coding: utf-8 -*-

import sys
from os import getcwd, listdir
from os.path import basename, dirname, join
from time import time
from pickle import dump, load
import matplotlib.pyplot as plt

sys.path.append(getcwd())
from data_gestion.file_gestion import read_dictionary, read_grid, write_partially_solved_grid
from algorithms.arc_consistency import ac3
from algorithms.rac import backtrack
from algorithms.cbj import CBJ
from algorithms.heuristics import *

algorithms = [backtrack, CBJ]

str_algo = {backtrack: "RAC", CBJ: "CBJ"}

heuristics = [  # heuristic_next,
              heuristic_max_constraints, heuristic_min_domain, heuristic_constraints_and_size,
              heuristic_size_and_constraints, heuristics_max_constraints_with_instanciated
              ]
str_heuristics = {heuristic_next: "heuristic_next", heuristic_max_constraints: "heuristic_max_constraints",
                  heuristic_min_domain: "heuristic_min_domain",
                  heuristic_constraints_and_size: "heuristic_constraints_and_size",
                  heuristic_size_and_constraints: "heuristic_size_and_constraints",
                  heuristics_max_constraints_with_instanciated: "heuristics_max_constraints_with_instanciated"
                  }

heuristics_str = """Légende des heuristiques :
1: heuristic_max_constraints
2: heuristic_min_domain
3: heuristic_constraints_and_size
4: heuristic_size_and_constraints
5: heuristics_max_constraints_with_instanciated
"""

list_files = ["randomGrid5x5.txt",
              "gridA.txt",
              "gridB.txt",
              "gridC.txt",
              "randomGrid10x10.txt",
              "grid13x13GridIndex.txt"
              ]
list_files_str = """Légende des grilles lancées :
0: randomGrid5x5.txt
1: gridA.txt
2: gridB.txt
3: gridC.txt
4: randomGrid10x10.txt
5: grid13x13GridIndex.txt
"""

list_dicos = [
    "ANDROIDE.txt",
    "850-mots-us.txt",
    "22600-mots-fr.txt",
    "58000-mots-us.txt",
    "133000-mots-us.txt",
    "135000-mots-fr.txt"
]

list_dicos_str = """Légende des dictionnaires lancés :
0: ANDROIDE.txt
1: 850-mots-us.txt
2: 22600-mots-fr.txt
3: 58000-mots-us.txt
4: 133000-mots-us.txt
5: 135000-mots-fr.txt
"""


def benchmark_heuristics(file_grid, file_dico, output_file=None, algo=backtrack, do_ac3=True):
    """
    Calcule les temps de calcul d'une solution pour une grille suivant toutes les heuristiques,
    puis stocke le résultat dans un fichier
    :param file_grid: Fichier où se trouve la grille sur laquelle appliquer les heuristiques
    :param file_dico: Fichier où se trouve le dictionnaire contenant les mots à appliquer
    :param output_file: Fichier où écrire les données
    """
    times = []
    for heuristic in heuristics:
        print(str_heuristics[heuristic])
        nb = 1 if heuristic == heuristic_next else 5
        temp = []
        for i in range(nb):
            print("Itération " + str(i), end=" ")
            dico = read_dictionary(file_dico)
            grid = read_grid(file_grid, dico)
            if do_ac3:
                ac3(grid)
            t = time()
            algo(grid, heuristic)
            temp.append(time() - t)
            print("took " + str(temp[-1]) + " seconds")
        times.append(sum(temp)/nb)
        print("heuristic " + str_heuristics[heuristic] + " takes an average of " + str(times[-1]) + " seconds")
    if output_file:
        fp = open(output_file, "wb")
        dump(times, fp)
        fp.close()
    return times


def affiche_plot_heuristics(origin_file_grid, origin_file_dico, input_file, algo=backtrack):
    """
    Récupère les données écrites dans un fichier pour l'afficher dans un plot
    :param origin_file_grid: Fichier d'origine de la grille
    :param origin_file_dico: Fichier d'origine du dictionnaire utilisé
    :param input_file: fichier où récupérer les données
    """
    fp = open(input_file, "rb")
    times = load(fp)
    fp.close()
    plt.plot(range(len(heuristics)), times, "-o")
    plt.title("Temps d'exécution de " + str_algo[algo] + " en fonction de l'heuristique utilisée sur " + basename(origin_file_grid) + " et le dictionnaire " + basename(origin_file_dico))
    plt.ylabel("Temps d'exécution")
    plt.xlabel('Heuristique')
    plt.yscale("log")
    plt.annotate(heuristics_str, xy=(1.5, 50))
    plt.show()


def benchmark_taille_grille(dossier_grids, file_dico, output_file=None, algo=backtrack):
    """
    Calcule les temps de calcul d'une solution pour les grilles d'un dossier, puis stocke le résultat dans un fichier
    :param dossier_grids: dossier contenant les fichiers des grilles
    :param file_dico: Fichier du dictionnaire à utiliser
    :param output_file: fichier où écrire les données
    """
    times = []
    dico = read_dictionary(file_dico)

    for file_grid in list_files:
        print(file_grid)
        temp = []
        for i in range(5):
            print("Itération " + str(i), end=" ")
            grid = read_grid(join(dossier_grids, file_grid), dico)
            ac3(grid)
            t = time()
            algo(grid, heuristic_size_and_constraints)
            temp.append(time() - t)
            print("took " + str(temp[-1]) + " seconds")
        times.append(sum(temp)/5)
        print("File " + file_grid + " takes an average of " + str(times[-1]) + " seconds")
    if output_file:
        fp = open(output_file, "wb")
        dump(times, fp)
        fp.close()
    return times


def affiche_plot_taille(origin_dossier_grids, origin_file_dico, input_file, algo=backtrack):
    """
    Récupère les données écrites dans un fichier pour l'afficher dans un plot
    :param origin_dossier_grids: Dossier d'origine des grilles où sont situés les fichiers de list_files
    :param origin_file_dico: Fichier d'origine du dictionnaire utilisé
    :param input_file: fichier où récupérer les données
    """
    fp = open(input_file, "rb")
    times = load(fp)
    fp.close()
    plt.plot(range(len(list_files)), times, "-o")
    plt.title("Temps d'exécution de " + str_algo[algo] + " en fonction de la grille exécutée, avec le dictionnaire " + basename(origin_file_dico))
    plt.ylabel("Temps d'exécution")
    plt.xlabel("Grille lancée")
    plt.yscale("log")
    plt.annotate(list_files_str, xy=(2.5, 0.1))
    plt.show()


def benchmark_ac3(file_grid, file_dico, output_file=None, algo=backtrack):
    """
    Calcule les temps de calcul d'une solution pour une grille suivant toutes les heuristiques, avec et sans AC3
    puis stocke le résultat dans un fichier
    :param file_grid: Fichier où se trouve la grille sur laquelle appliquer les heuristiques
    :param file_dico: Fichier où se trouve le dictionnaire contenant les mots à appliquer
    :param output_file: Fichier où écrire les données
    """
    dico = {}
    dico["ac3"] = benchmark_heuristics(file_grid, file_dico, do_ac3=True)
    dico["not_ac3"] = benchmark_heuristics(file_grid, file_dico, do_ac3=False)
    if output_file:
        fp = open(output_file, "wb")
        dump(dico, fp)
        fp.close()
    return dico


def affiche_plot_ac3(origin_file_grid, origin_file_dico, input_file, algo=backtrack):
    """
    Récupère les données écrites dans un fichier pour l'afficher dans un plot
    :param origin_file_grid: Fichier d'origine de la grille
    :param origin_file_dico: Fichier d'origine du dictionnaire utilisé
    :param input_file: fichier où récupérer les données
    """
    fp = open(input_file, "rb")
    dico = load(fp)
    fp.close()
    plt.plot(range(1, len(heuristics)+1), dico["ac3"], "-o", label="With AC3")
    plt.plot(range(1, len(heuristics)+1), dico["not_ac3"], "-+", label="Without AC3")
    plt.title("Temps d'exécution de " + str_algo[algo] + " en fonction de l'heuristique utilisée sur " + basename(origin_file_grid) + " et le dictionnaire " + basename(origin_file_dico))
    plt.ylabel("Temps d'exécution")
    plt.xlabel('Heuristique')
    plt.yscale("log")
    plt.legend(loc="best")
    plt.annotate(heuristics_str, xy=(3.5, 5))
    plt.show()


def benchmark_dico(file_grid, dossier_dicos, output_file=None, algo=backtrack):
    """
    Calcule les temps de calcul d'une solution pour une grille avec différents dictionnaires,
    puis stocke le résultat dans un fichier
    :param file_grid: Chemin relatif ou absolu menant à la grille qu'on veut lancer
    :param dossier_dicos: Dossier contenant tous les dictionnaires à lancer
    :param output_file: fichier où écrire les données
    """
    times = []

    for file_dico in list_dicos:
        print(file_dico)
        temp = []
        for i in range(5):
            print("Itération " + str(i), end=" ")
            dico = read_dictionary(join(dossier_dicos, file_dico))
            grid = read_grid(file_grid, dico)
            ac3(grid)
            t = time()
            algo(grid, heuristic_size_and_constraints)
            temp.append(time() - t)
            print("took " + str(temp[-1]) + " seconds")
        times.append(sum(temp)/5)
        print("Dico " + file_dico + " takes an average of " + str(times[-1]) + " seconds")
    if output_file:
        fp = open(output_file, "wb")
        dump(times, fp)
        fp.close()
    return times


def affiche_plot_dico(origin_file_grid, dossier_dicos, input_file, algo=backtrack):
    """
    Récupère les données écrites dans un fichier pour l'afficher dans un plot
    :param origin_file_grid: Fichier d'origine de la grille
    :param origin_file_dico: Fichier d'origine du dictionnaire utilisé
    :param input_file: fichier où récupérer les données
    """
    fp = open(input_file, "rb")
    times = load(fp)
    fp.close()
    plt.plot(range(len(list_dicos)), times, "-o")
    plt.title("Temps d'exécution de " + str_algo[algo] + " en fonction du dictionnaire utilisé sur " + basename(origin_file_grid))
    plt.ylabel("Temps d'exécution")
    plt.xlabel('Dictionnaire')
    plt.yscale("log")
    plt.annotate(list_dicos_str, xy=(3, 10))
    plt.show()


def benchmark_algo(dossier_grids, file_dico, output_file=None):
    """
    Calcule les temps de calcul d'une solution pour les grilles d'un dossier, puis stocke le résultat dans un fichier
    :param dossier_grids: dossier contenant les fichiers des grilles
    :param file_dico: Fichier du dictionnaire à utiliser
    :param output_file: fichier où écrire les données
    """
    dico = {}
    dico["rac"] = benchmark_taille_grille(dossier_grids, file_dico, algo=backtrack)
    dico["cbj"] = benchmark_taille_grille(dossier_grids, file_dico, algo=CBJ)
    if output_file:
        fp = open(output_file, "wb")
        dump(dico, fp)
        fp.close()
    return dico


def affiche_plot_algo(dossier_grids, origin_file_dico, input_file, algo=backtrack):
    """
    Récupère les données écrites dans un fichier pour l'afficher dans un plot
    :param dossier_grids: Dossier contenant les grilles
    :param origin_file_dico: Fichier dictionnaire ayant servi à faire les calculs
    :param input_file: fichier où récupérer les données
    """
    fp = open(input_file, "rb")
    dico = load(fp)
    fp.close()
    plt.plot(range(len(list_files)), dico["rac"], "-o", label="$RAC$")
    plt.plot(range(len(list_files)), dico["cbj"], "-+", label="$CBJ$")
    plt.title("Temps d'exécution des algorithmes en fonction de la grille sur lequel il s'applique, avec le dictionnaire " + basename(origin_file_dico))
    plt.ylabel("Temps d'exécution")
    plt.xlabel('Grille lancée')
    plt.yscale("log")
    plt.legend(loc="best")
    plt.annotate(list_files_str, xy=(3.5, 5))
    plt.show()


if __name__ == '__main__':
    # benchmark_heuristics(sys.argv[1], sys.argv[2], sys.argv[3])
    # affiche_plot_heuristics(sys.argv[1], sys.argv[2], sys.argv[3])

    # benchmark_taille_grille(sys.argv[1], sys.argv[2], sys.argv[3])
    # affiche_plot_taille(sys.argv[1], sys.argv[2], sys.argv[3])

    # benchmark_ac3(sys.argv[1], sys.argv[2], sys.argv[3])
    # affiche_plot_ac3(sys.argv[1], sys.argv[2], sys.argv[3])

    # benchmark_dico(sys.argv[1], sys.argv[2], sys.argv[3])
    affiche_plot_dico(sys.argv[1], sys.argv[2], sys.argv[3])

    # benchmark_algo(sys.argv[1], sys.argv[2], sys.argv[3])
    # affiche_plot_algo(sys.argv[1], sys.argv[2], sys.argv[3])


