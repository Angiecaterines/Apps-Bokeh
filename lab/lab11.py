# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 16:23:49 2021

@author: angie.sarmiento
"""

import numpy as np
import pandas as pd
import edhec_risk_kit_111 as erk

ind = erk.get_ind_returns()
er = erk.annualize_rets(ind["1995":"2000"],12)
cov = ind["1999":"2000"].cov()

l = ["Food","Steel"]
erk.msr(0.1,er[l],cov.loc[l,l])
er[l]
erk.msr(0.1,np.array([.11,.12]) ,cov.loc[l,l])

erk.msr(0.1,np.array([.13,.10]) ,cov.loc[l,l])
erk.plot_ef(20, er, cov,show_cml=True,riskfree_rate=0.1)

### cartera de varianza minima ew

erk.plot_ef(20, er, cov,show_cml=True,riskfree_rate=0.1,show_ew=True)

## portafolio glogal de varianza minima gmv
erk.plot_ef(20, er, cov,show_cml=True,riskfree_rate=0.1,show_ew=True,show_gmv=True)


## la linea azul de puntos es la frotera eficiente
