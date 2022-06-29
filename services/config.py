#!/usr/bin/python

import sys
import os

MODELE_PATH = "modele"
ENTITES_PATH = "entites"
TESTS_PATH = "tests"
DAO_PATH = "dao"
API_PATH = "services"

def recuperer_cle_secrete():
    FICHIER_CLE_SECRETE = "Fichier_cle_secrete"
    fichier = None
    cle = None
    try:
        fichier = open(FICHIER_CLE_SECRETE, "r")
        cle = fichier.readline().strip()
    except IOError as erreur:
        print(f"La clé secrète de l'API n'a pas pu être lue")
        sys.exit(1)
    finally:
        if fichier:
            fichier.close()
    return cle