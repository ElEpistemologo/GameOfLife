import unittest
import config
config.configurer_pythonpath()

from ConfigurationAutomateJohnConway import ConfigurationAutomateJohnConway
from Utilisateur import Utilisateur
import GameOfLifeException

class TestConfigurationAutomateJohnConway(unittest.TestCase):

    def test_constructeur_1(self):
        with self.assertRaises(ValueError):
            automate = ConfigurationAutomateJohnConway(1, "nom", [-1, 5])

    def test_constructeur_2(self):
        with self.assertRaises(ValueError):
            automate = ConfigurationAutomateJohnConway(1, "nom", [5, -1])

    def test_constructeur_3(self):
        with self.assertRaises(ValueError):
            automate = ConfigurationAutomateJohnConway(1, "nom", [101, 5])

    def test_constructeur_4(self):
        with self.assertRaises(ValueError):
            automate = ConfigurationAutomateJohnConway(1, "nom", [5, 101])

    def test_constructeur_5(self):
        with self.assertRaises(ValueError):
            automate = ConfigurationAutomateJohnConway(1, 0, [5, 5])

    def test_constructeur_6(self):
        with self.assertRaises(ValueError):
            automate = ConfigurationAutomateJohnConway(40, "nom", [5, 5])

    def test_constructeur_7(self):
        with self.assertRaises(ValueError):
            automate = ConfigurationAutomateJohnConway(-1, "nom", [5, 5])

    def test_constructeur_8(self):
        config_automate = ConfigurationAutomateJohnConway(2, "automateTest", [5, 6])
        jsonAttendu = "{\"Identifiant\":2,\"Nom\":\"automateTest\",\"Largeur\":5,\"Hauteur\":6}"
        self.assertEqual(config_automate.json(), jsonAttendu)

    def test_constructeur_9(self):
        config_automate = ConfigurationAutomateJohnConway(2, "automateTest", [5, 6])
        self.assertIsInstance(config_automate, ConfigurationAutomateJohnConway)

    def test_dictionnaireParametresConfiguration_1(self):
        config_automate = ConfigurationAutomateJohnConway(2, "automateTest", [5, 6])
        self.assertEqual(config_automate.parametres_configuration(),\
                         {"Identifiant":2, "Nom": "automateTest", "Largeur":5, "Hauteur":6})

class TestUtilisateur(unittest.TestCase):

    def test_constructeur_1(self):
        with self.assertRaises(ValueError):
            utilisateur = Utilisateur(1, [])

    def test_constructeur_2(self):
        with self.assertRaises(ValueError):
            utilisateur = Utilisateur("a", [])

    def test_constructeur_3(self):
        with self.assertRaises(ValueError):
            utilisateur = Utilisateur("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", [])

    def test_constructeur_4(self):
        with self.assertRaises(ValueError):
            utilisateur = Utilisateur("Wluis", ["q",4])

    def test_constructeur_5(self):
        with self.assertRaises(ValueError):
            liste_configuration = []
            for i in range(21):
                liste_configuration.append(ConfigurationAutomateJohnConway(1, "nom", [5, 5]))
            utilisateur = Utilisateur("Wluis", liste_configuration)

    def test_constructeur_6(self):
        liste_configuration = [1,2,3,4]
        utilisateur = Utilisateur("Wluis", "pswd", liste_configuration)
        self.assertIsInstance(utilisateur, Utilisateur)
        self.assertEqual(utilisateur.__str__(), "{\"Pseudo\":\"Wluis\",\"Identifiants de configurations\":[1,2,3,4]}")

    def test_constructeur_7(self):
        with self.assertRaises(ValueError):
            liste_configuration = [1,2,3,1]
            utilisateur = Utilisateur("Wluis", liste_configuration)

    def test_constructeur_8(self):
        utilisateur = Utilisateur("Wluis", "pswd")
        self.assertEqual(utilisateur.__str__(), "{\"Pseudo\":\"Wluis\",\"Identifiants de configurations\":[]}")

    def test_supprimer_configuration_1(self):
        liste_configuration = [1, 2, 3, 4]
        utilisateur = Utilisateur("Wluis", "pswd", liste_configuration)
        resultat = utilisateur.supprimer_configuration(3)
        self.assertEqual("{\"Pseudo\":\"Wluis\",\"Identifiants de configurations\":[1,2,4]}", utilisateur.__str__())

    def test_supprimer_configuration_2(self):
        liste_configuration = [1, 2, 3, 4]
        utilisateur = Utilisateur("Wluis", "pswd", liste_configuration)
        resultat = utilisateur.supprimer_configuration(5)
        self.assertEqual("{\"Pseudo\":\"Wluis\",\"Identifiants de configurations\":[1,2,3,4]}", utilisateur.__str__())

    def test_ajouter_nouvelle_configuration_1(self):
        liste_configuration = [1, 2, 3]
        utilisateur = Utilisateur("Wluis", "pswd", liste_configuration)
        resultat = utilisateur.ajouter_nouvelle_configuration(4)
        self.assertEqual("{\"Pseudo\":\"Wluis\",\"Identifiants de configurations\":[1,2,3,4]}", utilisateur.__str__())

    def test_ajouter_nouvelle_configuration_2(self):
        with self.assertRaises(ValueError):
            liste_configuration = [1, 2, 3]
            utilisateur = Utilisateur("Wluis", "pswd", liste_configuration)
            resultat = utilisateur.ajouter_nouvelle_configuration(3)
            self.assertEqual("{\"Pseudo\":\"Wluis\",\"Identifiants de configurations\":[1,2,3]}", utilisateur.__str__())

    def test_ajouter_nouvelle_configuration_3(self):
        with self.assertRaises(ValueError):
            liste_configuration = [1, 2, 3]
            utilisateur = Utilisateur("Wluis", "pswd", liste_configuration)
            resultat = utilisateur.ajouter_nouvelle_configuration("a")
            self.assertEqual("{\"Pseudo\":\"Wluis\",\"Identifiants de configurations\":[1,2,3]}", utilisateur.__str__())

if __name__ == "__main__":
    unittest.main()