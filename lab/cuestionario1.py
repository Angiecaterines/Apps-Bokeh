# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 18:52:54 2021

@author: angie.sarmiento
"""
import pandas as pd
import numpy as np
import edhec_risk_kit_106 as erk

returns1 = pd.read_csv('C:/Users/angie.sarmiento/Documents/Cursos/introduction-portafolio/data/Portfolios_Formed_on_ME_monthly_EW.csv',
                       header=0,index_col=0,parse_dates=True,na_values=-99.99)
returns1.index = pd.to_datetime(returns1.index,format="%Y%m")
columns = ["Lo 20", "Hi 20"]
returns1 = returns1[columns]
## se divide por 100 por que los retornos estan en porcentajes
returns1 = returns1/100

annualized_vol = returns1.std()*np.sqrt(12)

# retornos por mes
returns_per_month =(returns1+1).prod()**(1/returns1.shape[0])-1

annualized_return = (returns_per_month +1)**12 -1
annualized_re=(returns1+1).prod()**(12/returns1.shape[0])-1

## volatilidad anualizada en un periodo

returns1.index = returns1.index.to_period("M")
aa=returns1["1999":"2015"]
annualized_rea=((aa+1).prod()**(12/aa.shape[0])-1)*100
annualized_vola = aa.std()*np.sqrt(12)*100


### reducciones

indice_riqueza = 1000*(1+returns1["Hi 20"]).cumprod()
indice_riqueza.plot.line()

pasos_anteriores= indice_riqueza.cummax()
pasos_anteriores.plot.line()

reduccion = (indice_riqueza - pasos_anteriores)/pasos_anteriores
(reduccion["1999":"2015"]*-1).idxmax()*100
reduccion.plot()
reduccion.min()
reduccion["1975":].idxmin()
reduccion.idxmin()

##semidevianzas

hfi = erk.get_hfi_returns()
hfi = hfi["2000":]
erk.semideviation(hfi).sort_values()
erk.skewness(hfi).sort_values()
erk.kurtosis(hfi).sort_values()

