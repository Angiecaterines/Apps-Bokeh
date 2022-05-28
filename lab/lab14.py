# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 22:13:24 2021

@author: angie.sarmiento
"""

import numpy as np
import pandas as pd
import edhec_risk_kit_114 as erk

ind_return = erk.get_ind_returns()
tmi_return = erk.get_total_market_index_returns()

# Configurar los párametros de CPPI

# Activo arriesgado
risky_r = ind_return["2000":][["Steel", "Fin", "Beer"]]
# Activo libre o seguro
safe_r = pd.DataFrame().reindex_like(risky_r)
safe_r.values[:] = 0.03/12 # fast way to set all values to a number
start = 1000 # start at $1000
floor = 0.80 # set the floor to 80 percent of the starting value

# 1. Cojin -> Valor del activo(CPPI) - El valor minimo(floor)
# 2. Calcular los activos seguros y arriesgados --> m* Presupuesto de riesgo
# 3. Calcular el valor dela ctivo en fundción de los rendimientos

##Configurar algunos DataFrames para guardar valores intermedios
dates = risky_r.index
n_steps = len(dates)
account_value = start
floor_value = start*floor
m = 3
# Presupuesto de riesgo
# Asignación a los seguros y arriesgados

account_history = pd.DataFrame().reindex_like(risky_r)
risky_w_history = pd.DataFrame().reindex_like(risky_r)
cushion_history = pd.DataFrame().reindex_like(risky_r)

for step in range(n_steps):
    cushion = (account_value - floor_value)/account_value
    risky_w = m*cushion
    risky_w = np.minimum(risky_w, 1)
    risky_w = np.maximum(risky_w, 0)
    safe_w = 1-risky_w
    risky_alloc = account_value*risky_w
    safe_alloc = account_value*safe_w
    # recompute the new account value at the end of this step
    account_value = risky_alloc*(1+risky_r.iloc[step]) + safe_alloc*(1+safe_r.iloc[step])
    # save the histories for analysis and plotting
    cushion_history.iloc[step] = cushion
    risky_w_history.iloc[step] = risky_w
    account_history.iloc[step] = account_value
    risky_wealth = start*(1+risky_r).cumprod()

account_history.head()
risky_wealth = start*(1+risky_r).cumprod()
risky_wealth.plot()

#### parte 2

ind = "Beer"
ax = account_history[ind].plot(figsize=(12,6))
risky_wealth[ind].plot(ax = ax, style="k:")
ax.axhline(y=floor_value, color = "r",linestyle="--")

####
risky_w_history.plot()

##
ind = "Fin"
ax = account_history[ind].plot(figsize=(12,6))
risky_wealth[ind].plot(ax = ax, style="k:")
ax.axhline(y=floor_value, color = "r",linestyle="--")

##
ind = "Steel"
ax = account_history[ind].plot(figsize=(12,6))
risky_wealth[ind].plot(ax = ax, style="k:")
ax.axhline(y=floor_value, color = "r",linestyle="--")

erk.summary_stats(risky_r)
btr = erk.run_cppi(risky_r)
erk.summary_stats(btr["Wealth"].pct_change().dropna())

btr = erk.run_cppi(tmi_return["2007":])
ax = btr["Wealth"].plot(legend=False)
btr["Risky Wealth"].plot(ax=ax,style="k--",legend=False)

erk.summary_stats(btr["Risky Wealth"]).pct_change().dropna()

erk.summary_stats(btr["Wealth"]).pct_change().dropna()


## reduccion
btr = erk. run_cppi(ind_return["2007":][["Steel","Fin","Beer"]],drawdown=0.25)
ax = btr["Wealth"].plot()
btr["Risky Wealth"].plot(ax=ax,style="--")
erk.summary_stats(btr["Risky Wealth"].pct_change().dropna())
erk.summary_stats(btr["Wealth"].pct_change().dropna())
