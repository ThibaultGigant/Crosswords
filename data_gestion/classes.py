import sys
from os import getcwd
sys.path.append(getcwd())
from unicodedata import normalize
from copy import deepcopy


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
        self.constraints = []  # type: list[(Word, Word, int, int)]
        self.words = self.grid_to_words()

    def grid_to_words(self):
        """
        Méthode prenant la grille totale et retournant tous les mots à trouver dans cette grille
        :return: liste de mots de la grille
        :rtype: list[Word]
        """
        words_list = []

        # Détection des mots horizontaux
        for line in range(self.get_height()):
            i = 0
            while i < self.get_width():
                if self.grid[line][i] != '1':
                    start = i
                    while i < self.get_width() and self.grid[line][i] != '1':
                        i += 1
                    if i >= start + 2:  # On rajoute un mot que s'il fait plus de 2 lettres
                        words_list.append(Word(i - start, self.dictionary, (line, start), True))
                i += 1

        # Détection des mots verticaux
        for line in range(self.get_height()):
            for letter in range(self.get_width()):
                if self.grid[line][letter] != '1' and (line == 0 or (line > 0 and self.grid[line-1][letter] == '1')):
                    i = line
                    while i < self.get_height() and self.grid[i][letter] != '1':
                        i += 1
                    if i >= line + 2:  # On rajoute un mot que s'il fait plus de 2 lettres
                        words_list.append(Word(i - line, self.dictionary, (line, letter), False))

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
        :type dictionary: dict[int, Tree]
        :type coord: tuple
        :type horizontal: bool
        :return: 
        """
        self.length = length
        self.domain = deepcopy(dictionary[length])
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
        :type word: Word
        :type letter_index1: int
        :type letter_index2: int
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

    def respect_unary_constraints(self):
        """
        Ecume le domaine du mot par rapport à ses contraintes unaires
        :return: True si le domaine du mot n'est pas vide après écumage, False sinon
        """
        for constraint in self.unary_constraints:
            self.domain.respect_unary_constraints(constraint[0], [constraint[1]])
        return not self.domain.is_empty()

    def respect_binary_constraint(self, word, letter_index1, letter_index2):
        """
        Ecume le domaine du mot courant en fonction du mot passé en paramètre et des contraintes d'indices
        :param word: mot avec lequel il y a contrainte
        :param letter_index1: indice de la lettre commune dans le mot courant
        :param letter_index2: indice de la lettre commune dans le mot passé en paramètre
        :return: True si le domaine a été modifié, false sinon
        :rtype: bool
        """
        modif = False
        this_letters = self.domain.letters_at_index(letter_index1)
        other_letters = word.domain.letters_at_index(letter_index2)
        union_letters = this_letters.intersection(other_letters)

        # print(this_letters, other_letters, union_letters)

        if this_letters != union_letters:
            self.domain.respect_unary_constraints(letter_index1, union_letters)
            modif = True
        if other_letters != union_letters:
            word.domain.respect_unary_constraints(letter_index2, union_letters)
            modif = True

        return modif

    def respect_binary_constraints(self):
        """
        Ecume le domaine du mot par rapport à ses contraintes binaires
        :return: True si un domaine a été modifié, False sinon
        :rtype: bool
        """
        modif = []
        for constraint in self.binary_constraints:
            modif.append(self.respect_binary_constraint(constraint[0], constraint[1], constraint[2]))
        return any(modif)


class Tree:
    """
    Classe basique d'arbre, pour les besoins du stockage des domaines
    """

    def __init__(self, word, level=0, children=None):
        """
        Constructeur
        :param word: mot contenu dans l'arbre
        :param children: dictionnaire recensant les fils, la clé étant la data de l'arbre fils
        :type word: str
        :type children: dict[str, Tree]
        :return:
        """
        self.children = children if children else {}
        self.level = level
        if level == 0:
            self.data = ""
            self.add_word(word)
        else:
            if word:
                self.data = word[0]
                self.add_word(word[1:])
            else:
                self.data = ""
                self.add_word("")

    def get_data(self):
        """
        Retourne la donnée stockée à ce noeud
        :return:
        """
        return self.data

    def add_word(self, word):
        """
        Ajoute le mot à l'arbre courant
        :param word: mot à rajouter à l'arbre
        :type word: str
        """
        if word and word[0] not in self.children:
            self.children[word[0]] = Tree(word, level=self.level + 1)
        elif word and word[0] in self.children:
            self.children[word[0]].add_word(word[1:])
        else:
            self.children[""] = None

    def cardinality(self):
        """
        Donne le nombre de mots contenus dans l'arbre, c'est-à-dire le nombre de feuilles
        :return: nombre de mots contenus dans l'arbre
        :rtype: int
        """
        return sum([1 if not tree else tree.cardinality() for tree in self.children.values()])

    def list_words(self):
        """
        Renvoie la liste des mots contenus dans le graphe
        :return: la liste des mots contenus dans le graphe
        :rtype: list[str]
        """
        if self.children:
            res = []
            for child in self.children.values():
                if child:
                    for word in child.list_words():
                        res.append(self.data + word)
                else:
                    res.append(self.data)
            res.sort()
            return res
        else:
            return [self.data]

    def respect_unary_constraints(self, letter_index, letters_list):
        """
        Ecume le domaine pour respecter la contrainte
        :param letter_index: indice de la lettre dans le mot à respecter
        :param letters_list: liste de lettres acceptées à cet indice
        :type letter_index: int
        :type letters_list: list[str]
        :return: True si après écumage, le noeud courant n'a plus de fils, False sinon
        :rtype: bool
        """
        # Si on est au niveau demandé, on regarde les lettres contenues dans les enfants
        if self.level == letter_index:
            if self.children:
                letters = []
                for letter in self.children.keys():
                    if letter not in letters_list:
                        letters.append(letter)
                for letter in letters:
                    del self.children[letter]
                if not self.children:
                    return True
        # sinon on appelle récursivement sur les enfants, en vérifiant bien que c'est possible
        else:
            if self.children:
                letters = []
                for letter, child in self.children.items():
                    if child and child.respect_unary_constraints(letter_index, letters_list):
                        letters.append(letter)
                for letter in letters:
                    del self.children[letter]
                if not self.children or list(self.children.keys()) == [""]:
                    return True
        return False

    def letters_at_index(self, letter_index):
        """
        Renvoie la liste de toutes les lettres à l'indice demandé dans les mots contenus dans l'arbre
        :param letter_index: indice de la lettre dans le mot
        :type letter_index: int
        :return: liste des lettres
        :rtype: set[str]
        """
        if self.level == letter_index:
            if self.children:
                return set(self.children.keys())
        else:
            if self.children:
                res = set([])
                for child in self.children.values():
                    if child:
                        temp = child.letters_at_index(letter_index)
                        if temp:
                            res = res.union(temp)
                if res:
                    return set(res)
        return set([])

    def is_empty(self):
        """
        Détermine si l'arbre est vide ou non
        :return: True si l'arbre est vide, False sinon
        """
        return (not self.children) or list(self.children.keys()) == [""]


def test_tree():
    t = Tree("representative")
    t.add_word("test")
    t.add_word("representant")
    print(t.list_words(), t.cardinality())
    t.respect_unary_constraints(2, ["p", "s", "i"])
    print(t.list_words())
    print(t.letters_at_index(10))


def test_contraintes():
    t1 = Tree("top")
    t1.add_word("tap")
    t1.add_word("tou")
    t1.add_word("cou")
    t1.add_word("car")

    t2 = Tree("four")
    t2.add_word("cour")
    t2.add_word("sour")
    t2.add_word("soir")

    dico = {3: t1, 4: t2}

    w1 = Word(3, dico, (0, 0), True)
    w2 = Word(4, dico, (0, 0), True)

    w1.add_unary_constaint(0, "c")
    print(w1.domain.list_words())
    w1.respect_unary_constraints()
    print(w1.domain.list_words())

    w1.add_binary_constraint(w2, 1, 1)
    w2.add_binary_constraint(w1, 1, 1)
    print("Avant modification des domaines par respect des contraintes binaires")
    print(w1.domain.list_words())
    print(w2.domain.list_words())

    modif = w1.respect_binary_constraints()
    print("Après modification des domaines par respect des contraintes binaires 1 1")
    print(modif)
    print(w1.domain.list_words())
    print(w2.domain.list_words())

    w1.add_binary_constraint(w2, 0, 0)
    w2.add_binary_constraint(w1, 0, 0)
    modif = w1.respect_binary_constraints()
    print("Après modification des domaines par respect des contraintes binaires 0 0")
    print(modif)
    print(w1.domain.list_words())
    print(w2.domain.list_words())
    print("Après modification des domaines par respect des contraintes binaires 0 0")
    modif = w1.respect_binary_constraints()
    print(modif)
    print(w1.domain.list_words())
    print(w2.domain.list_words())


if __name__ == '__main__':
    test_tree()
    test_contraintes()