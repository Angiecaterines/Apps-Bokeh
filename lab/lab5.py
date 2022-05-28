# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 09:23:06 2021

@author: angie.sarmiento
"""
# desviacion de la normalidad

import pandas as pd
import edhec_risk_kit_105 as erk
import scipy.stats
import numpy as np

hfi = erk.get_hfi_returns()
hfi.head()
hfi.plot()
pd.concat([hfi.mean(),hfi.median(),hfi.mean()>hfi.median()],axis="columns")

## calculo de la asimetria
## sort values ordena de mayor a menor
erk.skewness(hfi).sort_values()

# calculo con la libreiria scipy.stats
scipy.stats.skew(hfi)
erk.skewness(hfi).plot.line()

normal_rets = np.random.normal(0,0.15, size=(26300,1))
erk.skewness(normal_rets)

## calculo de la curtosis
erk.kurtosis(hfi)

## la funcion de kutosis, arroja el exceso de kurtosis
## es decir lo que sobra de 3

scipy.stats.kurtosis(normal_rets)


## test jarque_bera de normalidad

scipy.stats.jarque_bera(normal_rets)
scipy.stats.jarque_bera(hfi)
erk.is_normal(hfi,0.05)

ffme= erk.get_ffme_returns()
erk.skewness(ffme)
erk.kurtosis(ffme)

erk.is_normal(ffme)
