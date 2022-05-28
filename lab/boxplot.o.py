# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 21:25:09 2021

@author: angie.sarmiento
"""
import numpy as np
import pandas as pd
import colorsys
import random
import dash_html_components as html
import statsmodels.api as sm
import edhec_risk_kit_106 as erk
from os.path import dirname, join
from bokeh.transform import dodge
from bokeh.layouts import*
from bokeh.models import HoverTool
from pandas import DataFrame
from bokeh.io import curdoc,show
from bokeh.layouts import column
from bokeh.models import  (BoxSelectTool, Circle, Column, ColumnDataSource,ranges, PreText,Legend,
                          DataTable, Grid, HoverTool, IntEditor, LinearAxis, DateRangeSlider,Div,
                          NumberEditor, NumberFormatter, Plot, SelectEditor,Button,CheckboxGroup,
                          StringEditor, StringFormatter,Spinner, TableColumn,CustomJS, Select,LassoSelectTool, 
                          Panel, RadioGroup, Tabs,DatePicker,MultiSelect, RangeSlider,TextInput, Slider)
from bokeh.plotting import figure
from csv import reader
from datetime import datetime,timedelta,date
from scipy import stats
from scipy.stats import chisquare

hfi = erk.get_hfi_returns()

# aggregated data
cats = hfi.columns.tolist()
mean = hfi.mean().tolist()
q1 = hfi.quantile(0.25).tolist()
q3 = hfi.quantile(0.75).tolist()
iqr = (hfi.quantile(0.25)-hfi.quantile(0.75)).tolist()
upper = (hfi.quantile(0.75) +1.5 *(hfi.quantile(0.25)-hfi.quantile(0.75))).tolist()
lower = (hfi.quantile(0.25) -1.5 *(hfi.quantile(0.25)-hfi.quantile(0.75))).tolist()
p = figure(y_range=cats)

# # stems
p.segment(upper, cats, q3, cats, color="black")
p.segment(lower, cats, q3, cats, color="black")


# boxes
p.hbar(cats, 0.7, q1, mean, fill_color="navy", line_color="black")
p.hbar(cats, 0.7, mean, q3, fill_color="navy", line_color="black")


show(p)
p.xgrid.grid_line_color = None



