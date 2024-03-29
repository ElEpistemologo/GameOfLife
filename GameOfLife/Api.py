#!/usr/bin/python

from flask import Flask, make_response, request, session
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import json
import traceback

import config
config.configurer_python_path()

from DaoMySQL import DaoMySQL
from DaoTest import DaoTest
from DaoInterface import DaoInterface
from ConfigurationAutomateInterface import ConfigurationAutomateInterface
from Utilisateur import Utilisateur
from ConfigurationAutomateJohnConway import ConfigurationAutomateJohnConway

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

api = Flask(__name__)
daoSingleton = DAOSingleton()

def lancer_api():
    daoSingleton.setDAO(DaoMySQL())
    api.secret_key = config.recuperer_cle_secrete()
    # CORS(api, origins=["http://51.68.229.81"], supports_credentials=True)
    CORS(api, origins=["http://localhost:3000"], supports_credentials=True)
    api.config.update(ENV="development", DEBUG=True)
    api.wsgi_app = ProxyFix(
        api.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    return api

configurations_publiques = [4]

def lancer_api_test():

    daoSingleton.setDAO(DaoTest())
    api.secret_key = config.recuperer_cle_secrete()
    #CORS(api, origins=["http://51.68.229.81"], supports_credentials=True)
    CORS(api, origins=["http://localhost:3000"], supports_credentials=True)
    api.config.update(ENV="development", DEBUG=True)
    api.wsgi_app = ProxyFix(
        api.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )
    return api

@api.route("/session")
def retourner_session():
    # si le client n'a pas de session, on lui renvoit la session Anonyme et on initialise le cookie session
    if ( "pseudo" not in session ):
        print(f"Nouvelle session anonyme émanant de {request}")
        recuperationUtilisateurAnonyme = DAOSingleton.getDAO().obtenir_utilisateur_par_pseudo("Anonyme")
        if recuperationUtilisateurAnonyme[1]:
            session["pseudo"] = "Anonyme"
            utilisateurAnonyme = recuperationUtilisateurAnonyme[0]
            reponse_json = creer_informations_utilisateur(utilisateurAnonyme)
            print("L'utilisateur suivant s'est connecté à une nouvelle session anonyme: " + str(json.dumps(reponse_json)))
            response = make_response(json.dumps(reponse_json))
            response.headers.set("Content-type", "application/json; charser=utf8")
            return response, 200
        else:
            print(f"L'initialisation d'une nouvelle session anonyme a échouée {request}")
            reponse = make_response()
            return reponse, 400
    # si le client a une session anonyme, on retourne les informations de base
    elif ( session["pseudo"] == "Anonyme"):
        recuperationUtilisateurAnonyme = DAOSingleton.getDAO().obtenir_utilisateur_par_pseudo("Anonyme")
        if recuperationUtilisateurAnonyme[1]:
            print(f"Le client anonyme se reconnecte {request};")
            reponse_json = creer_informations_utilisateur(recuperationUtilisateurAnonyme[0])
            response = make_response(json.dumps(reponse_json))
            response.headers.set("Content-type", "application/json; charser=utf8")
            return response, 200
        else:
            print(f"Le compte client anonyme n'a pas été trouvé {request}")
            reponse = make_response()
            return reponse, 400
    # si le client a une session utilisateur, lui renvoyer ses informations
    else:
        pseudo = session["pseudo"]
        print(f"Le client avec la requête {request} et la session = {pseudo} tente de récupérer ses informations")
        recuperationUtilisateur = DAOSingleton.getDAO().obtenir_utilisateur_par_pseudo(session["pseudo"])
        if recuperationUtilisateur[1]:
            utilisateur = recuperationUtilisateur[0]
            reponse_json = creer_informations_utilisateur(utilisateur)
            print("L'utilisateur suivant a récupéré ses informations: " + str(json.dumps(reponse_json)))
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
    if "pseudo" in session:
        pseudo = session["pseudo"]
        # si l'utilisateur a une session anonyme
        if pseudo == "Anonyme":
            # TODO: on pourra ajouter plus tard ici une liste de configuration publique
            if int(identifiant) in configurations_publiques:
                resultat_requete_configuration = DAOSingleton.getDAO().obtenir_configuration_automate_par_identifiants(
                    [int(identifiant)])
                if (resultat_requete_configuration[1]):
                    configuration = resultat_requete_configuration[0][0]
                    print("Récupération de la configuration: " + str(configuration.parametres_configuration())+f", provenant de {request} ")
                    response = make_response(json.dumps(configuration.parametres_configuration()))
                    response.headers.set("Content-type", "application/json; charser=utf8")
                    return response, 200
                else:
                    print(f"la configuration {identifiant} recherché par {pseudo} n'a pas été trouvé, provenant de {request}")
                    response = make_response(
                        json.dumps({"message": "La configuration d'automate n'a pas été trouvé"}))
                    response.headers.set("Content-type", "application/json; charser=utf8")
                    return response, 400
            else:
                print(f"Un utilisateur anonyme a tenté d'obtenir la configuration privé d'identifiant: {identifiant}, provenant de {request}")
                response = make_response(
                    json.dumps({"message": "Impossible d'obtenir la configuration"}))
                response.headers.set("Content-type", "application/json; charser=utf8")
                return response, 400
        else:
            # si l'utilisateur n'est pas anonyme
            resultat_recherche_utilisateur = DAOSingleton.getDAO().obtenir_utilisateur_par_pseudo(session["pseudo"])
            if ( resultat_recherche_utilisateur[1]):
                utilisateur = resultat_recherche_utilisateur[0]
                appartient = False
                for config_id in utilisateur.identifiants_configurations_automate:
                    if config_id == int(identifiant):
                        appartient = True
                # si la configuration lui appartient
                if appartient:
                    resultat_requete_configuration = DAOSingleton.getDAO().obtenir_configuration_automate_par_identifiants(
                        [int(identifiant)])
                    configuration = resultat_requete_configuration[0][0]
                    print("Récupération de la configuration: " +
                          str(configuration.parametres_configuration()) + f" par l'utilisateur {pseudo}")
                    response = make_response(json.dumps(configuration.parametres_configuration()))
                    response.headers.set("Content-type", "application/json; charser=utf8")
                    return response, 200
                # si elle ne lui appartient pas
                else:
                    print(f"L'utlisateur avec {pseudo} a tenté d'obtenir une configuration privé qui ne lui appartient pas"
                          f", provenant de {request}")
                    response = make_response(
                        json.dumps({"message": "Impossible d'obtenir la configuration"}))
                    response.headers.set("Content-type", "application/json; charser=utf8")
                    return response, 400
            else:
                print(f"Un utilisateur sans session a tenté d'obtenir une configuration privé"
                      f", provenant de {request}")
                response = make_response()
                response.headers["Content-Length"]
                return response, 400
    else:
        print( f"un client non authentifié a tenté d'accéder à une configuration, provenant de {request}" )
        response = make_response()
        response.headers.set("Content-type", "application/json; charser=utf8")
        return response, 400

# Créer une nouvelle configuration
@api.route("/configuration/creer", methods=['POST'])
def creer_configuration():
    print(f"Tentative de création de configuration provenant de {request}")
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        if "pseudo" in session:
            pseudo = session["pseudo"]
            resultat_requete_utilisateur = DAOSingleton.getDAO().obtenir_utilisateur_par_pseudo(pseudo)
            # vérifie si le client a un compte utilisateur
            if resultat_requete_utilisateur[1] or pseudo != "Anonyme":
                config_json = request.json
                try:
                    resultat_ajout_nouvel_config = DAOSingleton.getDAO().\
                        ajouter_configuration_automate(config_json["nom"],
                                                       [int(config_json["largeur"]),
                                                        int(config_json["hauteur"]),
                                                        config_json["etat_initial"]], session["pseudo"])
                    if resultat_ajout_nouvel_config[1]:
                        # identifiant_nouvelle_config = resultat_ajout_nouvel_config[0]
                        # utilisateur = resultat_requete_utilisateur[0]
                        # utilisateur.ajouter_nouvelle_configuration(identifiant_nouvelle_config)
                        print(f"La tentative de création de configuration provenant de {request} et de l'utilisateur"
                              f" {pseudo} a réussie")
                        response = make_response({"identifiant":resultat_ajout_nouvel_config[0]})
                        response.headers.set("Content-type", "application/json; charser=utf8")
                        return response, 200
                    else:
                        print(f"La tentative de création de configuration provenant de {request} a échoué")
                except ValueError:
                    print(f"La tentative de création de configuration provenant de {request} et de l'utilisateur:"
                          f" {pseudo} a échoué, les paramètres de la configurations sont invaludes: {config_json}")
                    response = make_response(json.dumps({"message": "Les paramètres de la configuration sont invalides"}))
                    response.headers.set("Content-type", "application/json; charser=utf8")
                    return response, 400
            else:
                print(f"La tentative de création de configuration provenant de {request} a échoué, l'utilisateur est"
                      f"introuvable ou il est anonyme ")
        else:
            print(f"La tentative de création de configuration provenant de {request} a échoué, le client n'a pas"
                  f"de session initialisée")
    else:
        print(f"La tentative de création de configuration provenant de {request} a échoué, la requete n'est pas au"
              f"bon format")
    response = make_response(json.dumps({"message": "L'enregistrement de la configuration a échouée"}))
    response.headers.set("Content-type", "application/json; charser=utf8")
    return response, 400


# Modifier une configuration existante
@api.route("/configuration/modifier", methods=['POST'])
def modifier_configuration():
    content_type = request.headers.get('Content-Type')
    print(f"Tentative de modification de {request.json}")
    if (content_type == 'application/json'):
        # vérification de l'authentification du client
        if "pseudo" in session:
            resultat_recherche_utilisateur = DAOSingleton.getDAO().obtenir_utilisateur_par_pseudo(session["pseudo"])
            if resultat_recherche_utilisateur:
                utilisateur = resultat_recherche_utilisateur[0]
                requete_json = request.json
                #  vérification si la configuration qui est modifié appartient à l'utilisateur
                appartient = False
                for config_id in utilisateur.identifiants_configurations_automate:
                    if config_id  == int(requete_json["identifiant"]):
                        appartient = True
                if appartient and int(requete_json["identifiant"]) not in configurations_publiques:
                    try:
                        # si la configuration existe bien, on la modifie
                        resultat_recherche_config = DAOSingleton.getDAO().obtenir_configuration_automate_par_identifiants([int(requete_json["identifiant"])])
                        if ( resultat_recherche_config[1] ):
                            config_modification = resultat_recherche_config[0][0]
                            resultat_modification = DAOSingleton.getDAO().modifier_configuration_automate(ConfigurationAutomateJohnConway(
                                config_modification.identifiant,
                                requete_json["nom"],
                                [int(requete_json["largeur"]),
                                 int(requete_json["hauteur"]),
                                 requete_json["etat_initial"]]
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
    response = make_response(json.dumps({"message": "La modification de la configuration a échoué"}))
    response.headers.set("Content-type", "application/json; charser=utf8")
    return response, 400

# Supprimer une configuration
@api.route("/configuration/supprimer/<identifiant>")
def supprimer_configuration(identifiant: int):
    if "pseudo" in session:
        pseudo = session["pseudo"]
        print(f"Tentative de suppression de la configuration {identifiant} provenant de {request}, de l'utilisateur {pseudo}")
        if pseudo != "Anonyme":
            # vérifier si l'utilisateur existe
            try:
                resultat_requete_utilisateur = DAOSingleton.getDAO().obtenir_utilisateur_par_pseudo(pseudo)
                if resultat_requete_utilisateur[1]:
                    utilisateur = resultat_requete_utilisateur[0]
                    # vérifier si la configuration appartient à l'utilisateur
                    if int(identifiant) in utilisateur.identifiants_configurations_automate and int(identifiant) != 1:
                        DAOSingleton.getDAO().supprimer_configuration_automate_par_identifiant(int(identifiant))
                        utilisateur.supprimer_configuration(int(identifiant))
                        response = make_response()
                        return response, 200
                    else:
                        print(
                            f"La tentative de suppresion de la configuration {identifiant} provenant de {request} a échoué,"
                            f"la configuration n'appartient pas à l'utilisateur {pseudo}")
                else:
                    print(f"La tentative de suppresion de la configuration {identifiant} provenant de {request} a échoué,"
                          f"l'utilisateur {pseudo} est introuvable")
            except:
                print(f"La tentative de suppresion de la configuration {identifiant} provenant de {request} a échoué")
                traceback.print_exc()
        else:
            print(f"La tentative de suppression de la configuration {identifiant} provenant de {request} a échoué,"
                  f"le client a une session anonyme")
    else:
        print(f"La tentative de suppresion de la configuration {identifiant} provenant de {request} a échoué, "
              f"le client n'a pas de session")
    response = make_response(json.dumps({"message": "La suppresion de la configuration a échoué"}))
    response.headers.set("Content-type", "application/json; charser=utf8")
    return response, 400

# Tentative de connexion utilisateur
@api.route("/utilisateur/connecter", methods=['POST'])
def connecter_utilisateur():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
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
    recuperationUtilisateurAnonyme = DAOSingleton.getDAO().obtenir_utilisateur_par_pseudo("Anonyme")
    if recuperationUtilisateurAnonyme[1]:
        session["pseudo"] = "Anonyme"
        utilisateurAnonyme = recuperationUtilisateurAnonyme[0]
        reponse_json = creer_informations_utilisateur(utilisateurAnonyme)
        print("L'utilisateur suivant s'est connecté à une session existante: " + str(json.dumps(reponse_json)))
        response = make_response(json.dumps(reponse_json))
        response.headers.set("Content-type", "application/json; charser=utf8")
        return response, 200
    else:
        print(f"L'initialisation d'une nouvelle session anonyme a échouée {request}")
        reponse = make_response()
        return reponse, 400

# Nouvel utilisateur
@api.route("/utilisateur/creer", methods=['POST'])
def creer_utilisateur():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        if "pseudo" in session:
            if session["pseudo"] == "Anonyme":
                requete_json = request.json
                try:
                    resultat_creation_utilisateur = DAOSingleton.getDAO().ajouter_nouvel_utilisateur(requete_json["pseudo"], requete_json["mot_de_passe"])
                    if resultat_creation_utilisateur:
                        nouvel_utilisateur = DAOSingleton.getDAO().obtenir_utilisateur_par_pseudo(requete_json["pseudo"])[0]
                        reponse_json = creer_informations_utilisateur(nouvel_utilisateur)
                        session["pseudo"] = nouvel_utilisateur.pseudo
                        response = make_response(json.dumps(reponse_json))
                        response.headers.set("Content-type", "application/json; charser=utf8")
                        return response, 200
                    else:
                        print(f"La tentative de créer un compte, provenant de {request} "
                  f"a échoué, le pseudo est déjà utilisé")
                        response = make_response(json.dumps({"message": "Ce pseudo est déjà utilisé"}))
                        response.headers.set("Content-type", "application/json; charser=utf8")
                        return response, 400
                    # renvoyer les informations du compte nouvellement créé
                except:
                    response = make_response(json.dumps({"message": "Création de compte impossible"}))
                    response.headers.set("Content-type", "application/json; charser=utf8")
                    return response, 400
            else:
                print(f"La tentative de créer un compte, provenant de {request} "
                    f"a échoué, le client a déjà une session non-anonyme")
        else:
            print(f"La tentative de créer un compte, provenant de {request} "
                  f"a échoué, le client n'a pas de session anonyme")
    else:
        print(f"La tentative de créer un compte, provenant de {request} "
              f"a échoué, le corps de la requête n'est pas un json")
    response = make_response(json.dumps({"message": "Création de compte impossible"}))
    response.headers.set("Content-type", "application/json; charser=utf8")
    return response, 400

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

if __name__ == "__main__":
    #api = lancer_api_test()
    api = lancer_api()
    api.run()