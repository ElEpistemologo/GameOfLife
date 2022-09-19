from typing import List
from mysql.connector import connect, DatabaseError, InterfaceError, Error
from ast import literal_eval
import json
import sys

from ConfigurationAutomateInterface import ConfigurationAutomateInterface
from ConfigurationAutomateJohnConway import ConfigurationAutomateJohnConway
from DaoInterface import DaoInterface
from Utilisateur import Utilisateur

FICHIER_INFO_DB = "Fichier_info_db"
fichier = None
info_db = {}
try:
    fichier = open(FICHIER_INFO_DB, "r")
    ligne = fichier.readline().strip()
    info_db.update({"host":ligne})
    ligne = fichier.readline().strip()
    info_db.update({"user": ligne})
    ligne = fichier.readline().strip()
    info_db.update({"password": ligne})
    ligne = fichier.readline().strip()
    info_db.update({"database": ligne})
except IOError as erreur:
    print(f"Les informations de la base de données pas pu être lue")
    sys.exit(1)
finally:
    if fichier:
        fichier.close()

config_par_defaut = 4

class DaoMySQL (DaoInterface):

    def __init__(self):
        self.connexion = None
        try:
            self.connexion = connect(pool_name="pool_connections", pool_size=5,
                                     host=info_db["host"], user=info_db["user"],
                                     password=info_db["password"], database=info_db["database"])
            print(f"Connexion à la base de donnée réussie")
        except (InterfaceError, DatabaseError) as erreur:
            print(f"La connexion à la base a échoué: {erreur}")

    def obtenir_utilisateur_par_pseudo(self, pseudo: str) -> [Utilisateur, bool]:

        cnx = connect(pool_name = "pool_connections")

        curseur = cnx.cursor()
        curseur2 = cnx.cursor()
        requete = "SELECT * FROM utilisateurs WHERE pseudo=%s"
        curseur.execute(requete, (pseudo,))
        utilisateur = None
        pseudo_utilisateur = None
        mot_de_passe_utilisateur = None
        configurations_utilisateur = []
        for (pseudo, mot_de_passe) in curseur:
            pseudo_utilisateur = pseudo
            mot_de_passe_utilisateur = mot_de_passe
        requete = "SELECT * FROM reference WHERE pseudo=%s"
        curseur2.execute(requete, (pseudo,))
        for (pseudo, id) in curseur2:
            configurations_utilisateur.append(id)

        utilisateur = Utilisateur(pseudo_utilisateur, mot_de_passe_utilisateur, configurations_utilisateur)
        curseur.close()
        curseur2.close()
        cnx.close()
        if utilisateur is not None:
            return [utilisateur, True]
        else:
            return [None, False]

    #TODO: ajouter la gestion des exceptions pour si la requete échoue et retourner False dans ce cas
    def ajouter_nouvel_utilisateur(self, pseudo: str, mot_de_passe: str) -> bool:

        cnx = connect(pool_name="pool_connections")
        curseur = cnx.cursor()
        curseur2 = cnx.cursor()

        try :
            requete = "INSERT INTO utilisateurs VALUES (%s, %s)"
            curseur.execute(requete, (pseudo, mot_de_passe))
            requete = "INSERT INTO reference VALUES (%s, %s)"
            curseur2.execute(requete, (pseudo, config_par_defaut))
            cnx.commit()
            return True

        except Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            return False
        finally:
            curseur.close()
            curseur2.close()
            cnx.close()


    # TODO: ajouter la gestion des exceptions pour si la requete échoue et retourner False dans ce cas
    def supprimer_nouvel_utilisateur_par_pseudo(self, pseudo: str) -> bool:

        cnx = connect(pool_name="pool_connections")
        curseur = cnx.cursor()
        curseur2 = cnx.cursor()
        try:
            #suppression des configurations qui lui appartiennent
            requete = "DELETE FROM configurations WHERE id IN (SELECT id FROM reference WHERE pseudo = %s) AND id != %s"
            curseur.execute(requete, (pseudo,config_par_defaut))
            #suppression de l'utilisateur
            requete = "DELETE FROM utilisateurs WHERE pseud=%s"
            curseur2.execute(requete, (pseudo,))
            cnx.commit()
            curseur.close()
            curseur2.close()
            cnx.close()
            return True

        except Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            return False

        finally:
            curseur.close()
            curseur2.close()
            cnx.close()

    def obtenir_configuration_automate_par_identifiants(self, identifiants: List[int]) -> [
        List[ConfigurationAutomateInterface], bool]:

        cnx = connect(pool_name="pool_connections")
        try:
            curseur = cnx.cursor()
            requete = "SELECT * FROM configurations WHERE id IN ({c})".format(c=', '.join(['%s']*len(identifiants)))
            curseur.execute(requete, tuple(identifiants))
            configurations = []
            for (id, nom, parametres) in curseur:
                parametres_json = json.loads(parametres)
                parametre = [int(parametres_json["largeur"]), int(parametres_json["hauteur"]), literal_eval(parametres_json["etat_initial"])]
                configurations.append(ConfigurationAutomateJohnConway(id, nom, parametre))

            if configurations is None:
                return [None, False]
            else:
                return [configurations, True]

        except Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            return False

        finally:
            curseur.close()
            cnx.close()

    def ajouter_configuration_automate(self, nom: str, parametres: List, pseudo_utilisateur: str) -> [int, bool]:

        parametres_json = {"largeur":parametres[0], "hauteur":parametres[1], "etat_initial":str(parametres[2])}
        cnx = connect(pool_name="pool_connections")
        try:
            curseur = cnx.cursor()
            curseur2 = cnx.cursor()
            requete = "INSERT INTO configurations (nom,parametres) VALUES (%s,%s)"
            curseur.execute(requete, (nom,json.dumps(parametres_json)))
            requete = "INSERT INTO reference VALUES (%s,%s)"
            curseur2.execute(requete, (pseudo_utilisateur, curseur.lastrowid))
            id_nouvelle_configuration = curseur.lastrowid
            cnx.commit()
            return [id_nouvelle_configuration, True]

        except Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            return False

        finally:
            curseur.close()
            curseur2.close()
            cnx.close()

    def modifier_configuration_automate(self, config: ConfigurationAutomateJohnConway) -> bool:
        try:
            cnx = connect(pool_name="pool_connections")
            curseur = cnx.cursor()
            requete = "UPDATE configurations SET nom=%s, parametres=%s WHERE id=%s"
            curseur.execute(requete, (config.nom, config.json_parametres(), config.identifiant))
            cnx.commit()
            return True

        except Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            return False

        finally:
            curseur.close()
            cnx.close()

    def supprimer_configuration_automate_par_identifiant(self, identifiant: int) -> bool:
        if identifiant != config_par_defaut:
            try:

                cnx = connect(pool_name="pool_connections")
                curseur = cnx.cursor()
                requete = "DELETE FROM configurations WHERE id=%s"
                curseur.execute(requete, (identifiant,))
                cnx.commit()
                return True

            except Error as err:
                print(err)
                print("Error Code:", err.errno)
                print("SQLSTATE", err.sqlstate)
                print("Message", err.msg)
                return False

            finally:
                curseur.close()
                cnx.close()
        else:
            return False