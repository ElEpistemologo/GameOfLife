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
        self.stop = False

    @property
    def sid(self):
        return self.__sid

    @property
    def etat_initial(self):
        return self.__etat_initial

    @property
    def socketio(self):
        return self.__socketio

    @property
    def pause(self):
        return self.__pause

    @property
    def stop(self):
        return self.__stop

    @property
    def generation_temps(self):
        return self.__generation_temps

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

    @pause.setter
    def pause(self, pause):
        self.__pause = pause

    @stop.setter
    def stop(self, stop):
        self.__stop = stop

    @generation_temps.setter
    def generation_temps(self, generation_temps):
        self.__generation_temps = generation_temps

    def run(self):
        while not self.stop:
            while not self.pause and not self.stop:
                self.automate.generation_suivante()
                self.socketio.emit("maj_automate", self.automate.__str__(), room=self.sid)
                time.sleep(self.generation_temps)
        print(f"Client {self.sid}, automate terminé")

    def lancer_automate(self):
        self.start()
        print(f"Client {self.sid}, ordre: Lancer automate")

    def pause_automate(self):
        self.pause = not self.pause
        print(f"Client {self.sid}, ordre: Pause")

    def stop_automate(self):
        self.stop = True
        self.pause = False
        print(f"Client {self.sid}, ordre: Stop")

    def etape_suivante(self):
        print(f"Client {self.sid}, ordre: Etape suivante")
        self.automate.generation_suivante()
        self.socketio.emit("maj_automate", self.automate.__str__(), room=self.sid)

    def augmenter_vitesse(self):
        self.generation_temps /= 4
        print(f"Client {self.sid}, ordre: Augmenter vitesse")

    def diminuer_vitesse(self):
        self.generation_temps *= 4
        print(f"Client {self.sid}, ordre: Diminuer vitesse")
