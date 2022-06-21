import unittest
from typing import List

import config
config.configurer_pythonpath()

from ConfigurationAutomateJohnConway import ConfigurationAutomateJohnConway
from ConfigurationAutomateInterface import ConfigurationAutomateInterface
from DaoInterface import DaoInterface
from Utilisateur import Utilisateur

class DaoTest(DaoInterface):

    def __init__(self):
        config_automate_1 = ConfigurationAutomateJohnConway(1,"Configuration par défaut", [5, 5])
        config_automate_2 = ConfigurationAutomateJohnConway(2,"config_2", [4, 8])
        config_automate_3 = ConfigurationAutomateJohnConway(3,"config_3", [2, 12])
        config_automate_4 = ConfigurationAutomateJohnConway(4,"config_4", [10, 20])
        config_automate_5 = ConfigurationAutomateJohnConway(5,"config_5", [30, 30])
        self.table_configurations = [config_automate_1, config_automate_2,config_automate_3,config_automate_4,config_automate_5]

        utilisateur_1 = Utilisateur("Wluis", "pswd_Wluis", [1,4,2,3])
        utilisateur_2 = Utilisateur("Setruan", "pswd_Setruan", [1,2,3])
        utilisateur_3 = Utilisateur("Ooskour", "pswd_Ooskour", [1,4,5,3])
        utilisateur_4 = Utilisateur("Anonyme", "pswd_Anonyme", [1])
        self.table_utilisateurs = [utilisateur_1, utilisateur_2, utilisateur_3, utilisateur_4]

    def obtenir_utilisateur_par_pseudo(self, pseudo: str) -> [Utilisateur, bool]:
        for utilisateur in self.table_utilisateurs:
            if utilisateur.pseudo == pseudo:
                return [utilisateur, True]
        return [[], False]

    def ajouter_nouvel_utilisateur(self, utilisateur:Utilisateur) -> bool:
        if not self.obtenir_utilisateur_par_pseudo(utilisateur.pseudo)[1]:
            self.table_utilisateurs.append(utilisateur)
            return True
        else:
            return False

    def supprimer_nouvel_utilisateur_par_pseudo(self, pseudo: str) -> bool:
        for iterateur_utilisateur in range(len(self.table_utilisateurs)):
            if self.table_utilisateurs[iterateur_utilisateur].pseudo == pseudo:
                del self.table_utilisateurs[iterateur_utilisateur]
                return True
        return False

    def obtenir_configuration_automate_par_identifiants(self, identifiants: List[int]) -> [List[ConfigurationAutomateInterface], bool]:
        list_config = []
        for identifiants in identifiants:
            for config_existante in self.table_configurations:
                if identifiants == config_existante.identifiant:
                    list_config.append(config_existante)
        if len(list_config) == 0:
            return [[], False]
        else:
            return [list_config, True]


    def ajouter_configuration_automate(self, nom: str, config: List[int]) -> [int, bool]:
        nouvel_identifiant = self.table_configurations[-1].identifiant +1
        try:
            nouvel_automate = ConfigurationAutomateJohnConway(nouvel_identifiant, nom, config)
            self.table_configurations.append(nouvel_automate)
        except Exception:
            return [None, False]
        return [nouvel_identifiant, True]

    def modifier_configuration_automate(self, automate_configuration:ConfigurationAutomateInterface) -> bool:
        indice_a_supprimer = None
        if ( self.obtenir_configuration_automate_par_identifiants([automate_configuration.identifiant])[1]):
            for iterateur in list(range(len(self.table_configurations))):
                if self.table_configurations[iterateur].identifiant == automate_configuration.identifiant:
                    indice_a_supprimer = iterateur
            self.table_configurations.pop(indice_a_supprimer)
            self.table_configurations.append(automate_configuration)
            return True
        else:
            return False

    def supprimer_configuration_automate_par_identifiant(self, identifiant: int) -> bool:
        for iterateur_configurations_existantes in range(len(self.table_configurations)):
            if self.table_configurations[iterateur_configurations_existantes].identifiant == identifiant:
                del self.table_configurations[iterateur_configurations_existantes]
                return True
        return False

class TestDaoTest(unittest.TestCase):

    def test_modifier_configuration_automate_1(self):
        dao_test = DaoTest()
        nombre_config_avant_modif = len(dao_test.table_configurations)
        resultat_modif = dao_test.modifier_configuration_automate(ConfigurationAutomateJohnConway(2,"config_2_modif", [4, 6]))
        self.assertEqual(resultat_modif, True)
        resultat_cherche = dao_test.obtenir_configuration_automate_par_identifiants([2])
        self.assertEqual(resultat_cherche[1], True)
        self.assertEqual(1, len(resultat_cherche[0]))
        self.assertEqual(resultat_cherche[0][0].nom, "config_2_modif")
        self.assertEqual(nombre_config_avant_modif, len(dao_test.table_configurations))

    def test_obtenir_utilisateur_par_pseudo_1(self):
        dao_test = DaoTest()
        resultats = dao_test.obtenir_utilisateur_par_pseudo("utilisateur_inexistant")
        self.assertEqual(resultats[1], False)
        self.assertEqual(resultats[0], [])
        self.assertEqual(len(dao_test.table_utilisateurs), 4)

    def test_obtenir_utilisateur_par_pseudo_2(self):
        dao_test = DaoTest()
        resultats = dao_test.obtenir_utilisateur_par_pseudo("Wluis")
        self.assertEqual(resultats[1], True)
        self.assertEqual(resultats[0].pseudo, "Wluis")

    def test_ajouter_nouvel_utilisateur_1(self):
        dao_test = DaoTest()
        resultat = dao_test.ajouter_nouvel_utilisateur(Utilisateur("nouvel_utilisateur", "pswd", []))
        self.assertEqual(resultat, True)
        self.assertEqual(dao_test.table_utilisateurs[4].pseudo, "nouvel_utilisateur")
        self.assertEqual(dao_test.table_utilisateurs[4].mot_de_passe, "pswd")
        self.assertEqual(dao_test.table_utilisateurs[4].identifiants_configurations_automate, [])
        self.assertEqual(len(dao_test.table_utilisateurs), 5)

    def test_ajouter_nouvel_utilisateur_2(self):
        dao_test = DaoTest()
        resultat = dao_test.ajouter_nouvel_utilisateur(Utilisateur("Ooskour", "pswdtest", []))
        self.assertEqual(resultat, False)
        self.assertEqual(len(dao_test.table_utilisateurs), 4)

    def test_supprimer_nouvel_utilisateur_par_pseudo_1(self):
        dao_test = DaoTest()
        resultat = dao_test.supprimer_nouvel_utilisateur_par_pseudo("Ooskour")
        self.assertEqual(resultat, True)
        self.assertEqual(len(dao_test.table_utilisateurs), 3)

    def test_supprimer_nouvel_utilisateur_par_pseudo_2(self):
        dao_test = DaoTest()
        resultat = dao_test.supprimer_nouvel_utilisateur_par_pseudo("Utilisateur_non_existant")
        self.assertEqual(resultat, False)
        self.assertEqual(len(dao_test.table_utilisateurs), 4)

    def test_ajouter_configuration_automate_1(self):
        dao_test = DaoTest()
        resultat = dao_test.ajouter_configuration_automate("nom_config", [10, 10])
        self.assertEqual(resultat[1], True)
        self.assertEqual(len(dao_test.table_configurations), 6)

    def test_ajouter_configuration_automate_2(self):
        dao_test = DaoTest()
        resultat1 = dao_test.ajouter_configuration_automate(0, [10, 10])
        resultat2 = dao_test.ajouter_configuration_automate("nom_config", [-10, 10])
        resultat3 = dao_test.ajouter_configuration_automate("nom_config", [10, -10])
        resultat4 = dao_test.ajouter_configuration_automate("nom_config", [101, 10])
        resultat5 = dao_test.ajouter_configuration_automate("nom_config", [10, 101])
        self.assertEqual(resultat1[1], False)
        self.assertEqual(resultat1[1], False)
        self.assertEqual(resultat1[1], False)
        self.assertEqual(resultat1[1], False)
        self.assertEqual(resultat1[1], False)

    def test_obtenir_configuration_automate_par_identifiants_1(self):
        dao_test = DaoTest()
        config = dao_test.obtenir_configuration_automate_par_identifiants([2])[0]
        self.assertEqual(config[0].json(), "{\"Identifiant\":2,\"Nom\":\"config_2\",\"Largeur\":4,\"Hauteur\":8}")

    def test_obtenir_configuration_automate_par_identifiants_2(self):
        dao_test = DaoTest()
        self.assertEqual(dao_test.obtenir_configuration_automate_par_identifiants([6])[0], [])

    def test_supprimer_configuration_automate_par_identifiant_1(self):
        dao_test = DaoTest()
        resultat_suppresion = dao_test.supprimer_configuration_automate_par_identifiant(2)
        resultat_request_config = dao_test.obtenir_configuration_automate_par_identifiants([2])
        self.assertEqual(len(dao_test.table_configurations), 4)
        self.assertEqual(True, resultat_suppresion)
        self.assertEqual(False, resultat_request_config[1])
        self.assertEqual([], resultat_request_config[0])

    def test_supprimer_configuration_automate_par_identifiant_2(self):
        dao_test = DaoTest()
        result = dao_test.supprimer_configuration_automate_par_identifiant(6)
        self.assertEqual(len(dao_test.table_configurations), 5)
        self.assertEqual(result, False)

if __name__ == "__main__":
    unittest.main()