from random import choice


def heuristic_next(words):
    """
    Retourne la première variable parmi celles qui ne sont pas encore instanciée
    :param domain: liste de mots
    """
    return words[0]


def heuristic_max_constraints(words):
    """
    Retourne le mot qui a le plus de contraintes binaires
    :param words: liste de mots
    :type words: list[Word]
    :rtype: Word
    """
    nb_constraints = [len(i.binary_constraints) for i in words]
    max_constraints = max(nb_constraints)
    indices = [i for i, j in enumerate(nb_constraints) if j == max_constraints]
    return words[choice(indices)]


def heuristic_min_domain(words):
    """
    Retourne le mot qui a le plus petit domaine
    :param words: liste de mots
    :type words: list[Word]
    :rtype: Word
    """
    domains_size = [word.domain.cardinality() for word in words]
    min_domain = min(domains_size)
    indices = [i for i, j in enumerate(domains_size) if j == min_domain]
    return words[choice(indices)]


def heuristic_constraints_and_size(words):
    """
    Retourne le mot qui a le plus de contraintes binaires,
    en cas d'égalité celui d'entre eux qui a le plus petit domaine,
    en cas d'égalité on en choisit un au hasard
    :param words: liste de mots
    :type words: list[Word]
    :rtype: Word
    """
    nb_constraints = [len(i.binary_constraints) for i in words]
    max_constraints = max(nb_constraints)
    indices = [i for i, j in enumerate(nb_constraints) if j == max_constraints]
    if len(indices) > 1:
        return heuristic_min_domain([words[i] for i in indices])
    return words[choice(indices)]


def heuristic_size_and_constraints(words):
    """
    Retourne le mot qui a le plus de contraintes binaires,
    en cas d'égalité celui d'entre eux qui a le plus petit domaine,
    en cas d'égalité on en choisit un au hasard
    :param words: liste de mots
    :type words: list[Word]
    :rtype: Word
    """
    domains_size = [word.domain.cardinality() for word in words]
    min_domain = min(domains_size)
    indices = [i for i, j in enumerate(domains_size) if j == min_domain]
    if len(indices) > 1:
        return heuristic_max_constraints([words[i] for i in indices])
    return words[choice(indices)]

