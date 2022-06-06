import unittest
from typing import List

import config
config.configurer_pythonpath()

from ConfigurationAutomateJohnConway import ConfigurationAutomate
from DaoInterface import DaoInterface
from Utilisateur import Utilisateur

class DaoTest(DaoInterface):

    def __init__(self):
        config_automate_1 = ConfigurationAutomate(1,"config_1", 5, 5)
        config_automate_2 = ConfigurationAutomate(2,"config_2", 4, 8)
        config_automate_3 = ConfigurationAutomate(3,"config_3", 2, 12)
        self.table_configurations = [config_automate_1, config_automate_2,config_automate_3]

        utilisateur_1 = ["Wluis", "pswd_Wluis", [1,2]]
        utilisateur_2 = ["Setruan", "pswd_Setruan", [2,7]]
        utilisateur_3 = ["Ooskour", "pswd_Ooskour", [4,5]]
        self.table_utilisateurs = [utilisateur_1, utilisateur_2, utilisateur_3]

    def obtenir_utilisateur_par_pseudo(self, pseudo: str) -> [Utilisateur, bool]:
        for utilisateur in self.table_utilisateurs:
            if utilisateur[0] == pseudo:
                return [utilisateur, True]
        return [[], False]

    def ajouter_nouvel_utilisateur(self, pseudo: str, mot_de_passe: str) -> bool:
        if not self.obtenir_utilisateur_par_pseudo(pseudo)[1]:
            self.table_utilisateurs.append([pseudo, mot_de_passe, []])
            return True
        else:
            return False

    def supprimer_nouvel_utilisateur_par_pseudo(self, pseudo: str) -> bool:
        for iterateur_utilisateur in range(len(self.table_utilisateurs)):
            if self.table_utilisateurs[iterateur_utilisateur][0] == pseudo:
                del self.table_utilisateurs[iterateur_utilisateur]
                return True
        return False

    def obtenir_configuration_automate_par_identifiants(self, identifiants: List[int]) -> List[ConfigurationAutomate]:
        list_config = []
        for identifiants in identifiants:
            for config_existante in self.table_configurations:
                if identifiants == config_existante.identifiant:
                    list_config.append(config_existante)
        return list_config

    def ajouter_configuration_automate(self, parametres: List) -> bool:
        try:
            nouvelle_configuration_automate = ConfigurationAutomate(self.table_configurations[-1].identifiant+1, \
                                                                parametres[0], parametres[1], parametres[2])
            self.table_configurations.append(nouvelle_configuration_automate)
        except Exception as exception:
            return False
        else:
            return True

    def supprimer_configuration_automate_par_identifiant(self, identifiant: int) -> bool:
        for iterateur_configurations_existantes in range(len(self.table_configurations)):
            if self.table_configurations[iterateur_configurations_existantes].identifiant == identifiant:
                del self.table_configurations[iterateur_configurations_existantes]
                return True
        return False

class TestDaoTest(unittest.TestCase):

    def test_obtenir_utilisateur_par_pseudo_1(self):
        dao_test = DaoTest()
        resultats = dao_test.obtenir_utilisateur_par_pseudo("utilisateur_inexistant")
        self.assertEqual(resultats[1], False)
        self.assertEqual(resultats[0], [])
        self.assertEqual(len(dao_test.table_utilisateurs), 3)

    def test_obtenir_utilisateur_par_pseudo_2(self):
        dao_test = DaoTest()
        resultats = dao_test.obtenir_utilisateur_par_pseudo("Wluis")
        self.assertEqual(resultats[1], True)
        self.assertEqual(resultats[0][0], "Wluis")
        self.assertEqual(len(dao_test.table_utilisateurs), 3)

    def test_ajouter_nouvel_utilisateur_1(self):
        dao_test = DaoTest()
        resultat = dao_test.ajouter_nouvel_utilisateur("nouvel_utilisateur", "pswd")
        self.assertEqual(resultat, True)
        self.assertEqual(dao_test.table_utilisateurs[3][0], "nouvel_utilisateur")
        self.assertEqual(dao_test.table_utilisateurs[3][1], "pswd")
        self.assertEqual(dao_test.table_utilisateurs[3][2], [])
        self.assertEqual(len(dao_test.table_utilisateurs), 4)

    def test_ajouter_nouvel_utilisateur_2(self):
        dao_test = DaoTest()
        resultat = dao_test.ajouter_nouvel_utilisateur("Ooskour", "pswdtest")
        self.assertEqual(resultat, False)
        self.assertEqual(len(dao_test.table_utilisateurs), 3)

    def test_supprimer_nouvel_utilisateur_par_pseudo_1(self):
        dao_test = DaoTest()
        resultat = dao_test.supprimer_nouvel_utilisateur_par_pseudo("Ooskour")
        self.assertEqual(resultat, True)
        self.assertEqual(len(dao_test.table_utilisateurs), 2)

    def test_supprimer_nouvel_utilisateur_par_pseudo_2(self):
        dao_test = DaoTest()
        resultat = dao_test.supprimer_nouvel_utilisateur_par_pseudo("Utilisateur_non_existant")
        self.assertEqual(resultat, False)
        self.assertEqual(len(dao_test.table_utilisateurs), 3)

    def test_ajouter_configuration_automate_1(self):
        dao_test = DaoTest()
        resultat = dao_test.ajouter_configuration_automate(["nom_config", 10, 10])
        self.assertEqual(resultat, True)
        self.assertEqual(len(dao_test.table_configurations), 4)

    def test_ajouter_configuration_automate_2(self):
        dao_test = DaoTest()
        resultat1 = dao_test.ajouter_configuration_automate([0, 10, 10])
        resultat2 = dao_test.ajouter_configuration_automate(["nom_config", -10, 10])
        resultat3 = dao_test.ajouter_configuration_automate(["nom_config", 10, -10])
        resultat4 = dao_test.ajouter_configuration_automate(["nom_config", 101, 10])
        resultat5 = dao_test.ajouter_configuration_automate(["nom_config", 10, 101])
        self.assertEqual(resultat1, False)
        self.assertEqual(resultat1, False)
        self.assertEqual(resultat1, False)
        self.assertEqual(resultat1, False)
        self.assertEqual(resultat1, False)

    def test_obtenir_configuration_automate_par_identifiants_1(self):
        dao_test = DaoTest()
        config = dao_test.obtenir_configuration_automate_par_identifiants([2])
        self.assertEqual(config[0].__str__(), "{\"Identifiant\":2,\"Nom\":\"config_2\",\"Largeur\":4,\"Hauteur\":8}")

    def test_obtenir_configuration_automate_par_identifiants_2(self):
        dao_test = DaoTest()
        self.assertEqual(dao_test.obtenir_configuration_automate_par_identifiants([4]), [])

    def test_supprimer_configuration_automate_par_identifiant_1(self):
        dao_test = DaoTest()
        result = dao_test.supprimer_configuration_automate_par_identifiant(2)
        self.assertEqual(len(dao_test.table_configurations), 2)
        self.assertEqual(dao_test.obtenir_configuration_automate_par_identifiants([2]), [])
        self.assertEqual(result, True)

    def test_supprimer_configuration_automate_par_identifiant_2(self):
        dao_test = DaoTest()
        result = dao_test.supprimer_configuration_automate_par_identifiant(0)
        self.assertEqual(len(dao_test.table_configurations), 3)
        self.assertEqual(result, False)

if __name__ == "__main__":
    unittest.main()