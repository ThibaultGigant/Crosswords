import sys
from unicodedata import normalize


class Grid:
    """
    Classe représentant une grille de mots croisés
    """

    def __init__(self, grid, dictionary):
        """
        Constructeur
        :param grid: grille récupérée directement à partir du fichier, non transformée (liste de listes de str)
        :param dictionary: dictionnaire contenant tous les mots, triés par nombre de lettres des mots
        """
        self.grid = grid
        self.dictionary = dictionary
        self.constraints = []
        self.words = self.grid_to_words()

    def grid_to_words(self):
        """
        Méthode prenant la grille totale et retournant tous les mots à trouver dans cette grille
        :return: liste de mots de la grille
        :rtype: list
        """
        words_list = []

        # Détection des mots horizontaux
        print("horizontal")
        for line in range(self.get_height()):
            i = 0
            while i < self.get_width():
                if self.grid[line][i] != '1':
                    start = i
                    while i < self.get_width() and self.grid[line][i] != '1':
                        i += 1
                    if i > start + 2:  # On rajoute un mot que s'il fait plus de 2 lettres
                        words_list.append(Word(i - start, self.dictionary, (line, start), True))
                i += 1

        print("vertical")
        # Détection des mots verticaux
        for line in range(self.get_height()):
            for letter in range(self.get_width()):
                if self.grid[line][letter] != '1' and (line == 0 or (line > 0 and self.grid[line-1][letter] == '1')):
                    i = line
                    while i < self.get_height() and self.grid[i][letter] != '1':
                        i += 1
                    if i > line + 2:  # On rajoute un mot que s'il fait plus de 2 lettres
                        words_list.append(Word(i - line, self.dictionary, (line, letter), False))

        print("contraintes unaires")
        # Ajout des contraintes unaires : s'il y a déjà des lettres dans la grille
        for word in words_list:
            coord = word.coord
            length = word.length
            for i in range(length):
                if word.horizontal and self.grid[coord[0]][coord[1] + i] not in ['0', '1']:
                    letter = normalize("NFKD",
                                       self.grid[coord[0]][coord[1] + i]).encode("ascii", "ignore").decode("ascii")
                    word.add_unary_constaint(i, letter)
                if (not word.horizontal) and self.grid[coord[0] + i][coord[1]] not in ['0', '1']:
                    letter = normalize("NFKD",
                                       self.grid[coord[0] + i][coord[1]]).encode("ascii", "ignore").decode("ascii")
                    word.add_unary_constaint(i, letter)

        print("contraintes binaires")
        # Ajout des contraintes binaires (entre deux mots)
        for word1 in range(len(words_list)-1):
            for word2 in range(word1 + 1, len(words_list)):
                commons = set(words_list[word1].list_coordinates).intersection(set(words_list[word2].list_coordinates))
                if commons:
                    for coord in commons:
                        coord1 = words_list[word1].list_coordinates.index(coord)
                        coord2 = words_list[word2].list_coordinates.index(coord)
                        self.add_constraint(words_list[word1], words_list[word2], coord1, coord2)

        return words_list

    def add_constraint(self, word1, word2, letter_index1, letter_index2):
        """
        Ajout d'une contrainte entre les mots passés en paramètre
        :param word1: mot ayant une lettre commune avec word2
        :param word2: mot ayant une lettre commune avec word1
        :param letter_index1: indice de la lettre commune dans word1
        :param letter_index2: indice de la lettre commune dans word2
        :type word1: Word
        :type word2: Word
        """
        word1.add_binary_constraint(word2, letter_index1, letter_index2)
        word2.add_binary_constraint(word1, letter_index2, letter_index1)
        self.constraints.append((word1, word2, letter_index1, letter_index2))

    def get_width(self):
        """
        Donne la largeur de la grille
        :return: largeur de la grille
        :rtype: int
        """
        if self.grid:
            return len(self.grid[0])
        else:
            return 0

    def get_height(self):
        """
        Donne la hauteur de la grille
        :return: hauteur de la grille
        :rtype: int
        """
        if self.grid:
            return len(self.grid)
        else:
            return 0

    def get_words_count(self):
        """
        Renvoie le nombre de mots dans la grille
        :return: nombre de mots dans la grille
        :rtype: int
        """
        return len(self.words)

    def __str__(self):
        """
        Affichage de la grille
        """
        res = ""
        for i in self.words:
            res += i.__str__() + "\n"
        return res


class Word:
    """
    Classe représentant les mots contenus dans une grille
    """
    word_id = 0

    def __init__(self, length, dictionary, coord, horizontal):
        """
        Constructeur
        :param length: longueur du mot
        :param dictionary: dictionnaire pour créer domaine
        :param coord: coordonnées (ligne, colonne) de la première lettre dans la grille
        :param horizontal: True si le mot est horizontal dans la grille, False sinon
        :type length: int
        :type dictionary: dict
        :type coord: tuple
        :type horizontal: bool
        :return: 
        """
        self.length = length
        self.domain = dictionary[length]
        self.coord = coord
        self.horizontal = horizontal
        self.binary_constraints = []  # liste de tuples de contraintes binaires : (word, index of common letter)
        self.unary_constraints = []  # liste de tuples de contraintes unaires : (word, index of common letter)
        self.list_coordinates = [(coord[0], coord[1] + i) if horizontal else (coord[0] + i, coord[1]) for i in range(length)]
        self.id = Word.word_id
        Word.word_id += 1


    def __str__(self):
        """
        Affichage
        """
        res = "Mot d'ID : " + str(self.id) + "\n"
        res += "Longueur : " + str(self.length) + "\n"
        res += "Débute en " + str(self.coord) + "\n"
        res += "Horizontal\n" if self.horizontal else "Vertical\n"
        res += "Liste coordonnées : " + str(self.list_coordinates) + "\n"
        if self.unary_constraints:
            res += "Contraintes unaires :\n"
            for i in self.unary_constraints:
                res += str(i) + "\n"
        if self.binary_constraints:
            res += "Contraintes binaires :\n"
            for word, letter1, letter2 in self.binary_constraints:
                res += str(word.id) + ", " + str(letter1) + ", " + str(letter2) + "\n"

        return res

    def add_binary_constraint(self, word, letter_index1, letter_index2):
        """
        Ajout d'une contrainte entre le mot passé en paramètre et le mot courant
        :param word: mot ayant une lettre commune avec le mot courant
        :param letter_index1: indice de la lettre commune dans le mot courant
        :param letter_index2: indice de la lettre commune dans word
        """
        self.binary_constraints.append((word, letter_index1, letter_index2))
        
    def add_unary_constaint(self, letter_index, letter):
        """
        Ajout d'une contrainte sur une lettre du mot : en fait on fixe une lettre du mot
        :param letter_index: indice de la lettre dans le mot
        :param letter: lettre à fixer dans le mot
        :type letter_index: int
        :type letter: str
        """
        self.unary_constraints.append((letter_index, letter))
