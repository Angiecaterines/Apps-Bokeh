# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 21:14:54 2021

@author: angie.sarmiento
"""
import numpy as np
import pandas as pd
import edhec_risk_kit_108 as erk

ind = erk.get_ind_returns()
er = erk.annualize_rets(ind["1995":"2000"],12)
er.sort_values().plot.bar()

## matriz de covarianza

cov = ind["1999":"2000"].cov()

l = ["Food","Beer","Smoke","Coal"]
er[l]
cov.loc[l,l]

weights= np.repeat(1/4,4)
erk.portfolio_return(weights,er[l])
erk.portfolio_vol(weights,cov.loc[l,l])

### frontera de dos activos

l = ["Games","Fin"]
n_points = 20
weights = [np.array([w, 1-w]) for w in np.linspace(0, 1, n_points)]
rets = [erk.portfolio_return(w, er[l]) for w in weights]
vols = [erk.portfolio_vol(w, cov.loc[l,l]) for w in weights]
ef = pd.DataFrame({
        "Returns": rets, 
        "Volatility": vols
    })
ef.plot.scatter(x="Volatility", y="Returns", style=".-")

l= ["Fin","Beer"]
erk.plot_ef2(n_points, er, cov)
