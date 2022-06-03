import sys
import os

CONTROLEUR_PATH = "controleur"
MODELE_PATH = "modele"

def configurer_pythonpath():
    racine_script = os.path.dirname(os.path.abspath(__file__))
    racine_application = racine_script.split("tests")[0]
    sys.path.insert(0, racine_application)
    sys.path.insert(0, racine_application + CONTROLEUR_PATH)
    sys.path.insert(0, racine_application + MODELE_PATH)