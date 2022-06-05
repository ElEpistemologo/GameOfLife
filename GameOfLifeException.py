

# Exception relevant les erreurs lors de l'initialisation ou du calul de l'automate cellulaire
class GameOfLifeException(Exception):
    ################## CODES ERREURS #######################
    # 1: parametres invalides
    def __init__(self: object, code_exception: int, message_exception: str):
        BaseException.__init__(self, message_exception)
        self.code_exception = code_exception

    def __str__(self):
        return f"{self.code_exception}, {super().__str__()}"

    # ------------------------------------------------ GETTERS ------------------------------------------------
    @property
    def code_exception(self) -> int:
        return self.__code_exception

    # ------------------------------------------------ SETTERS ------------------------------------------------
    # Initialise l'attribut code_exception
    # code_exception: un entier strictement positif
    @code_exception.setter
    def code_exception(self, code_exception: int):
        if isinstance(code_exception, int) and code_exception > 0:
            self.__code_exception = code_exception
        else:
            raise ValueError(f"Le code d\'erreur {code_exception} n\'est pas correct")