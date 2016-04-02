import sys
from os import getcwd
from time import time, sleep

sys.path.append(getcwd())
from data_gestion.classes import Grid, deepcopy, Tree, Word
from data_gestion.file_gestion import *
from algorithms.arc_consistency import ac3
from algorithms.heuristics import *
from copy import deepcopy as deep

def CBJ(grid, heuristic_function, uniq=True, stop=None, mainwindow=None, first_call=True):
    """
    Conflict BackJumping
    :param grid: grille sur laquelle on lance l'algorithme
    :param heuristic_function: fonction heuristique qui détermine quel mot sera instancié à chaque itération
    :type grid: Grid
    :return: Ensemble de variables "en conflit" s'il y en a
    :rtype: set
    """
    # print("Mots restants à instancier : " + str(len(grid.uninstanciated_words)))
    if not grid.uninstanciated_words:
        # Affichage graphique
        if mainwindow:
            mainwindow.display_grid()
            sleep(0.05)
            mainwindow.display_done(True)
        return set([])

    conflit = set([])

    xk = heuristic_function(grid.uninstanciated_words)  # Prochaine variable à instancier
    grid.uninstanciated_words.remove(xk)
    grid.instanciated_words.append(xk)

    # On garde en mémoire les domaines qui pourraient être modifiés
    domains = {word: deepcopy(word.domain) for word, ind1, ind2 in xk.binary_constraints}
    domains[xk] = deepcopy(xk.domain)

    words = xk.domain.list_words()
    # Si le domaine est vide, alors on s'est fait vider avant par un mot instancié
    if words == [""]:
        grid.instanciated_words.remove(xk)
        grid.uninstanciated_words.insert(0, xk)
        if first_call and mainwindow:
            mainwindow.display_done(False)
        return set([w for (w, ind1, ind2) in xk.binary_constraints if w in grid.instanciated_words])

    for word in words:
        # print("Essai instanciation mot " + str(xk.id) + " en " + word)
        xk.domain = Tree(word)

        # Affichage graphique
        if mainwindow:
            mainwindow.display_grid()
            sleep(0.05)
        if stop:
            stop.wait()
            stop.clear()

        # forward check avec récupèration des mots dont les domaines ont été modifiés
        modif = xk.update_related_variables_domain()
        conflit_local = set([w for w in modif if w in grid.instanciated_words])  # ne devrait jamais arriver à cause du FC

        if uniq:
            same_size_words = [w for w in grid.uninstanciated_words if w.length == xk.length]
            same_modif = []
            for w in same_size_words:
                if w.domain.remove_word(word) and w not in modif:
                    same_modif.append(w)
        if not conflit_local:
            conflit_fils = CBJ(grid, heuristic_function, uniq, stop, mainwindow, first_call=False)

            if xk in conflit_fils:
                conflit_fils.remove(xk)
                if conflit_fils:
                    conflit = conflit.union(conflit_fils)
                else:
                    conflit = conflit.union(set([w for (w, ind1, ind2) in xk.binary_constraints if w in grid.instanciated_words]))
            else:
                conflit = conflit_fils
                if conflit:
                    # rétablissement des domaines
                    for w in modif:
                        w.domain = deepcopy(domains[w])
                    if uniq:
                        for w in same_modif:
                            w.domain.add_word(word)
                break
        else:
            conflit = conflit.union(conflit_local)
        # rétablissement des domaines
        for w in modif:
            w.domain = deepcopy(domains[w])
        if uniq:
            for w in same_modif:
                w.domain.add_word(word)

    if conflit:
        xk.domain = deepcopy(domains[xk])
        grid.instanciated_words.remove(xk)
        grid.uninstanciated_words.insert(0, xk)
        if first_call and mainwindow:
            mainwindow.display_done(False)
    return conflit


def CBJ_without_FC(grid, heuristic_function, uniq=True, stop=None, mainwindow=None, first_call=True):
    """
    Conflict BackJumping
    :param grid: grille sur laquelle on lance l'algorithme
    :param heuristic_function: fonction heuristique qui détermine quel mot sera instancié à chaque itération
    :type grid: Grid
    :return: Ensemble de variables "en conflit" s'il y en a
    :rtype: set
    """
    # print("Mots restants à instancier : " + str(len(grid.uninstanciated_words)))
    if not grid.uninstanciated_words:
        # print("HIT!!!!!!!!!!!!!")
        # Affichage graphique
        if mainwindow:
            mainwindow.display_grid()
            sleep(0.05)
            mainwindow.display_done(True)
        return set([])

    conflit = set([])

    xk = heuristic_function(grid.uninstanciated_words)  # Prochaine variable à instancier
    grid.uninstanciated_words.remove(xk)
    grid.instanciated_words.append(xk)

    # On garde en mémoire les domaines qui pourraient être modifiés
    domain = deepcopy(xk.domain)

    words = xk.domain.list_words()
    # Si le domaine est vide, alors on s'est fait vider avant par un mot instancié
    if words == [""]:
        # print("Going back from " + str(xk.id) + " car domaine vide")
        grid.instanciated_words.remove(xk)
        grid.uninstanciated_words.insert(0, xk)
        if first_call and mainwindow:
            mainwindow.display_done(False)
        return set([w for (w, ind1, ind2) in xk.binary_constraints if w in grid.instanciated_words])

    for word in words:
        # print("Essai instanciation mot " + str(xk.id) + " en " + word)
        xk.domain = Tree(word)

        # Affichage graphique
        if mainwindow:
            mainwindow.display_grid()
            sleep(0.05)
        if stop:
            stop.wait()
            stop.clear()

        # Vérification de la consistance et récupération des conflits locaux
        conflit_local = set(xk.consistant(grid.instanciated_words))
        if uniq:
            same_size_instanciated_words = [w for w in grid.instanciated_words if w.domain.contains(word) and w != xk]
            conflit_local = conflit_local.union(set(same_size_instanciated_words))

        # print("conflit local : " + str([w.id for w in conflit_local]))
        if not conflit_local:
            conflit_fils = CBJ_without_FC(grid, heuristic_function, uniq, stop, mainwindow, first_call=False)

            if xk in conflit_fils:
                conflit_fils.remove(xk)
                if conflit_fils:
                    conflit = conflit.union(conflit_fils)
                else:
                    conflit = conflit.union(set([w for (w, ind1, ind2) in xk.binary_constraints if w in grid.instanciated_words]))
            else:
                conflit = conflit_fils
                break
        else:
            conflit = conflit.union(conflit_local)

    if conflit:
        xk.domain = deepcopy(domain)
        grid.instanciated_words.remove(xk)
        grid.uninstanciated_words.insert(0, xk)
        if first_call and mainwindow:
            mainwindow.display_done(False)
    # print("Going back from " + str(xk.id))
    # print("conflits : " + str([w.id for w in conflit]))
    return conflit


if __name__ == '__main__':
    t1 = time()
    dico = read_dictionary(sys.argv[1])
    print("Temps de création du dictionnaire : " + str(time()-t1))
    t = time()
    grid1 = read_grid(sys.argv[2], dico)
    print("Temps de création de la grille: " + str(time()-t))
    grid2 = deep(grid1)
    t = time()
    ac3(grid2)
    res = CBJ_without_FC(grid2, heuristic_size_and_constraints, True)
    print("Temps de calcul de l'algo : " + str(time()-t))
    print([w.id for w in res])
    if not res:
        instanciation = [(w.id, w.domain.list_words()) for w in grid2.instanciated_words]
        instanciation.sort(key=lambda x: x[0])
        print(instanciation)

    t = time()
    ac3(grid1)
    res = CBJ(grid1, heuristic_size_and_constraints, True)

    print("Temps de calcul de l'algo : " + str(time() - t))
    print("Temps total : " + str(time()-t1))
    print([w.id for w in res])
    if not res:
        instanciation = [(w.id, w.domain.list_words()) for w in grid1.instanciated_words]
        instanciation.sort(key=lambda x: x[0])
        print(instanciation)
