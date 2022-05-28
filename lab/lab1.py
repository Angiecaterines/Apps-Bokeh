# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 13:38:19 2021

@author: angie.sarmiento
"""

import numpy as np
import pandas as pd
import matplotlib

precios = [8.70, 8.91, 8.71]
(precios[1]/precios[0])-1

# con numpy
precio = np.array([8.70, 8.91, 8.71])
retornos = precio[1:]/precio[:-1]-1

# con pandas
prices = pd.DataFrame({"BLUE": [8.70, 8.91, 8.71, 8.43, 8.73],
                      "ORANGE": [10.66, 11.08, 10.71, 11.59, 12.11]}
                      )

# metodo con indexación
prices.iloc[1:].values/prices.iloc[:-1]-1

# metodo con alineación
prices / prices.shift(1)-1

# calcula los retornos inmediatos
prices.pct_change()

prices1 = pd.read_csv('C:/Users/angie.sarmiento/Documents/Cursos/introduction-portafolio/data/sample_prices.csv')
returns = prices1.pct_change()
prices1.plot()
returns.plot.bar()
returns.std()
returns.mean()
returns+1
## retorno total
np.prod(returns+1)
(returns+1).prod()-1
(((returns+1).prod()-1)*100).round(2)

## Anualizacion

# anual
rm = 0.01
((1+rm)**12-1)*100

# trimestral
rq = 0.04
((1+rq)**4-1)*100

# diaria, 252 porque hay 252 dias de negociacion
rd = 0.0001
((1+rd)**252-1)*100
