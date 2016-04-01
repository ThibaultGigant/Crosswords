# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.messagebox import askyesno
from os.path import isfile
from ihm.statics import choose_file
from data_gestion.file_gestion import write_partially_solved_grid


class SolvingButtons(Frame):
    """
    Widgets affichés lors de l'exécution d'un algorithme
    """

    def __init__(self, master, event):
        Frame.__init__(self, master)
        self.parent = master
        self.outfile = StringVar()
        self.next_btn = Button(self, text="Next", command=event.set) if event else None
        self.save_btn = Button(self, text="Enregistrer la grille en l'état", command=self.save_grid)
        self.label_file = Label(self, text="Fichier de sortie :")
        self.entry_file = Entry(self, textvariable=self.outfile)
        self.btn_file = Button(self, text="...",
                               command=lambda: self.outfile.set(choose_file("Choisir un Fichier de sortie")))
        self.btn_save = Button(self, text="Enregistrer la grille en l'état", command=self.verify_and_save)
        self.display_buttons()

    def display_buttons(self):
        if self.next_btn:
            self.next_btn.grid(row=0, columnspan=3)
        self.save_btn.grid(row=1, columnspan=3)

    def save_grid(self):
        """
        Lance l'enregistrement de la grille courante dans un fichier
        """
        self.save_btn.destroy()

        self.label_file.grid(row=1, column=0)
        self.entry_file.grid(row=1, column=1)
        self.btn_file.grid(row=1, column=2)
        self.btn_save.grid(row=2, columnspan=3)

    def verify_and_save(self):
        """
        Vérifie que le fichier est bon et lance la sauvegarde
        """
        if isfile(self.outfile.get()):
            if not askyesno("Fichier existant",
                            "Le fichier " + self.outfile.get() + " existe déjà, la procédure effacera son contenu, voulez-vous vraiment choisir ce fichier ?"):
                return

        write_partially_solved_grid(self.outfile.get(), self.parent.parent.grid)

        self.label_file.destroy()
        self.entry_file.destroy()
        self.btn_file.destroy()
        self.btn_save.destroy()

        self.save_btn = Button(self, text="Enregistrer la grille en l'état", command=self.save_grid)
        self.save_btn.grid(row=1, columnspan=3)
