# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 15:41:30 2021

@author: angie.sarmiento
"""

### medidas a la baja
import pandas as pd
import edhec_risk_kit_106 as erk
import numpy as np
from scipy.stats import norm
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
from bokeh.transform import factor_cmap,dodge

hfi = erk.get_hfi_returns()

## semidesviacion
## es la desviacion estandar para los valores por debajo de la media
hfi.std(ddof=0)
hfi[hfi<0].std(ddof=0)

erk.semideviation(hfi)

## vaR and CVar
# valor en riesgo

## 1) VaR historico
## 2) VaR paramterico - Gaussiano
## 3) VaR modificada o Cornish - Fisher


## 1)  historico de Retornos
np.percentile(hfi,5,axis=0)

erk.var_historic(hfi)

## 2) var gausiana
## para encontrar los cuantiles ppf
z = norm.ppf(0.05)

## intervalo superior de riesgo al 5%
hfi.mean() + z * hfi.std(ddof=0)

hfi.mean() - z * hfi.std(ddof=0)

erk.var_gaussian(hfi)

## Cornish - Fisher

var_list = [erk.var_gaussian(hfi),erk.var_gaussian(hfi,modified=True),erk.var_historic(hfi)]
comparacion = pd.concat(var_list, axis =1)
comparacion.columns= ["Gausiana","Cornish-Fisher","Historic"]
comparacion.plot.bar(title="EDHEC Hedge:VaR")

##  CVar o VaR condicional
# cvar es el promedio de todos los retornos que
# son peores que el VaR

erk.cvar_historic(hfi)

## si ocurre ese 5% de probabilidad que es el peor 5% de los casos posibles
#  cuando esas cosas sucedan el promedio de eso es una perdida
# de 3.6 por ciento en un mes.

fruits=hfi.columns.tolist()


data = {'fruits'  : fruits,
        'Gausiana': comparacion["Gausiana"].tolist(),
        'Cornish-Fisher': comparacion["Cornish-Fisher"].tolist(),
        'Historic'   : comparacion["Historic"].tolist()}

source = ColumnDataSource(data=data)

p = figure(x_range=fruits, plot_height=350, title="Fruit Counts by Year",
           toolbar_location=None, tools="")

p.vbar(x=dodge('fruits', -0.25, range=p.x_range), top='Gausiana', width=0.2, source=source,
       color="#c9d9d3", legend_label="2015")

p.vbar(x=dodge('fruits',  0.0,  range=p.x_range), top='Cornish-Fisher', width=0.2, source=source,
       color="#718dbf", legend_label="2016")

p.vbar(x=dodge('fruits',  0.25, range=p.x_range), top='Historic', width=0.2, source=source,
       color="#e84d60", legend_label="2017")

p.legend.location = "top_left"
p.legend.orientation = "horizontal"
p.xaxis.major_label_orientation = 1

show(p)

