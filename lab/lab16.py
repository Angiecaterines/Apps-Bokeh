# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 06:12:48 2021

@author: angie.sarmiento
"""

import ipywidgets as widgets
from IPython.display import display
import pandas as pd
import edhec_risk_kit_116 as erk

erk.gbm(10,100).plot(legend=False)

def show_gbm(n_scenarios, mu, sigma):
    """
    Draw the results of a stock price evolution under a Geometric Brownian Motion model
    """
    s_0=100
    prices = erk.gbm(n_scenarios=n_scenarios, mu=mu, sigma=sigma, s_0=s_0)
    ax = prices.plot(legend=False, color="indianred", alpha = 0.5, linewidth=2, figsize=(12,5))
    ax.axhline(y=100, ls=":", color="black")
    # draw a dot at the origin
    ax.plot(0,s_0, marker='o',color='darkred', alpha=0.2)

show_gbm(30, 0.07,0.15)

gbm_controls = widgets.interactive(show_gbm, 
                                   n_scenarios=widgets.IntSlider(min=1, max=1000, step=1, value=1), 
                                   mu=(0., +.2,.01),
                                   sigma=(0, .3, .01)
)
display(gbm_controls)
