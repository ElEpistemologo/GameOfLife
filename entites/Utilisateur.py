import json
from typing import List

class Utilisateur(object):


    #Créer un Utilisateur
    # identifiant: entier
    # pseudo: chaine de cractère de longueur [4, 20]
    # configurations_automate: liste des identifiants de configuration d'automate, des entiers positifs
    # cette liste ne doit pas dépasser 20 éléments et ne doit pas comporter de doublons
    def __init__(self, pseudo: str, mot_de_passe: str, identifiants_configurations_automate: List[int] = []):
        self.pseudo = pseudo
        self.identifiants_configurations_automate = identifiants_configurations_automate
        self.mot_de_passe = mot_de_passe

    def __str__(self):
        jsonUtilisateur = {"Pseudo":self.pseudo, "Identifiants de configurations":self.identifiants_configurations_automate}
        return json.dumps(jsonUtilisateur, separators=(',', ':'))

    @property
    def mot_de_passe(self):
        return self.__mot_de_passe

    @property
    def pseudo(self) -> str:
        return self.__pseudo

    @property
    def identifiants_configurations_automate(self) -> List[int]:
        return self.__identifiants_configurations_automate

    @mot_de_passe.setter
    def mot_de_passe(self, mot_de_passe:str):
        if not isinstance(mot_de_passe, str):
            raise ValueError("Le pseudo de l'utilisateur doit être une chaine de caractère")
        elif len(mot_de_passe) <4 or len(mot_de_passe) > 20:
            raise ValueError("Le pseudo de l'utilisateur doit être de longueur [4-20]")
        else:
            self.__mot_de_passe = mot_de_passe

    # pseudo: chaine de cractère de longueur [4, 20]
    @pseudo.setter
    def pseudo(self, pseudo:str):
        if not isinstance(pseudo, str):
            raise ValueError("Le pseudo de l'utilisateur doit être une chaine de caractère")
        elif len(pseudo) <4 or len(pseudo) > 20:
            raise ValueError("Le pseudo de l'utilisateur doit être de longueur [4-20]")
        else:
            self.__pseudo = pseudo

    # identifiants_configurations_automate: liste de ConfigurationAutomate, de longueur [0,20]
    # cette liste ne doit pas contenir de configurations d'identifiants égaux
    @identifiants_configurations_automate.setter
    def identifiants_configurations_automate(self, identifiants_configurations_automate: List[int]):
        if not isinstance(identifiants_configurations_automate, list):
            raise ValueError("La liste de configurations d'automates est invalide")
        elif len(identifiants_configurations_automate) > 20:
            raise ValueError("La liste de configurations est trop longue. Longueur maximum: 20")
        else:
            # vérifie si tous les éléments de la liste sont des entiers
            for config in identifiants_configurations_automate:
                if not isinstance(config, int):
                    raise ValueError("La liste de configurations d'automates est invalide")
            # vérifie s'il n'y a pas de doublons dans les identifiants des configurations
            for i in range(len(identifiants_configurations_automate)-1):
                identifiant_a_verifier = identifiants_configurations_automate[i]
                for j in range(len(identifiants_configurations_automate))[i+1:]:
                    if identifiant_a_verifier == identifiants_configurations_automate[j]:
                        raise ValueError("Un utilisateur ne peut pas avoir deux configurations de même identifiant")
            self.__identifiants_configurations_automate = identifiants_configurations_automate
