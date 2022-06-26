import copy
import json
from typing import List
import random

from ConfigurationAutomateJohnConway import ConfigurationAutomateJohnConway
from GameOfLifeException import GameOfLifeException
from AutomateInterface import AutomateInterface


class AutomateJohnConway(AutomateInterface):

    def __init__(self, config: ConfigurationAutomateJohnConway):

        if not isinstance(config, ConfigurationAutomateJohnConway):
            raise ValueError(
                "La configuration apportée à l'automate de JC n'est pas une configuration d'automate de JC")
        else:
            self.automate = config.etat_initial

    def generation_suivante(self):
        nouvelle_generation = copy.deepcopy(self.automate.copy())
        for i in range(len(self.automate)):
            for j in range(len(self.automate[0])):
                if  self.automate[i][j] and \
                        (self.compter_cellule_vivante(i, j) == 2 or self.compter_cellule_vivante(i, j) == 3):
                    nouvelle_generation[i][j] = True
                elif not self.automate[i][j] and self.compter_cellule_vivante(i, j) == 3:
                    nouvelle_generation[i][j] = True
                else:
                    nouvelle_generation[i][j] = False

        self.automate = nouvelle_generation.copy()

    def compter_cellule_vivante(self, i, j):
        largeur = len(self.automate)
        hauteur = len(self.automate[0])
        somme_cellule_vivante = 0

        if i - 1 >= 0 and j - 1 >= 0:
            if self.automate[i - 1][j - 1]:
                somme_cellule_vivante += 1
        if i - 1 >= 0:
            if self.automate[i - 1][j]:
                somme_cellule_vivante += 1
        if i - 1 >= 0 and j + 1 < hauteur:
            if self.automate[i - 1][j + 1]:
                somme_cellule_vivante += 1
        if j - 1 >= 0:
            if self.automate[i][j - 1]:
                somme_cellule_vivante += 1
        if i + 1 < largeur and j + 1 < hauteur:
            if self.automate[i + 1][j + 1]:
                somme_cellule_vivante += 1
        if i + 1 < largeur and j - 1 >= 0:
            if self.automate[i + 1][j - 1]:
                somme_cellule_vivante += 1
        if j + 1 < hauteur:
            if self.automate[i][j + 1]:
                somme_cellule_vivante += 1
        if i + 1 < hauteur:
            if self.automate[i + 1][j]:
                somme_cellule_vivante += 1

        return somme_cellule_vivante

    def __str__(self):
        return json.dumps({"automate": self.automate})

    @property
    def automate(self):
        return self.__automate

    @automate.setter
    def automate(self, automate: List[List[bool]]):
        self.__automate = automate
