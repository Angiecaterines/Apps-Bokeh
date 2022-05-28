# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 14:08:01 2021

@author: angie.sarmiento
"""

import pandas as pd
import numpy as np
prices1 = pd.read_csv('C:/Users/angie.sarmiento/Documents/Cursos/introduction-portafolio/data/sample_prices.csv')
returns = prices1.pct_change()
returns = returns.dropna()
returns.std()
volatilidad=((((returns - returns.mean())**2).sum())/(returns.shape[0]-1))**0.5

## anualizacion de la volatidad
returns.std()*np.sqrt(12)

returns1 = pd.read_csv('C:/Users/angie.sarmiento/Documents/Cursos/introduction-portafolio/data/Portfolios_Formed_on_ME_monthly_EW.csv',
                       header=0,index_col=0,parse_dates=True,na_values=-99.99)

columns = ["Lo 10", "Hi 10"]
returns1 = returns1[columns]
## se divide por 100 por que los retornos estan en porcentajes
returns1 = returns1/100
returns1.columns =['SmallCap','LargeCap']
returns1.plot.line()
returns1.std()
annualized_vol = returns1.std()*np.sqrt(12)

# retornos por mes
returns_per_month =(returns1+1).prod()**(1/returns1.shape[0])-1

annualized_return = (returns_per_month +1)**12 -1
annualized_re=(returns1+1).prod()**(12/returns1.shape[0])-1

annualized_return/annualized_vol
riskfree_rate = 0.03
excess_return = annualized_return -riskfree_rate
sharpe_ratio = excess_return/annualized_vol



