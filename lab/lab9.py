# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 10:40:39 2021

@author: angie.sarmiento
"""

import numpy as np
import pandas as pd
import edhec_risk_kit_109 as erk

ind = erk.get_ind_returns()
er = erk.annualize_rets(ind["1995":"2000"],12)
er.sort_values().plot.bar()
cov = ind["1999":"2000"].cov()

l = ["Food","Beer","Smoke","Coal"]
l = ["Games","Fin"]
er[l]
cov.loc[l,l]
erk.plot_ef2(20,er[l],cov.loc[l,l],"orange")
erk.plot_ef2(20,er[l],cov.loc[l,l],"cyan")

w15 = erk.minimize_vol(0.15,er[l],cov.loc[l,l])
vol15 = erk.portfolio_vol(w15, cov.loc[l,l])

l = ["Smoke","Fin","Games","Coal"]
erk.plot_ef(25,er[l],cov.loc[l,l])