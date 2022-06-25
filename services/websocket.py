from flask import Flask, session
from flask_socketio import SocketIO, emit

serveur_web_socket = Flask("Web Socket Serveur")
socketio = SocketIO(serveur_web_socket, cors_allowed_origins =["http://localhost:3000"])

@socketio.on("etape_suivante")
def etape_suivante(message):
    print(f"etape_suivante, message: {message}")

@socketio.on("connect")
def nouvelle_connexion(auth):
    print(f"connexion nouveau client: {auth}")
    emit("reponse_serveur", {"message": "ordre étape suivante acceptée"})

if __name__ == "__main__":
    socketio.run(serveur_web_socket, "127.0.0.1", "5001", debug=True, use_reloader=True)
