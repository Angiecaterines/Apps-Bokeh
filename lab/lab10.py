# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 11:47:57 2021

@author: angie.sarmiento
"""

import numpy as np
import pandas as pd
import edhec_risk_kit_110 as erk

ind = erk.get_ind_returns()
er = erk.annualize_rets(ind["1995":"2000"],12)
cov = ind["1999":"2000"].cov()

ax = erk.plot_ef(20,er,cov)
ax.set_xlim(left=0)
rf = 0.1
w_msr = erk.msr(rf,er,cov)
r_msr = erk.portfolio_return(w_msr,er)
vol_msr = erk.portfolio_vol(w_msr,cov)

## linea de mercado de capitales

cml_x = [0,vol_msr]
cml_y = [rf,r_msr]
ax.plot(cml_x,cml_y,color="green",marker="o",linestyle="dashed")
erk.plot_ef(20,er,cov,show_cml=True, riskfree_rate =0.1)