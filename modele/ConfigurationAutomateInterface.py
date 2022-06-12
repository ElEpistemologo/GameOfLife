from abc import ABC, abstractmethod
from typing import List, Dict

class ConfigurationAutomateInterface(ABC):

    @abstractmethod
    def __init__(self, parametres: List):
        pass

    @abstractmethod
    def parametres_configuration(self) -> List:
        pass
    @abstractmethod
    def json(self) -> str:
        pass

    @abstractmethod
    def parametres_configuration(self) -> Dict:
        pass