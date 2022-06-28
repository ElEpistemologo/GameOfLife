#!/usr/bin/python

import config
config.configurer_pythonpath()
from DaoTest import DaoTest
import Api

Api.lancer_api(DaoTest())