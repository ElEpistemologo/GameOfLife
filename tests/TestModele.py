import unittest

import config
config.configurer_pythonpath()

from ConfigurationAutomateJohnConway import ConfigurationAutomateJohnConway
from AutomateJohnConway import AutomateJohnConway

class TestAutomateJohnConway(unittest.TestCase):

    def test_constructeur_1(self):
        config = ConfigurationAutomateJohnConway(1, "config JC", [5, 5, [[True, False, True, False, False],
                                                                  [True, False, True, False, False],
                                                                  [True, False, True, False, False],
                                                                  [True, False, True, False, False],
                                                                  [True, False, True, False, False]]])
        automate = AutomateJohnConway(config)
        self.assertIsInstance(automate, AutomateJohnConway)
        self.assertEqual(len(automate.automate), 5)

if __name__ == "__main__":
        unittest.main()