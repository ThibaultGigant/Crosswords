import sys
from os import getcwd
from copy import copy
from time import time

sys.path.append(getcwd())
from data_gestion.classes import Grid, Tree, Word, deepcopy
from data_gestion.file_gestion import *

def bnb(nvar, grid_words, dico_values, nodes=[], node=([], 0), best=([], 0)):
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
        variable_domain.sort(key=lambda x: dico_values[x], reverse = True)

        # On garde en mémoire les domaines
        domains = {word: deepcopy(word.domain) for word, ind1, ind2 in variable.binary_constraints}
        domains[variable] = deepcopy(variable.domain)

        for word in variable_domain:
            consistant = True

            # Instanciation
            variable.domain = Tree(word)
            modif = variable.update_related_variables_domain()

            if any([w.domain.cardinality() == 0 for w in modif]):
                consistant = False

            for w in modif:
                w.domain = deepcopy(domains[w])

            # Calcule des bornes inf et sup
            inf, sup = bounds(new_grid_words, node, word, dico_values)

            # Ajouter noeud à l'arbre de recherche
            (new_node, new_sup) = (copy(node[0])+[word], sup)
            nodes += [(new_node, new_sup)]
            print (new_node)

            # Verifier consistance
            # Si non consistant, rétablire domaine

            if consistant:
                # Si la valeur trouvée à une feuille > à la valeur de la meilleure solution trouvée, retenir nouvelle solution
                if (len(new_node) == n) and inf > best[1]:
                    best = (new_node, inf)

                # Si borne supérieur > à la valeur de la meilleure solution trouvée, explorer noeud
                if sup > best[1]:
                    nodes, best = bnb(n, new_grid_words, dico_values, nodes, (new_node, new_sup), best)
            else:
                variable.domain = deepcopy(domains[variable])

    return nodes, best

def bounds(grid_words, node, word, dico_values):
    #print node
    inf = float(dico_values[word])
    for a_word in node[0]:
        inf += float(dico_values[a_word])
    sup = inf
    for variable in grid_words:
        variable_domain = variable.domain.list_words()
        sup += max([float(dico_values[word]) for word in variable_domain])
    return inf, sup

def total_nodes(n):
    t_nodes = 0
    for i in range(n):
        t_nodes += 2**(i+1)
    return t_nodes

if __name__ == '__main__':
    t1 = time()
    dico = read_dictionary(sys.argv[1])
    print("Temps de création du dictionnaire : " + str(time()-t1))
    t2 = time()
    dico_values = read_values(sys.argv[1])
    #print (dico_values)
    print("Temps de création du dictionnaire valué: " + str(time()-t2))
    t3 = time()
    grid = read_grid(sys.argv[2])
    grid.set_dictionary(dico)
    print("Temps de création de la grille: " + str(time()-t3))
    t = time()
    n = len(grid.grid_to_words())
    a, best = bnb(n, grid.grid_to_words(), dico_values)
    print("Temps d'exploration de l'arbre: " + str(time()-t))
    print("Solution optimale " + str(best[0]) + " qui a une valeur égale à " + str(best[1]))
    print("On explore " + str(len(a)) + " noeuds.")