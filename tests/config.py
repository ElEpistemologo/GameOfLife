import sys
import os

CONTROLEUR_PATH = "controleur"
MODELE_PATH = "modele"
ENTITES_PATH = "entites"
DAO_PATH = "dao"
API_PATH = "api"

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

def configurer_pythonpath():
    racine_script = os.path.dirname(os.path.abspath(__file__))
    racine_application = racine_script.split("tests")[0]
    sys.path.insert(0, racine_application)
    sys.path.insert(0, racine_application + CONTROLEUR_PATH)
    sys.path.insert(0, racine_application + MODELE_PATH)
    sys.path.insert(0, racine_application + ENTITES_PATH)
    sys.path.insert(0, racine_application + DAO_PATH)
    sys.path.insert(0, racine_application + API_PATH)