# -*- coding: utf-8 -*-

try:
    from tkinter import *
    from tkinter.filedialog import *
except:
    from Tkinter import *
    from tkFileDialog import *


"""
Ici sont toutes les méthodes statiques (indépendante des classes) utiles à l'interface
"""


def choose_file(titre):
    """
    Affiche une fenêtre permettant de choisir un fichier existant
    :param titre: titre de la fenêtre à afficher
    :type titre: str
    :return: chemin absolu du fichier sélectionné
    :rtype: str
    """
    return askopenfilename(title=titre, filetypes=[('txt files', '*.txt'), ('all files', '.*')])
