# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.messagebox import showerror
from ihm.statics import choose_file
from os.path import isfile
from threading import Thread, Event
from data_gestion.file_gestion import *
from algorithms.arc_consistency import ac3
from algorithms.heuristics import *
from algorithms.rac2 import backtrack
from algorithms.cbj import CBJ


# Variables globales
heuristic = {
    0: heuristic_next,
    1: heuristic_min_domain,
    2: heuristic_max_constraints,
    3: heuristic_size_and_constraints,
    4: heuristic_constraints_and_size,
    5: heuristics_max_constraints_with_instanciated
}


class ChoixAlgo(Frame):
    """
    Widgets pour le choix de l'algorithme à lancer
    """

    def __init__(self, master):
        Frame.__init__(self, master)
        self.parent = master
        # Définition de variables
        self.var_dico = StringVar()
        self.var_wrong_dico = StringVar()
        self.var_grille = StringVar()
        self.var_wrong_grille = StringVar()
        self.var_ac3 = BooleanVar()
        self.var_uniq = BooleanVar()
        self.var_algo = IntVar()
        self.var_heur = IntVar()
        self.var_step_by_step = BooleanVar()
        self.down_button = None
        self.dico = None

        self.choice_buttons()

    def choice_buttons(self):
        """
        Affiche les widgets liés à la grille et l'algorithme à appliquer
        """
        self.choice_dico()
        self.choice_grille()
        self.choice_algo()
        self.choice_heuristique()
        self.launch_button()

    def choice_dico(self):
        """
        Affiche les widgets liés au choix du dictionnaire
        """
        # Définition des variables
        self.var_wrong_dico.set("")

        # Définition des widgets
        label = Label(self, text="Choisir un dictionnaire et une grille :", font=("", 16))

        label_dico = Label(self, text="Dictionnaire :")
        entry_dico = Entry(self, textvariable=self.var_dico)
        btn_dico = Button(self, text="...", command=lambda: self.var_dico.set(choose_file("Choisir un Dictionnaire")))
        label_wrong_dico = Label(self, textvariable=self.var_wrong_dico)

        # Affichage des widgets
        label.grid(row=0, column=0, columnspan=4)
        label_dico.grid(row=1, column=0, sticky=E)
        entry_dico.grid(row=1, column=1)
        btn_dico.grid(row=1, column=2)
        label_wrong_dico.grid(row=1, column=3)

        # Affichage d'un message si le fichier est erroné
        self.var_dico.trace("w", lambda name, index, mode, var_test=self.var_dico, var_affichage=self.var_wrong_dico: self.affiche_wrong_dico(var_test, var_affichage))

    def choice_grille(self):
        """
        Affichage des widgets liés au choix de la grille
        """
        # Définition des variables
        self.var_wrong_grille.set("")
        if self.parent.parent.grid:
            self.var_grille.set("Grille affichée")

        # Définition des widgets
        label_grille = Label(self, text="Grille :")
        entry_grille = Entry(self, textvariable=self.var_grille)
        btn_grille = Button(self, text="...", command=lambda: self.var_grille.set(choose_file("Choisir une grille")))
        label_wrong_grid = Label(self, textvariable=self.var_wrong_grille)

        # Affichage des widgets
        label_grille.grid(row=2, column=0, sticky=E)
        entry_grille.grid(row=2, column=1)
        btn_grille.grid(row=2, column=2)
        label_wrong_grid.grid(row=2, column=3)

        # Affichage d'un message si le fichier est erroné
        self.var_grille.trace("w", lambda name, index, mode, var_test=self.var_grille, var_affichage=self.var_wrong_grille: self.affiche_wrong_grid(var_test, var_affichage))

    def choice_algo(self):
        """
        Affichage des widgets liés au type d'algorithme
        """
        # Définition des boutons
        check_ac3 = Checkbutton(self, text="Lancer AC3 avant d'appliquer l'algorithme principal ?",
                                variable=self.var_ac3, onvalue=True, offvalue=False)
        check_uniq = Checkbutton(self, text="Apparition unique d'un mot ?",
                                 variable=self.var_uniq, onvalue=True, offvalue=False)
        label_algo = Label(self, text="Choisir l'algorithme à appliquer :", font=("", 16))
        radio_rac = Radiobutton(self, text="Retour Arrière Chronologique", variable=self.var_algo, value=0)
        radio_cbj = Radiobutton(self, text="Conflict Back Jumping", variable=self.var_algo, value=1)
        radio_rac.select()

        # Affichage des widgets
        label_algo.grid(pady=10, columnspan=4)
        check_ac3.grid(sticky=W, columnspan=4)
        check_uniq.grid(sticky=W, columnspan=4)
        radio_rac.grid(sticky=W, columnspan=4)
        radio_cbj.grid(sticky=W, columnspan=4)

    def choice_heuristique(self):
        """
        Affichage des widgets liés à l'heuristique utilisée pour choisir un mot dans les algorithmes
        """
        # Définition des widgets
        label_heuristique = Label(self, text="Choisir l'heuristique :", font=("", 14))
        radio_next = Radiobutton(self, text="Premier de la liste des mots restants",
                                 variable=self.var_heur, value=0)
        radio_min_domain = Radiobutton(self, text="Plus petit domaine",
                                       variable=self.var_heur, value=1)
        radio_max_constraints = Radiobutton(self, text="Plus grand nombre de contraintes binaires",
                                            variable=self.var_heur, value=2)
        radio_domain_constraints = Radiobutton(self, text="Min taille du domaine puis nombre de contraintes",
                                               variable=self.var_heur, value=3)
        radio_constaints_domain = Radiobutton(self, text="Plus de contraintes puis min taille du domaine",
                                              variable=self.var_heur, value=4)
        radio_constraints_instanciated = Radiobutton(self, text="Plus de contraintes avec un instancié puis min taille",
                                                     variable=self.var_heur, value=5)

        radio_domain_constraints.select()

        # Affichage des widgets
        label_heuristique.grid(pady=10, columnspan=4)
        radio_next.grid(sticky=W, columnspan=4)
        radio_min_domain.grid(sticky=W, columnspan=4)
        radio_max_constraints.grid(sticky=W, columnspan=4)
        radio_domain_constraints.grid(sticky=W, columnspan=4)
        radio_constaints_domain.grid(sticky=W, columnspan=4)
        radio_constraints_instanciated.grid(sticky=W, columnspan=4)

    def launch_button(self):
        """
        Ajout du bouton qui lance l'algorithme
        """
        check_step_by_step = Checkbutton(self, text="Affichage étape par étape avec attente de clic ?",
                                         variable=self.var_step_by_step, onvalue=True, offvalue=False)
        self.down_button = Button(self, text="Lancer l'algorithme !", command=self.launch_algo)
        check_step_by_step.grid(columnspan=4, sticky=W)
        self.down_button.grid(columnspan=4)

    def launch_algo(self):
        """
        Lancement de l'algorithme avec les valeurs souhaitées
        """
        # Vérification que tout est bien entré et chargé
        if self.var_dico.get() == "" or self.var_wrong_dico.get() != "":
            showerror("Erreur Dictionnaire", "Veuillez choisir un fichier de dictionnaire correct")
            return
        if not self.dico:
            showerror("Erreur Dictionnaire", "Veuillez attendre le chargement du dictionnaire")
            return
        if self.var_grille.get() == "" or self.var_wrong_grille.get() != "":
            showerror("Erreur Grille", "Veuillez choisir un fichier de grille correct")
            return
        if not self.parent.grid:
            showerror("Erreur Grille", "Veuillez attendre le chargement de la grille")
            return

        # Récupération des variables qui nous intéressent
        if self.var_ac3:
            ac3(self.parent.parent.grid)

        if self.var_step_by_step.get():
            # On crée l'événement à suivre si on veut faire du step by step
            event = Event()
            self.parent.parent.left_frame.set_button_next(event)
        else:
            event = None

        # Création d'un thread pour les algorithmes à lancer
        if self.var_algo.get() == 0:
            thread = Thread(None, backtrack, None, (self.parent.parent.grid, heuristic[self.var_heur.get()]),
                            {"uniq": self.var_uniq.get(), "stop": event, "mainwindow": self.parent.parent})
        else:
            thread = Thread(None, CBJ, None, (self.parent.parent.grid, heuristic[self.var_heur.get()]),
                            {"uniq": self.var_uniq.get(), "stop": event, "mainwindow": self.parent.parent})
        # Lancement du thread qui fera les calculs et l'affichage
        thread.daemon = True
        thread.start()
        self.parent.set_to_solving(event)

    def affiche_wrong_dico(self, var_test, var_affichage):
        """
        Affiche un message s'il n'y a pas de fichier de chemin relatif voulu
        :param var_test: chemin relatif du fichier
        :param var_affichage: variable à changer pour l'affichage du message
        :type var_test: StringVar
        :type var_affichage: StringVar
        """
        self.dico = None
        if not isfile(var_test.get()):
            var_affichage.set("Fichier Inexistant")
        else:
            var_affichage.set("")
            thread = Thread(None, self.read_dico)
            thread.start()

    def read_dico(self):
        """
        Essaie de lire le dictionnaire en argument
        """
        try:
            self.dico = read_dictionary(self.var_dico.get())
        except IOError:
            showerror("Erreur Dictionnaire", "Le fichier donné n'est pas un dictionnaire correct")
            return
        if self.parent.parent.grid:
            self.parent.parent.grid.set_dictionary(self.dico)

    def affiche_wrong_grid(self, var_test, var_affichage):
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
            thread = Thread(None, self.read_grid)
            thread.start()

    def read_grid(self):
        """
        Essaie de lire le dictionnaire en argument
        """
        try:
            grid = read_grid(self.var_grille.get())
        except IOError:
            showerror("Erreur Grille", "Le fichier donné n'est pas une grille correcte")
            return
        if self.dico:
            grid.set_dictionary(self.dico)
        self.parent.parent.grid = grid
        self.parent.parent.display_grid()
