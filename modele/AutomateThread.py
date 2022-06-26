from threading import Thread
import time

from AutomateJohnConway import AutomateJohnConway
from ConfigurationAutomateInterface import ConfigurationAutomateInterface



class AutomateThread (Thread):

    def __init__(self, sid, etat_initial: ConfigurationAutomateInterface, socketio):
        Thread.__init__(self)
        self.sid = sid
        self.etat_initial = etat_initial
        self.pause = False
        self.automate = AutomateJohnConway(etat_initial)
        self.generation_temps = 1.0
        self.socketio = socketio

    @property
    def sid(self):
        return self.__sid

    @property
    def etat_initial(self):
        return self.__etat_initial

    @property
    def socketio(self):
        return self.__socketio

    @sid.setter
    def sid(self, sid):
        if not isinstance(sid, str):
            raise ValueError("l'identifiant de la room n'est pas une chaine de caractère")
        else:
            self.__sid = sid

    @etat_initial.setter
    def etat_initial(self, etat_initial):
        if not isinstance(etat_initial, ConfigurationAutomateInterface):
            raise ValueError("L'état initial n'est pas une configuration d'automate")
        else:
            self.__etat_initial = etat_initial

    @socketio.setter
    def socketio(self, socketio):
        self.__socketio = socketio

    def run(self):
        while(not self.pause):
            self.automate.generation_suivante()
            self.socketio.emit("maj_automate", self.automate.__str__(), room=self.sid)
            time.sleep(self.generation_temps)


    def attendre(self):
        pass

    def lancer_automate(self):
        self.start()

    def pause_automate(self):
        print("L'automate a été mis en pause")
        self.pause = not self.pause

    def etape_suivante(self):
        print("L'automate a été avancé d'une génération")

    def augmenter_vitesse(self):
        self.generation_temps /= 4
        print("La vitesse des génération a augmenté")

    def diminuer_vitesse(self):
        self.generation_temps *= 4
        print("La vitesse des génération a diminué")
