# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 16:12:40 2021

@author: angie.sarmiento
"""

import pandas as pd
import numpy as np


returns1 = pd.read_csv('C:/Users/angie.sarmiento/Documents/Cursos/introduction-portafolio/data/Portfolios_Formed_on_ME_monthly_EW.csv',
                       header=0,index_col=0,parse_dates=True,na_values=-99.99)
returns1.index = pd.to_datetime(returns1.index,format="%Y%m")
columns = ["Lo 10", "Hi 10"]
returns1 = returns1[columns]
returns1 = returns1/100
returns1.columns =['SmallCap','LargeCap']
returns1.plot.line()
returns1.index = returns1.index.to_period("M")
returns1["1975"]

## calculo Drawdowns

#1) indice de riqueza
#2) calcular picos anteriores
#3) Carcular la reduccion- que es el valor de la riqueza como porcentaje del pico anterior

indice_riqueza = 1000*(1+returns1["LargeCap"]).cumprod()
indice_riqueza.plot.line()

pasos_anteriores= indice_riqueza.cummax()
pasos_anteriores.plot.line()

reduccion = (indice_riqueza - pasos_anteriores)/pasos_anteriores
reduccion.plot()
reduccion.min()
reduccion["1975":].idxmin()
reduccion.idxmin()

def reduccion1(serie_retornos:pd.Series):
    """
    toma una seriede retornos 
    Calcula y computo  un DataFrame que contiene:
    el indice de riqueza,
    los picos anteriores
    porcentaje de reducción
    """
    indice_riqueza = 1000*(1+serie_retornos).cumprod()
    pasos_anteriores= indice_riqueza.cummax()
    reduccion = (indice_riqueza - pasos_anteriores)/pasos_anteriores
    return pd.DataFrame({
        "Riqueza":np.round(indice_riqueza,decimals=3),
        "Pasos":np.round(pasos_anteriores,decimals=3),
        "Reduccion":np.round(reduccion*100,decimals=3)
        })
reduccion1(returns1["LargeCap"]).plot()
reduccion1(returns1["LargeCap"])[["Riqueza","Pasos"]].plot()
reduccion1(returns1["LargeCap"])[["Reduccion"]].plot()
