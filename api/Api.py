import json

from flask import Flask, make_response, request
from DaoInterface import DaoInterface
from ConfigurationAutomateInterface import ConfigurationAutomateInterface
from flask_cors import CORS

api = Flask(__name__)
cors = CORS(api, resources={r"/*":{"origins":"*"}})

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
    def getDAO() -> ConfigurationAutomateInterface:
        return DAOSingleton.dao

def lancer_api(dao: DaoInterface):
    daoSingleton = DAOSingleton()
    daoSingleton.setDAO(dao)
    api.config.update(ENV="development", DEBUG=True)
    api.run()

# Accéder à une configuration par son identifiant
@api.route("/configuration/obtenir/<identifiant>")
def retourner_configuration(identifiant):
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

# Enregistrer une configuration
@api.route("/configuration/enregistrer")
def enregistrer_configuration(identifiant: int):

    print(request)
    #DAOSingleton.getDAO().ajouter_configuration_automate

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
                reponse_json = {}
                reponse_json["pseudo"] = utilisateur.pseudo
                iterateur_configuration = 0
                while iterateur_configuration < len(utilisateur.identifiants_configurations_automate):
                    identifiant_configuration = utilisateur.identifiants_configurations_automate[iterateur_configuration]
                    resultat_recherche_config = DAOSingleton.getDAO().obtenir_configuration_automate_par_identifiants([identifiant_configuration])
                    if ( resultat_recherche_config[1]):
                        nom_configuration = resultat_recherche_config[0][0].nom
                        reponse_json.update({identifiant_configuration : nom_configuration})
                    else:
                        print(f"Une configuration de l'utilisateur {utilisateur.pseudo} n'a pas été trouvée")
                    iterateur_configuration += 1
                print("L'utilisateur suivant s'est connecté: " + str(json.dumps(reponse_json)))
                response = make_response(json.dumps(reponse_json))
                response.headers.set("Content-type", "application/json; charser=utf8")
                return response
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
        return 'Content-Type not supported!'


# Déconnexion utilisateur
@api.route("/utilisateur/deconnecter")
def deconnecter_utilisateur():
    print(request)
    pass

# Nouvel utilisateur
@api.route("/utilisateur/creer")
def creer_utilisateur(pseudo: str, mot_de_passe: str):
    print(request)
    pass
