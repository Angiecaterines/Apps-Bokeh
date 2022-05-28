# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 08:33:01 2021

@author: angie.sarmiento
"""

## construcción de modulos

import pandas as pd

import hello as h

print(h.message)

## para hacer una autorecarga de los nuevos valores
%load_ext autoreload
%autoreload 2
print(h.message)