# Script de contrôle de l'application

# Demande à l'utilisateur la taille de l'automate
# Retourne la valeur saisie par l'utilisateur
def demander_taille_automate():
    hauteurValide = False
    largeurValide = False

    while(not hauteurValide):
        hauteur = input("Saisir la hauteur de l'automate à créer:")
        try :
            hauteur_entier = int(hauteur)
        except:
            print("veuillez saisir un entier")
            return demander_taille_automate()
        if (int(hauteur) > 0 and int(hauteur) < 100):
            hauteurValide = True
        else:
            print("veuillez saisir un entier entre 1 et 99")
            return demander_taille_automate()

    while (not largeurValide):
        largeur = input("Saisir la largeur de l'automate à créer:")
        try:
            largeur_entier = int(largeur)
        except:
            print("veuillez saisir un entier")
            return demander_taille_automate()
        if (int(largeur) > 0 and int(largeur) < 100):
            largeurValide = True
        else:
            print("veuillez saisir un entier entre 1 et 99")
            return demander_taille_automate()
    print(f"Vous avez saisi hauteur={hauteur} et largeur={largeur}")
    return [int(largeur), int(hauteur)]

def afficher_automate(automate):
    largeur = len(automate)
    hauteur = len(automate[0])

    iterateur_hauteur = 0
    largeur_chaine = ""
    while iterateur_hauteur < hauteur:
        iterateur_largeur = 0
        while iterateur_largeur < largeur:
            largeur_chaine += automate[iterateur_largeur][iterateur_hauteur]
            iterateur_largeur += 1
        print(largeur_chaine)
        largeur_chaine = ""
        iterateur_hauteur += 1
