# -*- coding: utf-8 -*-

try:
    from tkinter import *
except:
    from Tkinter import *
from ihm.statics import choose_file
from os.path import isfile


def affiche_wrong_file(var_test, var_affichage):
    """
    Affiche un message s'il n'y a pas de fichier de chemin relatif voulu
    :param var_test: chemin relatif du fichier
    :param var_affichage: variable à changer pour l'affichage du message
    :type var_test: StringVar
    :type var_affichage: StringVar
    """
    if not isfile(var_test.get()):
        var_affichage.set("Fichier Inexistant")
    else:
        var_affichage.set("")


class ChoixAlgo(Frame):
    """
    Widgets pour le choix de l'algorithme à lancer
    """

    def __init__(self, master):
        Frame.__init__(self, master)
        self.parent = master
        self.choice_buttons()

    def choice_buttons(self):
        """
        Affiche les widgets liés à la grille et l'algorithme à appliquer
        """
        self.choice_dico()
        self.choice_grille()
        self.choice_algo()
        self.choice_heuristique()

    def choice_dico(self):
        """
        Affiche les widgets liés au choix du dictionnaire
        """
        # Définition des variables
        var_dico = StringVar()
        var_wrong_dico = StringVar()
        var_wrong_dico.set("")

        # Définition des widgets
        label = Label(self, text="Choisir un dictionnaire et une grille :", font=("", 16))

        label_dico = Label(self, text="Dictionnaire :")
        entry_dico = Entry(self, textvariable=var_dico)
        btn_dico = Button(self, text="...", command=lambda: var_dico.set(choose_file("Choisir un Dictionnaire")))
        label_wrong_dico = Label(self, textvariable=var_wrong_dico)

        # Affichage des widgets
        label.grid(row=0, column=0, columnspan=4)
        label_dico.grid(row=1, column=0, sticky=E)
        entry_dico.grid(row=1, column=1)
        btn_dico.grid(row=1, column=2)
        label_wrong_dico.grid(row=1, column=3)

        # Affichage d'un message si le fichier est erroné
        var_dico.trace("w",
                       lambda name, index, mode, var_test=var_dico, var_affichage=var_wrong_dico: affiche_wrong_file(
                           var_test, var_affichage))

    def choice_grille(self):
        """
        Affichage des widgets liés au choix de la grille
        """
        # Définition des variables
        var_grille = StringVar()
        var_wrong_grille = StringVar()
        var_wrong_grille.set("")
        if self.parent.parent.grid:
            var_grille.set("Grille affichée")

        # Définition des widgets
        label_grille = Label(self, text="Grille :")
        entry_grille = Entry(self, textvariable=var_grille)
        btn_grille = Button(self, text="...", command=lambda: var_grille.set(choose_file("Choisir une grille")))
        label_wrong_grid = Label(self, textvariable=var_wrong_grille)

        # Affichage des widgets
        label_grille.grid(row=2, column=0, sticky=E)
        entry_grille.grid(row=2, column=1)
        btn_grille.grid(row=2, column=2)
        label_wrong_grid.grid(row=2, column=3)

        # Affichage d'un message si le fichier est erroné
        var_grille.trace("w", lambda name, index, mode, var_test=var_grille,
                                     var_affichage=var_wrong_grille: affiche_wrong_file(var_test, var_affichage))

    def choice_algo(self):
        """
        Affichage des widgets liés au type d'algorithme
        """
        # Définition des variables
        var_ac3 = BooleanVar()
        var_algo = IntVar()

        # Définition des boutons
        check_ac3 = Checkbutton(self, text="Lancer AC3 avant d'appliquer l'algorithme principal ?",
                                variable=var_ac3, onvalue=True, offvalue=False)
        label_algo = Label(self, text="Choisir l'algorithme à appliquer :", font=("", 16))
        radio_rac = Radiobutton(self, text="Retour Arrière Chronologique", variable=var_algo, value=0)
        radio_cbj = Radiobutton(self, text="Conflict Back Jumping", variable=var_algo, value=1)
        radio_rac.select()

        # Affichage des widgets
        label_algo.grid(pady=10, columnspan=4)
        check_ac3.grid(sticky=W, columnspan=4)
        radio_rac.grid(sticky=W, columnspan=4)
        radio_cbj.grid(sticky=W, columnspan=4)

    def choice_heuristique(self):
        """
        Affichage des widgets liés à l'heuristique utilisée pour choisir un mot dans les algorithmes
        """
        # Définition des variables
        var_heur = IntVar()

        # Définition des widgets
        label_heuristique = Label(self, text="Choisir l'heuristique :", font=("", 14))
        radio_next = Radiobutton(self, text="Premier de la liste des mots restants",
                                 variable=var_heur, value=0)
        radio_min_domain = Radiobutton(self, text="Plus petit domaine",
                                       variable=var_heur, value=1)
        radio_max_constraints = Radiobutton(self, text="Plus grand nombre de contraintes binaires",
                                            variable=var_heur, value=2)
        radio_domain_constraints = Radiobutton(self, text="Taille du domaine puis nombre de contraintes",
                                               variable=var_heur, value=3)
        radio_constaints_domain = Radiobutton(self, text="Nombre de contraintes puis taille du domaine",
                                              variable=var_heur, value=4)
        radio_domain_constraints.select()

        # Affichage des widgets
        label_heuristique.grid(pady=10, columnspan=4)
        radio_next.grid(sticky=W, columnspan=4)
        radio_min_domain.grid(sticky=W, columnspan=4)
        radio_max_constraints.grid(sticky=W, columnspan=4)
        radio_domain_constraints.grid(sticky=W, columnspan=4)
        radio_constaints_domain.grid(sticky=W, columnspan=4)
