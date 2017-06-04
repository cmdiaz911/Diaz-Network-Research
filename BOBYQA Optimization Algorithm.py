# -*- coding: utf-8 -*-
"""
Created on Sun Jun 04 15:40:09 2017

@author: Chris
"""

import nlopt
from numpy import *

opt = nlopt.opt(nlopt.LN_BOBYQA, 2)

print opt.get_algorithm_name()