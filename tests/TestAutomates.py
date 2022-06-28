#!/usr/bin/python

import unittest
from ConfigurationAutomateJohnConway import ConfigurationAutomateJohnConway
from AutomateJohnConway import AutomateJohnConway


class TestAutomateJohnConway(unittest.TestCase):

    def test_compter_cellule_vivantes(self):
        config = ConfigurationAutomateJohnConway(1, "test", [3, 3, [[False, False, False],
                                                                    [False, True, False],
                                                                    [False, False, False]]])
        automate = AutomateJohnConway(config)
        self.assertEqual(0, automate.compter_cellule_vivante(1,1))

        config = ConfigurationAutomateJohnConway(1, "test", [3, 3, [[False, True, False],
                                                                    [False, True, False],
                                                                    [False, False, False]]])
        automate = AutomateJohnConway(config)
        self.assertEqual(1, automate.compter_cellule_vivante(1, 1))

        config = ConfigurationAutomateJohnConway(1, "test", [3, 3, [[False, False, True],
                                                                    [False, True, False],
                                                                    [True, False, False]]])
        automate = AutomateJohnConway(config)
        self.assertEqual(2, automate.compter_cellule_vivante(1, 1))

        config = ConfigurationAutomateJohnConway(1, "test", [3, 3, [[True, True, True],
                                                                    [True, False, True],
                                                                    [True, True, True]]])
        automate = AutomateJohnConway(config)
        self.assertEqual(8, automate.compter_cellule_vivante(1, 1))

        config = ConfigurationAutomateJohnConway(1, "test", [3, 3, [[False, False, True],
                                                                    [False, False, False],
                                                                    [False, False, False]]])
        automate = AutomateJohnConway(config)
        self.assertEqual(0, automate.compter_cellule_vivante(0, 2))

        config = ConfigurationAutomateJohnConway(1, "test", [3, 3, [[False, True, True],
                                                                    [False, False, True],
                                                                    [False, False, False]]])
        automate = AutomateJohnConway(config)
        self.assertEqual(2, automate.compter_cellule_vivante(0, 2))

        config = ConfigurationAutomateJohnConway(1, "test", [3, 3, [[True, False, False],
                                                                    [False, False, False],
                                                                    [False, False, False]]])
        automate = AutomateJohnConway(config)
        self.assertEqual(0, automate.compter_cellule_vivante(0, 0))

        config = ConfigurationAutomateJohnConway(1, "test", [3, 3, [[True, False, False],
                                                                    [False, True, False],
                                                                    [False, False, False]]])
        automate = AutomateJohnConway(config)
        self.assertEqual(1, automate.compter_cellule_vivante(0, 0))

        config = ConfigurationAutomateJohnConway(1, "test", [3, 3, [[False, False, False],
                                                                    [False, False, False],
                                                                    [True, False, False]]])
        automate = AutomateJohnConway(config)
        self.assertEqual(0, automate.compter_cellule_vivante(0, 0))

        config = ConfigurationAutomateJohnConway(1, "test", [3, 3, [[False, False, False],
                                                                    [False, False, False],
                                                                    [True, True, False]]])
        automate = AutomateJohnConway(config)
        self.assertEqual(1, automate.compter_cellule_vivante(2, 0))

        config = ConfigurationAutomateJohnConway(1, "test", [3, 3, [[False, False, False],
                                                                    [False, False, False],
                                                                    [False, False, True]]])
        automate = AutomateJohnConway(config)
        self.assertEqual(0, automate.compter_cellule_vivante(2, 2))

        config = ConfigurationAutomateJohnConway(1, "test", [3, 3, [[False, False, False],
                                                                    [False, True, True],
                                                                    [False, True, True]]])
        automate = AutomateJohnConway(config)
        self.assertEqual(3, automate.compter_cellule_vivante(2, 2))

    def test_generation_suivante(self):
        config = ConfigurationAutomateJohnConway(1, "test", [3, 3, [[False, True, False],
                                                                    [False, True, False],
                                                                    [False, True, False]]])
        automate = AutomateJohnConway(config)
        automate.generation_suivante()
        print(automate.automate)
        self.assertEqual(False, automate.automate[0][1])
        self.assertEqual(False, automate.automate[2][1])
        self.assertEqual(True, automate.automate[1][0])
        self.assertEqual(True, automate.automate[1][2])
