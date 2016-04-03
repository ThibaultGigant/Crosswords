# -*- coding: utf-8 -*-

import sys
from os import getcwd, listdir
from os.path import basename, dirname, join
from time import time
from pickle import dump, load

sys.path.append(getcwd())
from data_gestion.file_gestion import read_dictionary, read_grid, write_partially_solved_grid
from algorithms.arc_consistency import ac3
from algorithms.rac import backtrack
from algorithms.cbj import CBJ
from algorithms.heuristics import *

algorithms = [backtrack, CBJ]
heuristics = [heuristic_constraints_and_size,
              heuristic_size_and_constraints, heuristics_max_constraints_with_instanciated
              ]

ordre_temps = """Ordre d'affichage des temps :
- backtrack avec heuristic_constraints_and_size sans obligation que chaque mot soit unique dans la grille
- backtrack avec heuristic_constraints_and_size avec obligation que chaque mot soit unique dans la grille
- backtrack avec heuristic_size_and_constraints sans obligation que chaque mot soit unique dans la grille
- backtrack avec heuristic_size_and_constraints avec obligation que chaque mot soit unique dans la grille
- backtrack avec heuristics_max_constraints_with_instanciated sans obligation que chaque mot soit unique dans la grille
- backtrack avec heuristics_max_constraints_with_instanciated avec obligation que chaque mot soit unique dans la grille
- CBJ avec heuristic_constraints_and_size sans obligation que chaque mot soit unique dans la grille
- CBJ avec heuristic_constraints_and_size avec obligation que chaque mot soit unique dans la grille
- CBJ avec heuristic_size_and_constraints sans obligation que chaque mot soit unique dans la grille
- CBJ avec heuristic_size_and_constraints avec obligation que chaque mot soit unique dans la grille
- CBJ avec heuristics_max_constraints_with_instanciated sans obligation que chaque mot soit unique dans la grille
- CBJ avec heuristics_max_constraints_with_instanciated avec obligation que chaque mot soit unique dans la grille

"""


def calcul_temps_algos(grid_file, dico_file):
    """
    Applique tous les algorithmes (et toutes les heuristiques) à la grille et renvoie le temps d'exécution de chacun
    :param grid_file: chemin relatif ou absolu de la grille à tester
    :param dico_file: chemin relatif ou absolu du dictionnaire associé
    :return: liste des temps d'exécution
    :rtype: list[list[int]]
    """
    temps = []
    for launch_ac3 in [False, True]:
        temps_ac3 = []
        for algo in algorithms:
            for heuristic in heuristics:
                for uniq in [False, True]:
                    dico = read_dictionary(dico_file)
                    grid = read_grid(grid_file, dico)
                    t = time()
                    if launch_ac3:
                        ac3(grid)
                    algo(grid, heuristic, uniq=uniq)
                    temps_ac3.append((time()-t))
        temps.append(temps_ac3)
    return temps


def benchmark_algos(dossier_grilles, dossier_dicos):
    """
    Effectue le calcul des temps d'exécution de chaque grille avec chaque dictionnaire
    :param dossier_grilles: dossier contenant les fichiers de toutes les grilles
    :param dossier_dicos: dossier contenant tous les dictionnaires
    :return: dictionnaire de dictionnaire tel que grille --> dictionnaire utilisé --> liste des temps d'exécution
    :rtype: dict[str, dict[str, list[list[int]]]]
    """
    res_dico = {}

    # Exécution pour chaque grille
    for grid_file in [f for f in listdir(dossier_grilles) if f[-4:] == ".txt"]:
        print(grid_file)
        dico_grille = {}
        grid = read_grid(join(dossier_grilles, grid_file))
        # Et chaque dico
        for dico_file in [f for f in listdir(dossier_dicos) if f[-4:] == ".txt"]:
            print(dico_file)
            dico_grille[dico_file] = calcul_temps_algos(join(dossier_grilles, grid_file), join(dossier_dicos, dico_file))

        res_dico[grid_file] = dico_grille

    return res_dico


def benchmark_to_file(dossier_grilles, dossier_dicos, output_file):
    """
    Effectue le benchmark et écrit le résultat dans 2 fichiers :
    - un premier formaté pour être lu
    - et le 2ème contiendra le dictionnaire enregistré avec pickle pour pouvoir le récupérer par la suite
    :param dossier_grilles: dossier contenant les fichiers de toutes les grilles
    :param dossier_dicos: dossier contenant tous les dictionnaires
    :param output_file: fichier où écrire tous les résultats
    """
    t = time()
    # Récupération du dictionnaire
    dico = benchmark_algos(dossier_grilles, dossier_dicos)
    print("Les benchmarks ont pris : " + str(time()-t) + " secondes")

    # Ecriture en binaire dans le fichier grâce à pickle
    fp = open(join(dirname(output_file), "pickle_" + basename(output_file)), "wb")
    dump(dico, fp)
    fp.close()

    # Ecriture dans le fichier formaté pour la lecture
    grand_sep = "=========================================================\n"
    petit_sep = "-------------------------------\n"
    fp = open(output_file, "w")
    fp.write(ordre_temps)
    for grille, dico_grille in dico.items():
        fp.write("\n\n" + grand_sep)
        fp.write(grille + "\n")
        fp.write(grand_sep)
        for dictionnaire, list_temps in dico_grille.items():
            fp.write(petit_sep)
            fp.write(dictionnaire + "\n")
            fp.write(petit_sep)
            fp.write("Sans AC3 : " + str(list_temps[0]) + "\n")
            fp.write("Avec AC3 : " + str(list_temps[1]) + "\n")
    fp.close()


def get_benchmark_results_from_file(input_file):
    """
    Récupère le résultat d'un benchmark écrit dans le fichier et retourne le dictionnaire en question
    :param input_file: chemin relatif ou absolu du fichier où récupérer les données
    :type input_file: str
    :return: dictionnaire contenant les résultats d'un benchmark lancé auparavant
    :rtype: dict[str, dict[str, list[list[int]]]]
    """
    fp = open(input_file, "rb")
    dico = load(fp)
    fp.close()
    return dico


if __name__ == '__main__':
    benchmark_to_file(sys.argv[1], sys.argv[2], sys.argv[3])
