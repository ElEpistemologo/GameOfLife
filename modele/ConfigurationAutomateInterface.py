from abc import ABC, abstractmethod
from typing import List

class ConfigurationAutomateInterface(ABC):

    @abstractmethod
    def __init__(self, parametres: List):
        pass

    @abstractmethod
    def parametres_configuration(self) -> List:
        pass