import sys
import os

CONTROLEUR_PATH = "/controleur"

def configurer_pythonpath():

    racine_application = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, racine_application+CONTROLEUR_PATH)

