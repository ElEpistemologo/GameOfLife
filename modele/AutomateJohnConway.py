from typing import List
import random

from ConfigurationAutomateJohnConway import ConfigurationAutomateJohnConway
from GameOfLifeException import GameOfLifeException
from AutomateInterface import AutomateInterface

class AutomateJohnConway(AutomateInterface):

    def __init__(self, config: ConfigurationAutomateJohnConway):

        if not isinstance(config, ConfigurationAutomateJohnConway):
            raise ValueError("La configuration apportée à l'automate de JC n'est pas une configuration d'automate de JC")
        else:
            automate = []
            iterateur_largeur = 0
            iterateur_hauteur = 0

            while iterateur_largeur < config.largeur:
                colonne = []
                while iterateur_hauteur < config.hauteur:
                    if random.randint(0,1) == 1:
                        colonne.append(True)
                    else:
                        colonne.append(False)
                    iterateur_hauteur += 1
                automate.append(colonne)
                iterateur_largeur += 1
            self.automate = automate

    def generation_suivante(self):
        pass

    def __str__(self):
        return str(self.automate)

    @property
    def automate(self):
        return self.__automate

    @automate.setter
    def automate(self, automate: List[List[bool]]):
        self.__automate = automate

