from abc import ABC, abstractmethod
from typing import List
from Utilisateur import Utilisateur
from ConfigurationAutomateJohnConway import ConfigurationAutomate

class DaoInterface(ABC):

    @abstractmethod
    def obtenir_utilisateur_par_pseudo(self, pseudo: str) -> [Utilisateur, bool]:
        pass

    @abstractmethod
    def ajouter_nouvel_utilisateur(self, pseudo: str, mot_de_passe: str) -> bool:
        pass

    @abstractmethod
    def supprimer_nouvel_utilisateur_par_pseudo(self, identifiant: str) -> bool:
        pass

    @abstractmethod
    def obtenir_configuration_automate_par_identifiants(self, identifiants: List[int]) -> List[ConfigurationAutomate]:
        pass

    @abstractmethod
    def ajouter_configuration_automate(self, parametres: List) -> bool:
        pass

    @abstractmethod
    def supprimer_configuration_automate_par_identifiant(self, identifiant: int) -> bool:
        pass