# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 07:01:25 2021

@author: angie.sarmiento
"""

import numpy as np
import pandas as pd
import edhec_risk_kit_111 as erk

ind = erk.get_hfi_returns()
(erk.var_gaussian(ind["2000":],level=1))*100

(erk.var_gaussian(ind["2000":],level=1,modified=True))*100

(erk.var_historic(ind["2000":],level=1))*100


ind = erk.get_ind_returns()
ind = ind["2013":"2017"]
er = erk.annualize_rets(ind,12)
cov = ind.cov()
l=["Books","Steel","Oil","Mines"]
np.round(erk.msr(0.10, er[l], cov.loc[l,l]),decimals=10)*100
n = er[l].shape[0]
w_ew = np.repeat(1/n, n)*100

w_gmv = np.round(gmv(cov.loc[l,l])*100,decimals=4)

erk.portfolio_vol(ind["2018"][l])
