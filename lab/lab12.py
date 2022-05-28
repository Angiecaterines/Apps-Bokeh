# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 09:11:28 2021

Que sucede cuando los mercados caen en terminos de las correlaciones
entre las acciones en el mercado 
@author: angie.sarmiento
"""

import numpy as np
import pandas as pd
import edhec_risk_kit_112 as erk

ind = erk.get_ind_returns()

## indice de mercado

#1 ) Numeor de empresas que componen la industria especifica
ind_returns = erk.get_ind_returns()
ind_nfirms = erk.get_ind_nfirms()
ind_size = erk.get_ind_size()

# se debe averiguar la capitañizacion de mercado de cada uno de estos

ind_mktcap = ind_nfirms * ind_size

# capitalizacion total del mercado que hay en cada industria

total_mktcap = ind_mktcap.sum(axis="columns")
total_mktcap.plot()
ind_capweight = ind_mktcap.divide(total_mktcap,axis = "rows")
ind_capweight["1926"].sum(axis="columns")
ind_capweight[["Fin","Steel"]].plot()

## calculo del rendimiento promedio ponderado
# de cada industria
total_market_return = (ind_capweight*ind_returns).sum(axis="columns")
total_market_return.plot()

# indice total del mercado capweight
# indice ponderado con limite maximo,
total_market_index = erk.drawdown(total_market_return).Wealth
total_market_index.plot()

## examinar los rendimientos
total_market_index["1980":].plot()
total_market_index["1980":].rolling(window=36).plot()
