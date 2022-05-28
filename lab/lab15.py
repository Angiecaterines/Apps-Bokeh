# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 04:38:15 2021

@author: angie.sarmiento
"""

import numpy as np
import edhec_risk_kit_115 as erk
import ipywidgets as widgets
p = erk.gbm(n_years=10, n_scenarios=3)
p.head()
p.plot()

p = erk.gbm(n_years=10, n_scenarios=1000).plot(figsize=(12,6) , legend=False)

erk.gbm(n_years=10, n_scenarios=20).plot(figsize=(12,6) ,legend=False)

def square(n):
    return n*n
square(5)


widgets.interact(square, n=(0,100))
