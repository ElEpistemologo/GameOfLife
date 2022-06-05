import json
from typing import List
from ConfigurationAutomate import ConfigurationAutomate
from GameOfLifeException import GameOfLifeException

class Utilisateur(object):

    #Créer un Utilisateur
    # identifiant: entier
    # pseudo: chaine de cractère de longueur [4, 20]
    # configurations_automate: liste des identifiants de configuration d'automate, des entiers positifs
    # cette liste ne doit pas dépasser 20 éléments et ne doit pas comporter de doublons
    def __init__(self, pseudo: str, configurations_automate: List[int] = []):
        self.pseudo = pseudo
        self.configurations_automate = configurations_automate

    def __str__(self):
        jsonUtilisateur = {"Pseudo":self.pseudo, "Configurations":self.configurations_automate}
        return json.dumps(jsonUtilisateur, separators=(',', ':'))

    @property
    def pseudo(self) -> str:
        return self.__pseudo

    @property
    def configurations_automate(self) -> List[int]:
        return self.__configurations_automate

    # pseudo: chaine de cractère de longueur [4, 20]
    @pseudo.setter
    def pseudo(self, pseudo:str):
        if not isinstance(pseudo, str):
            raise ValueError("Le pseudo de l'utilisateur doit être une chaine de caractère")
        elif len(pseudo) <4 or len(pseudo) > 20:
            raise ValueError("Le pseudo de l'utilisateur doit être de longueur [4-20]")
        else:
            self.__pseudo = pseudo

    # configurations_automate: liste de ConfigurationAutomate, de longueur [0,20]
    # cette liste ne doit pas contenir de configurations d'identifiants égaux
    @configurations_automate.setter
    def configurations_automate(self, configurations_automate: List[ConfigurationAutomate]):
        if not isinstance(configurations_automate, list):
            raise ValueError("La liste de configurations d'automates est invalide")
        elif len(configurations_automate) > 20:
            raise ValueError("La liste de configurations est trop longue. Longueur maximum: 20")
        else:
            # vérifie si tous les éléments de la liste sont des ConfigurationAutomate
            for config in configurations_automate:
                if not isinstance(config, int):
                    raise ValueError("La liste de configurations d'automates est invalide")
            # vérifie s'il n'y a pas de doublons dans les identifiants des configurations
            for i in range(len(configurations_automate)-1):
                identifiant_a_verifier = configurations_automate[i]
                for j in range(len(configurations_automate))[i+1:]:
                    if identifiant_a_verifier == configurations_automate[j]:
                        raise ValueError("Un utilisateur ne peut pas avoir deux configurations de même identifiant")
            self.__configurations_automate = configurations_automate