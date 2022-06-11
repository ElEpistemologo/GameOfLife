import unittest

import config
config.configurer_pythonpath()
import Api
from DaoTest import DaoTest

daoTest = DaoTest()
Api.lancer_api(daoTest)
