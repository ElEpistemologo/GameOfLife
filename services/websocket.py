#!/usr/bin/python

from flask import Flask, request
from flask_socketio import SocketIO, emit
import ast

from AutomateThread import AutomateThread
from ConfigurationAutomateJohnConway import ConfigurationAutomateJohnConway

serveur_web_socket = Flask("Web Socket Serveur")
socketio = SocketIO(serveur_web_socket, cors_allowed_origins =["http://localhost:3000"])
liste_thread_automate = {}

@socketio.on("connect")
def nouvelle_connexion(auth):
    sid = request.sid
    print(f"connexion nouveau client: {auth}, sid:{sid}")
    emit("reponse_connexion", "connexion au serveur websocket acceptée")

@socketio.on("disconnect")
def fin_connexion():
    sid = request.sid
    if sid in liste_thread_automate:
        liste_thread_automate.pop(sid)
    print(f"connexion avec client {sid} terminée")

@socketio.on("lancer_automate")
def lancer_automate(message):
    sid = request.sid
    print(f"ordre - lancer automate, provenant de {sid}, message:{message}")
    dict_message = ast.literal_eval(str(message))
    configuration_automate = ConfigurationAutomateJohnConway(-1, "temp", [int(dict_message["largeur"]),
                                                                          int(dict_message["hauteur"]),
                                                                          dict_message["automate"]])
    liste_thread_automate[sid] = AutomateThread(sid, configuration_automate, socketio)
    liste_thread_automate[sid].lancer_automate()

@socketio.on("pause_automate")
def pause_automate():
    sid = request.sid
    liste_thread_automate[sid].pause_automate()

@socketio.on("etape_suivante")
def etape_suivante(message):
    sid = request.sid
    dict_message = ast.literal_eval(str(message))
    configuration_automate = ConfigurationAutomateJohnConway(-1, "temp", [int(dict_message["largeur"]),
                                                                          int(dict_message["hauteur"]),
                                                                          dict_message["automate"]])
    liste_thread_automate[sid] = AutomateThread(sid, configuration_automate, socketio)
    liste_thread_automate[sid].etape_suivante()

@socketio.on("augmenter_vitesse")
def augmenter_vitesse():
    sid = request.sid
    liste_thread_automate[sid].augmenter_vitesse()

@socketio.on("diminuer_vitesse")
def diminuer_vitesse():
    sid = request.sid
    liste_thread_automate[sid].diminuer_vitesse()

@socketio.on("stop_automate")
def stop_automate():
    sid = request.sid
    if sid in liste_thread_automate:
        liste_thread_automate[sid].stop_automate()

if __name__ == "__main__":
    socketio.run(serveur_web_socket, "127.0.0.1", "5001", debug=True, use_reloader=True)
