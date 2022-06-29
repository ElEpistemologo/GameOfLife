#!/usr/bin/python

import sys
import os

MODELE_PATH = "/src/modele"
ENTITES_PATH = "/src/entites"
DAO_PATH = "/src/dao"
TESTS_PATH = "/tests"

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

def configurer_python_path():
    racine_application = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, racine_application + MODELE_PATH)
    sys.path.insert(0, racine_application + ENTITES_PATH)
    sys.path.insert(0, racine_application + DAO_PATH)
    sys.path.insert(0, racine_application + TESTS_PATH)
