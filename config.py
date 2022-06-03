import sys
import os

CONTROLEUR_PATH = "/controleur"
MODELE_PATH = "/modele"

def configurer_pythonpath():

    racine_application = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, racine_application + CONTROLEUR_PATH)
    sys.path.insert(0, racine_application + MODELE_PATH)
