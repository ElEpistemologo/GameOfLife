#!/usr/bin/python

from abc import ABC, abstractmethod
from typing import List, Dict

class ConfigurationAutomateInterface(ABC):

    @abstractmethod
    def __init__(self, identifiant: int, nom: str, parametres: List):
        pass

    @abstractmethod
    def json(self) -> str:
        pass

    @abstractmethod
    def parametres_configuration(self) -> Dict:
        pass

    @abstractmethod
    def identifiant(self) -> int:
        pass

    @abstractmethod
    def nom(self) -> str:
        pass

    @abstractmethod
    def type(self) -> Dict:
        pass
