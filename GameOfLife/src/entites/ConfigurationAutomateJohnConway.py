#!/usr/bin/python

import json
from typing import List, Dict
from ConfigurationAutomateInterface import ConfigurationAutomateInterface

class ConfigurationAutomateJohnConway(ConfigurationAutomateInterface):

    def __init__(self, identifiant: int, nom: str, parametres:List):
        self.identifiant = identifiant
        self.nom = nom
        if len(parametres) == 3:
            self.largeur = parametres[0]
            self.hauteur = parametres[1]
            self.etat_initial = parametres[2]
        else:
            raise ValueError("Les paramètres de la configuration d'automate de John Conway ne sont pas valides")
        self.__type = "AJC"

    def json(self) -> str :
        return json.dumps({"Identifiant":self.identifiant,
                           "Nom":self.nom,
                           "Largeur":self.largeur,
                           "Hauteur": self.hauteur,
                           "Etat_initial":self.etat_initial},
                          separators=(',', ':'))

    def json_parametres(self) -> str :
        return json.dumps({"largeur":self.largeur,
                           "hauteur": self.hauteur,
                           "etat_initial":str(self.etat_initial)},
                          separators=(',', ':'))

    # renvoie un dictionnaire contenant les paramètres de la configuration
    def parametres_configuration(self) -> Dict:
        return {"Identifiant": self.identifiant,
                "Nom": self.nom,
                "Largeur":self.largeur,
                "Hauteur":self.hauteur,
                "Etat_initial":self.etat_initial}

    @property
    def identifiant(self):
        return self.__identifiant

    @property
    def nom(self):
        return self.__nom

    @property
    def hauteur(self):
        return self.__hauteur

    @property
    def largeur(self):
        return self.__largeur

    @property
    def etat_initial(self):
        return self.__etat_initial

    @identifiant.setter
    def identifiant(self, identifiant: int):
        if not isinstance(identifiant, int):
            raise ValueError("L'identifiant de la configuration de l'automate n'est pas un entier")
        else:
            self.__identifiant = identifiant

    @nom.setter
    def nom(self, nom: str):
        if not isinstance(nom, str):
            raise ValueError("Le nom de la configuration de l'automate n'est pas une chaine de caractère")
        elif len(nom) > 31:
            raise ValueError("Le nom de de la configuration de l'automate n'est pas de la taille autorisée (1-30)")
        elif nom == "":
            raise ValueError("Le nom de l'automate est vide")
        else:
            self.__nom = nom

    @hauteur.setter
    def hauteur(self, hauteur:int):
        if not isinstance(hauteur, int):
            raise ValueError("La hauteur de la configuration de l'automate n'est pas un entier")
        elif hauteur <1 or hauteur > 99:
            raise ValueError("La hauteur de la configuration l'automate n'est pas dans les bornes valides. (Bornes valides: [1;99]")
        elif hauteur == 0:
            raise ValueError("La hauteur de la configuration est nulle")
        else:
            self.__hauteur = hauteur

    @largeur.setter
    def largeur(self, largeur: int):
        if not isinstance(largeur, int):
            raise ValueError("La largeur de la configuration de l'automate n'est pas un entier")
        elif largeur < 1 or largeur > 99:
            raise ValueError("La largeur de la configuration l'automate n'est pas dans les bornes valides. (Bornes valides: [1;99]")
        elif largeur == 0:
            raise ValueError("La largeur de l'automate est vide")
        else:
            self.__largeur = largeur

    @etat_initial.setter
    def etat_initial(self, etat_initial: List[List[bool]]):
        if len(etat_initial) == 0:
            raise ValueError("L'état initial de la configuration est vide")
        colonne_vide = False
        for colonne in etat_initial:
            if len(colonne) == 0:
                colonne_vide = True
        if colonne_vide:
            raise ValueError("Une colonne de l'état initial est vide")
        if len(etat_initial) != self.largeur:
            raise ValueError("L'état initial de la configuration ne correspond pas à sa largeur")
        hauteur_valide = True
        for colonne in etat_initial:
            if len(colonne) != self.hauteur:
                hauteur_valide = False
        if not hauteur_valide:
            raise ValueError("Au moins une colonne de l'état initial de la configuration "
                             "ne correspond pas à la hauteur donnée")
        for colonne in etat_initial:
            for cellule in colonne:
                if not isinstance(cellule, bool):
                    raise ValueError("Un élément de l'état initial de la configuration n'est pas un booléen")
        self.__etat_initial = etat_initial

    def type(self):
        return self.__type