import json
import traceback

from flask import Flask, make_response, request, session
from DaoInterface import DaoInterface
from ConfigurationAutomateInterface import ConfigurationAutomateInterface
from flask_cors import CORS
from Utilisateur import Utilisateur
from ConfigurationAutomateJohnConway import ConfigurationAutomateJohnConway

import config

api = Flask(__name__)
api.secret_key = config.recuperer_cle_secrete()
cors = CORS(api, origins=["*"], supports_credentials=True)

class DAOSingleton(object):

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DAOSingleton, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def setDAO(dao: ConfigurationAutomateInterface):
        if not hasattr(DAOSingleton, "dao"):
            DAOSingleton.dao = dao
        else:
            raise Exception("le dao a déjà été initialisé")

    @staticmethod
    def getDAO() -> DaoInterface:
        return DAOSingleton.dao

def lancer_api(dao: DaoInterface):
    daoSingleton = DAOSingleton()
    daoSingleton.setDAO(dao)
    api.config.update(ENV="development", DEBUG=True)
    api.run()

@api.route("/session")
def retourner_session():

    # si le client n'a pas de session, on initialise une session anonyme et on retourne les informations de base
    if ( "pseudo" not in session ):
        print(f"Nouvelle session anonyme émanant de {request}")
        session["pseudo"] = "anonyme"
        reponse = make_response(json.dumps({"pseudo": "Anonyme"}))
        return reponse, 200
    # si le client a une session anonyme, on retourne les informations de base
    elif ( session["pseudo"] == "anonyme"):
        pseudo = session["pseudo"]
        print(f"Le client anonyme se reconnecte {request}; session={pseudo}")
        reponse = make_response(json.dumps({"pseudo": "Anonyme"}))
        return reponse, 200
    # si le client a une session utilisateur, lui renvoyer ses informations
    else:
        pseudo = session["pseudo"]
        print(f"Le client avec la requête {request} et la session = {pseudo} tente de récupérer ses informations")
        recuperationUtilisateur = DAOSingleton.getDAO().obtenir_utilisateur_par_pseudo(session["pseudo"])
        if recuperationUtilisateur[1]:
            utilisateur = recuperationUtilisateur[0]
            reponse_json = creer_informations_utilisateur(utilisateur)
            print("L'utilisateur suivant s'est connecté à une session existante: " + str(json.dumps(reponse_json)))
            response = make_response(json.dumps(reponse_json))
            response.headers.set("Content-type", "application/json; charser=utf8")
            return response
        # si le client a une session correspondant à un utilisateur qui n'existe pas, change la session en anonyme
        else:
            pseudo = session["pseudo"]
            print(f"Le client avec la requête {request} et la session = {pseudo} a échoué à récupérer ses informations")
            session["pseudo"] = "anonyme"
            reponse = make_response()
            reponse.headers["Content-Length"] = 0
            return reponse, 200

# Accéder à une configuration par son identifiant
@api.route("/configuration/obtenir/<identifiant>")
def retourner_configuration(identifiant):
    # TODO: vérifier si le client a une session utilisateur et si la configuration demandée lui appartient
    resultat_requete_configuration = DAOSingleton.getDAO().obtenir_configuration_automate_par_identifiants([int(identifiant)])
    if( resultat_requete_configuration[1] ):
        configuration = resultat_requete_configuration[0][0]
        print("Récupération de la configuration: "+str(configuration.parametres_configuration()))
        response = make_response(json.dumps(configuration.parametres_configuration()))
        response.headers.set("Content-type", "application/json; charser=utf8")
        return response
    else:
        response = make_response(json.dumps({"message":"La configuration d'automate demandée n'existe pas"}))
        response.headers.set("Content-type", "application/json; charser=utf8")
        return response, 400

# Modifier une configuration existante
@api.route("/configuration/modifier", methods=['POST'])
def enregistrer_configuration():
    content_type = request.headers.get('Content-Type')
    print(f"Tentative de modification de {request.json}")
    if (content_type == 'application/json'):
        # vérification de l'authentification du client
        if "pseudo" in session:
            resultat_recherche_utilisateur = DAOSingleton.getDAO().obtenir_utilisateur_par_pseudo(session["pseudo"])
            if ( resultat_recherche_utilisateur ):
                utilisateur = resultat_recherche_utilisateur[0]
                requete_json = request.json
                #  vérification si la configuration qui est modifié appartient à l'utilisateur
                appartient = False
                for config_id in utilisateur.identifiants_configurations_automate:
                    if config_id  == int(requete_json["identifiant"]):
                        appartient = True
                if ( appartient ):
                    try:
                        # si la configuration est déjà existante, on la modifie
                        resultat_recherche_config = DAOSingleton.getDAO().obtenir_configuration_automate_par_identifiants([int(requete_json["identifiant"])])
                        if ( resultat_recherche_config[1] ):
                            config_modification = resultat_recherche_config[0][0]
                            resultat_modification = DAOSingleton.getDAO().modifier_configuration_automate(ConfigurationAutomateJohnConway(
                                config_modification.identifiant,
                                requete_json["nom"],
                                [int(requete_json["largeur"]),
                                 int(requete_json["hauteur"])]
                            ))
                            # si la modification a réussie
                            if ( resultat_modification ):
                                print(f"La tentative de modification de la configuration {config_modification.identifiant} a réussie, provenant de: {request}")
                                reponse = make_response()
                                reponse.headers["Content-Length"] = 0
                                return reponse, 200
                            else:
                                print(
                                    f"La tentative de modification de la configuration {config_modification.identifiant} a échoué, provenant de: {request}")
                                response = make_response(
                                    json.dumps({"message": "Echec de la modification de la configuration"}))
                                response.headers.set("Content-type", "application/json; charser=utf8")
                                return response, 400
                    except Exception:
                        print(f"La tentative de modification d'une configuration a échoué, provenant de: {request}")
                        traceback.print_exc()
                else:
                    print(f"La tentative de modification d'une configuration a échoué, provenant de: "
                          f"{request}, la configuration ne lui appartient pas")
            else:
                print(f"La tentative de modification d'une configuration a échoué, provenant de: "
                      f"{request}. L'utilisateur est introuvable")
        else:
            print(f"La tentative de modification d'une configuration a échoué, provenant de: "
                  f"{request}. Il n'y a pas d'information de session dans la requete")
    else:
        print("La tentative de connexion: " + str(request) + " a échoué: Le body de la requete n'est pas un json")
    response = make_response(json.dumps({"message": "La modification de la configuration a échouée"}))
    response.headers.set("Content-type", "application/json; charser=utf8")
    return response, 400

# Supprimer une configuration
@api.route("/configuration/supprimer")
def supprimer_configuration(identifiant:int):
    print(request)
    pass

# Tentative de connexion utilisateur
@api.route("/utilisateur/connecter", methods=['POST'])
def connecter_utilisateur():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        requete_json = request.json
        print("Tentative de connexion: " + str(requete_json))
        recuperationUtilisateur = DAOSingleton.getDAO().obtenir_utilisateur_par_pseudo(requete_json["pseudo"])
        if recuperationUtilisateur[1]:
            utilisateur = recuperationUtilisateur[0]
            if utilisateur.mot_de_passe == requete_json["mot_de_passe"]:
                reponse_json = creer_informations_utilisateur(utilisateur)
                print("L'utilisateur suivant s'est connecté: " + str(json.dumps(reponse_json)))
                session["pseudo"] = utilisateur.pseudo
                response = make_response(json.dumps(reponse_json))
                response.headers.set("Content-type", "application/json; charser=utf8")
                return response, 200
            else:
                print("La tentative de connexion: " + str(requete_json)+ " a échoué: Mauvais mot de passe")
                response = make_response(json.dumps({"message": "Les identifiants sont erronés"}))
                response.headers.set("Content-type", "application/json; charser=utf8")
                return response, 400
        else:
            print("La tentative de connexion: " + str(requete_json) + " a échoué: L'utilisateur est introuvable")
            response = make_response(json.dumps({"message": "Les identifiants sont erronés"}))
            response.headers.set("Content-type", "application/json; charser=utf8")
            return response, 400
    else:
        print("Requête de connexion utilisateur invalide: " + str(request)+ " n'a pas de contenu json")
        response = make_response(json.dumps({"message": "Content-Type non supporté"}))
        response.headers.set("Content-type", "application/json; charser=utf8")
        return response, 400


# Déconnexion utilisateur
@api.route("/utilisateur/deconnecter")
def deconnecter_utilisateur():
    pseudo = session["pseudo"]
    print(f"Déconnexion de l'utilisateur {pseudo}")
    session["pseudo"] = "anonyme"
    reponse = make_response()
    reponse.headers["Content-Length"] = 0
    return reponse, 200
    pass

# Nouvel utilisateur
@api.route("/utilisateur/creer")
def creer_utilisateur(pseudo: str, mot_de_passe: str):
    print(request)
    pass

def creer_informations_utilisateur(utilisateur: Utilisateur):
    reponse_json = {}
    reponse_json["pseudo"] = utilisateur.pseudo
    liste_configurations = {}
    iterateur_configuration = 0
    while iterateur_configuration < len(utilisateur.identifiants_configurations_automate):
        identifiant_configuration = utilisateur.identifiants_configurations_automate[iterateur_configuration]
        resultat_recherche_config = DAOSingleton.getDAO().obtenir_configuration_automate_par_identifiants(
            [identifiant_configuration])
        if (resultat_recherche_config[1]):
            nom_configuration = resultat_recherche_config[0][0].nom
            liste_configurations.update({identifiant_configuration: nom_configuration})
        else:
            print(f"Une configuration de l'utilisateur {utilisateur.pseudo} n'a pas été trouvée")
        iterateur_configuration += 1
    reponse_json["configurations"] = liste_configurations
    return reponse_json