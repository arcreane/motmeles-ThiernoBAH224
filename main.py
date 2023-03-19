import Game as game
import os


def main():
    while (True):
        choix = game.menu()
        if choix != 4:
            dico, grille, ligne, colonne, liste_mots = game.creer_grille(choix)
            game.play(grille, ligne, colonne, liste_mots, dico)
        if choix == 4:
            break


if __name__ == '__main__':
    main()
