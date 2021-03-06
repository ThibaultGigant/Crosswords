import sys
from os import getcwd
from copy import copy
from time import time

sys.path.append(getcwd())
from data_gestion.classes import deepcopy
from data_gestion.file_gestion import *
from algorithms.arc_consistency import ac3


def bnb(nvar, grid_words, dico_values, nodes=[], node=([], 0), best=([], 0), uniq=True):
    """
    Branch and Bound
    :param grid_words: Mot à instancier
    :param nodes: Liste de noeuds de l'arbre
    :param node: Noeud courant sur lequel brancher
    :param borne: Borne inférieur
    :return: Solution optimale
    """
    if grid_words:
        variable = grid_words[0]
        new_grid_words = copy(grid_words)
        new_grid_words.remove(variable)
        variable_domain = copy(variable.domain.list_words())
        if "" in variable_domain:
            variable_domain.remove("")
        variable_domain.sort(key=lambda x: dico_values[x], reverse=True)

        # On garde en mémoire les domaines
        domains = {word: deepcopy(word.domain) for word, ind1, ind2 in variable.binary_constraints}
        domains[variable] = deepcopy(variable.domain)

        for word in variable_domain:

            if not uniq or (uniq and word not in node[0]):
                consistant = True

                # Instanciation
                variable.domain = Tree(word)
                modif = variable.update_related_variables_domain()

                if any([w.domain.cardinality() == 0 for w in modif]):
                    consistant = False

                    variable.domain = deepcopy(domains[variable])
                    for w in modif:
                        w.domain = deepcopy(domains[w])

                # Calcule des bornes inf et sup
                inf, sup = bounds(new_grid_words, node, word, dico_values)

                # Ajouter noeud à l'arbre de recherche
                (new_node, new_sup) = (copy(node[0]) + [word], sup)
                nodes += [(new_node, new_sup)]

                # Si consistant, on branche
                if consistant:
                    # Si on est à une feuille de l'arbre et la valeur trouvée est > à la valeur de la meilleure solution trouvée, retenir nouvelle solution
                    if (len(new_node) == nvar) and inf > best[1]:
                        best = (new_node, inf)

                    # Si borne supérieur > à la valeur de la meilleure solution trouvée, explorer noeud
                    if sup > best[1]:
                        nodes, best = bnb(nvar, new_grid_words, dico_values, nodes, (new_node, new_sup), best, uniq)
    return nodes, best


def bounds(grid_words, node, word, dico_values):
    inf = float(dico_values[word])
    for a_word in node[0]:
        inf += float(dico_values[a_word])
    sup = inf
    for variable in grid_words:
        variable_domain = variable.domain.list_words()
        sup += max([float(dico_values[word]) for word in variable_domain])
    return inf, sup


def launch_bnb(grid, dico, uniq=True, mainwindow=None):
    """
    Lance l'algorithme de B&B pour trouver la meilleure solution valuée
    :param grid: Grille sur laquelle est appliqué l'algorithme
    :param dico: dictionnaire comportant les mots et leur valuation
    :param uniq: True si un mot ne peut apparaître qu'une fois dans la grille, False sinon
    :param mainwindow: widget de la fenêtre principale, sert principalement à l'affichage à la fin de la recherche
    """
    a, best = bnb(len(grid.words), grid.words, dico, uniq=uniq)
    if mainwindow:
        if best[0]:
            mainwindow.grid.fill_grid(best[0])
            mainwindow.right_frame.set_to_solved_bnb(True)
        else:
            mainwindow.right_frame.set_to_solved_bnb(False)
        mainwindow.update_grid()


def test_instance():
    t1 = time()
    dico = read_dictionary(sys.argv[1])
    print("Temps de création du dictionnaire : " + str(time() - t1))
    t2 = time()
    dico_values = read_values(sys.argv[1])
    # print (dico_values)
    print("Temps de création du dictionnaire valué: " + str(time() - t2))
    t3 = time()
    grid = read_grid(sys.argv[2])
    grid.set_dictionary(dico)
    print("Temps de création de la grille: " + str(time() - t3))
    t = time()
    n = len(grid.words)
    a, best = bnb(n, grid.words, dico_values, uniq=True)
    print("Temps d'exploration de l'arbre: " + str(time() - t))
    print("Solution optimale " + str(best[0]) + " qui a une valeur égale à " + str(best[1]))
    print("On explore " + str(len(a)) + " noeuds.")
    grid.fill_grid(best[0])
    # for variable in grid.words:
    #    print(variable.domain.list_words())


def test_frequence():
    t1 = time()
    dico, dico_values = read_text_frequency(sys.argv[1])
    print("Temps de création des dictionnaires : " + str(time() - t1))
    t3 = time()
    grid = read_grid(sys.argv[2])
    grid.set_dictionary(dico)
    print("Temps de création de la grille: " + str(time() - t3))
    t = time()
    n = len(grid.grid_to_words())
    print(n, len(dico_values))
    a, best = bnb(n, grid.grid_to_words(), dico_values)
    print("Temps d'exploration de l'arbre: " + str(time() - t))
    print("Solution optimale " + str(best[0]) + " qui a une valeur égale à " + str(best[1]))
    print("On explore " + str(len(a)) + " noeuds.")


def test_mots_androide():
    t1 = time()
    dico, dico_values = read_valued_dictionary(sys.argv[1])
    print("Temps de création des dictionnaires : " + str(time() - t1))
    t3 = time()
    grid = read_grid(sys.argv[2], dico)
    ac3(grid)
    print("Temps de création de la grille: " + str(time() - t3))
    t = time()
    n = len(grid.grid_to_words())
    print(n, len(dico_values))
    a, best = bnb(n, grid.grid_to_words(), dico_values, uniq=False)
    print("Temps d'exploration de l'arbre: " + str(time() - t))
    print("Solution optimale " + str(best[0]) + " qui a une valeur égale à " + str(best[1]))
    print("On explore " + str(len(a)) + " noeuds.")


if __name__ == '__main__':
    # test_instance()
    # test_frequence()
    test_mots_androide()
