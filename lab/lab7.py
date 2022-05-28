# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 20:54:30 2021

@author: angie.sarmiento
"""
import numpy as np
import pandas as pd
import edhec_risk_kit_107 as erk

## rendimientos mensuales de 30 carteras diferentes
ind = pd.read_csv('C:/Users/angie.sarmiento/Documents/Cursos/introduction-portafolio/data/ind30_m_vw_rets.csv',
                       header=0,index_col=0,parse_dates=True)/100


ind.index=pd.to_datetime(ind.index,format="%Y%m").to_period("M")

## str.strip() cambia los strings para eliminar los espacios
ind.columns = ind.columns.str.strip()


ind = erk.get_ind_returns()
erk.drawdown(ind["Food"])["Drawdown"].plot.line(figsize=(12,6))

erk.var_gaussian(ind[["Food","Smoke","Coal","Beer","Fin"]],modified=True)

erk.var_gaussian(ind,modified=True).sort_values().tail()

erk.var_gaussian(ind,modified=True).sort_values().plot.bar()

erk.sharpe_ratio(ind,0.03,12).sort_values().plot.bar(title="Industry Sharpe Ratios",color="cyan")
erk.sharpe_ratio(ind["2000":],0.03,12).sort_values().plot.bar(title="Industry Sharpe Ratios",color="goldenrod")

## retornos esperados
er = erk.annualize_rets(ind["1995":"2000"],12)
er.sort_values().plot.bar()

## matriz de covarianza

cov = ind["1999":"2000"].cov()
