from abc import ABC, abstractmethod
from typing import List
from ConfigurationAutomateInterface import ConfigurationAutomateInterface

class AutomateInterface(ABC):

    @abstractmethod
    def __init__(self, config: ConfigurationAutomateInterface):
        pass

    @abstractmethod
    def generation_suivante(self):
        pass

    @abstractmethod
    def __str__(self):
        pass