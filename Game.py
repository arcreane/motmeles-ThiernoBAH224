import random
import string
import os

# Fonction permettant de creer un menu


def menu():
    print("\n************************** Bienvenue ***********************")
    print("1 - Demmarer une partie")
    print("4 - Quitter")

    while (True):
        choix = input("Veuillez choisir votre option : ")
        if int(choix) == 1:
            return sous_menu()
        elif int(choix) == 4:
            return 4
        print("Saisie incorrect\n")

# Creer un sous menu


def sous_menu():
    print("\n")
    while (True):
        print("1 - niveau facile")
        print("2 - niveau moyen")
        print("3 - niveau difficile\n")
        print("4 - Quitter")
        choix = input("Veuillez choisir votre option : ")
        if int(choix) == 1 or int(choix) == 2 or int(choix) == 3 or int(choix) == 4:
            return int(choix)
        print("Saisie invalide\n")

# lire les mots sur un fichier et les renvoyer sous forme d'une liste


def lire_mots(nom_fichier):
    mots = []
    with open(nom_fichier, 'r') as f:
        for ligne in f:
            mot = ligne.strip()
            mots.append(mot)
    return mots


# Creer une grille en fonction du niveau choisi
"""
Cette fonction fait appel a la fonction initGrille qui initialise la grille avec les mots choisie aléatoirement
"""


def creer_grille(niveau):
    liste_mot = [[]]
    ligne, colonne = 0, 0
    if niveau == 1:
        liste_mot = lire_mots("facile.txt")
        # choisir 5 mots au hasar parmi la liste des mots pour le niveau facile
        liste_mot = random.sample(liste_mot, 5)
        ligne, colonne = 10, 5
    elif niveau == 2:
        liste_mot = lire_mots("moyen.txt")
        # choisir 6 mots au hasar parmi la liste des mots pour le niveau moyen
        liste_mot = random.sample(liste_mot, 6)
        ligne, colonne = 15, 7
    else:
        liste_mot = lire_mots("difficile.txt")
        # choisir 8 mots au hasar parmi la liste des mots pour le niveau difficile
        liste_mot = random.sample(liste_mot, 8)
        ligne, colonne = 30, 15
    # creation de la grille initialisé a vide
    grille = [['']*colonne for i in range(ligne)]

    return initGrille(grille, liste_mot, ligne, colonne)


# Affichage de la grille
def affichage(grille, liste_mots, l, c, liste_mots_trouve):
    colonne = [i for i in range(c)]

    print("\t|", end=' ')
    for i in colonne:
        print(" ", i+1, end=' ')
    print("  |")

    for i in range(c):
        print("------", end='')
    print("|")

    for i in range(l):
        print("{}\t| ".format(i+1), end=' ')
        for j in range(c):
            print(" {} ".format(grille[i][j]), end=' ')
        print(" |")
    print("\n")
    print("Liste des mots :", end=' ')
    for i in liste_mots:
        if i in liste_mots_trouve:
            print("\033[93m{}\033[0m".format(i), end=' ')
        else:
            print("{}".format(i), end=' ')
    print("\n")


# Initialiser la grille avec la liste des mots placés de façon aléatoire
def initGrille(grille, liste_mots, ligne, colonne):
    # dico : contient la postion de chaque mot dans la grille, il est utilisé pour faire la verification pour le saisie de l'utilisateur
    dico = {}
    for i in liste_mots:
        while (True):
            # choisir une position aléatoire du mot
            l = random.randint(0, ligne-1)
            c = random.randint(0, colonne-1)
            direction = random.choice(['h', 'v'])

            # verifier que le mot ne se chevauche pas avec un autre
            if peutPlacer(grille, ligne, colonne, l, c, len(i), direction):
                if direction == 'h':
                    grille[l][c:len(i)+c] = i
                    dico[i] = ['h', l+1, c+1]
                if direction == 'v':
                    for j in range(len(i)):
                        grille[l+j][c] = i[j]
                        dico[i] = ['v', l+1, c+1]
                break
    # remplir les cases vides avec des lettres aléatoires
    for i in range(ligne):
        for j in range(colonne):
            if grille[i][j] == '':
                grille[i][j] = random.choice(list(string.ascii_lowercase))
    return dico, grille, ligne, colonne, liste_mots


# Verification du placement du mot est valide
def peutPlacer(grille, ligne, colonne, l, c, taille_mot, direction):
    if direction == 'h' and taille_mot+c < colonne:
        x = grille[l][c:taille_mot+c]
        for i in x:
            if i != '':
                return False
        return True
    if direction == 'v' and taille_mot+l < ligne:
        x = []

        for i in range(l, l+taille_mot):
            x.append(grille[i][c])

        for i in x:
            if i != '':
                return False
        return True
    return False


def mot_a_chercher(dico, mot, ligne, colonne, ind_i, ind_j, dir, list_mots):
    if ind_i > ligne or ind_j > colonne:
        return False
    if mot in list_mots:
        if [dir, ind_i, ind_j] == dico[mot]:
            return True
    return False


def play(grille, ligne, colonne, liste_mots, dico):
    liste_mot_trouve = []

    while len(liste_mots) != len(liste_mot_trouve):
        os.system('clear')
        os.system('cls')
        affichage(grille, liste_mots, ligne, colonne, liste_mot_trouve)
        mot = input("mot a chercher ? : ")
        ind_i = int(input("indice de la ligne ? : "))
        ind_j = int(input("indice de la colonne : "))
        print("Selectionner la direction 'h' -> horizontale; 'v' -> verticale")
        dir = input("directioin : ")
        if mot_a_chercher(dico, mot, ligne, colonne, ind_i, ind_j, dir, liste_mots):
            liste_mot_trouve.append(mot)

    print("Felicitation !!!! \n")
