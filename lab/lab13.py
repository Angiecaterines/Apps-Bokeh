# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 15:22:23 2021

@author: angie.sarmiento
"""

import numpy as np
import pandas as pd
import edhec_risk_kit_113 as erk

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



#### laboratorio 13
total_market_index["1980":].plot()
## al indice se le trazo una media movil de 36 meses
total_market_index["1980":].rolling(window=36).mean().plot()

## retornos de este indice
tmi_tr36rets = total_market_return.rolling(window=36).aggregate(erk.annualize_rets,periods_per_year=12)
tmi_tr36rets.plot(label="Tre36 mo Return",legend=True)
total_market_return.plot(label="Returns",legend=True)

## correlaciones moviles junto con Multiindexes and 'groupby'

## se calcula la correlación, se produce una serie temporal
# de matrices
ts_corr = ind_returns.rolling(window=36).corr()
ts_corr.index.names = ["date","industry"]

ind_tr36corr = ts_corr.groupby(level="date").apply(lambda cormat:cormat.values.mean() )
ind_tr36corr.plot()

tmi_tr36rets.plot(label="Tr36 Mo Rets",legend=True)
ind_tr36corr.plot(label="Tr36 Mo Corr",legend=True,secondary_y=True)
