import json

from flask import Flask, make_response, request
from DaoInterface import DaoInterface
from ConfigurationAutomateInterface import ConfigurationAutomateInterface

api = Flask(__name__)

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
@api.route("/configuration/obtenir/<identifiant>", methods = ["GET"])
def retourner_configuration(identifiant):
        configurations = DAOSingleton.getDAO().obtenir_configuration_automate_par_identifiants([int(identifiant)])
        configurations_json = {}
        iterateur = 0
        while iterateur < len(configurations):
            configurations_json.update({iterateur:configurations[iterateur].parametres_configuration()})
            iterateur += 1
        print(configurations_json)
        response = make_response(json.dumps(configurations_json))
        response.headers.set("Content-type", "application/json; charser=utf8")
        return response

# Accéder à une configuration par son identifiant
@api.route("/configuration/enregistrer", methods = ["POST"])
def enregistrer_configuration(identifiant):

    print(request)
    #DAOSingleton.getDAO().ajouter_configuration_automate

