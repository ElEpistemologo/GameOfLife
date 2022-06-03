import unittest

import config
config.configurer_pythonpath()

import modele
import GameOfLifeException

class TestModele(unittest.TestCase):

    def test_initialiser_automate_1(self):
        with self.assertRaises(GameOfLifeException.GameOfLifeException):
            modele.initialiser_automate(5, -1)

    def test_initialiser_automate_2(self):
        with self.assertRaises(GameOfLifeException.GameOfLifeException):
            modele.initialiser_automate(-1, "a")

    def test_initialiser_automate_3(self):
        with self.assertRaises(GameOfLifeException.GameOfLifeException):
            modele.initialiser_automate(100, 10)

    def test_initialiser_automate_4(self):
        automate = modele.initialiser_automate(2, 2)
        self.assertListEqual([["x", "x"], ["x", "x"]], automate)

if __name__ == "__main__":
        unittest.main()