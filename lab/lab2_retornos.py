# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 17:52:26 2021

@author: angie.sarmiento
"""

#--------------------------------------------------------------------------------------------------------
#                                          Librerias
#--------------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import colorsys
import random
#import dash_html_components as html
import statsmodels.api as sm
import edhec_risk_kit_116 as erk
from os.path import dirname, join
from bokeh.transform import dodge
from bokeh.layouts import*
from bokeh.models import HoverTool
from pandas import DataFrame
from bokeh.io import curdoc,show
from bokeh.layouts import column
from bokeh.models import  (BoxSelectTool, Circle, Column, ColumnDataSource,ranges, PreText,Legend, ImageURL,
                          DataTable, Grid, HoverTool, IntEditor, LinearAxis, DateRangeSlider,Div,Paragraph,
                          NumberEditor, NumberFormatter, Plot, SelectEditor,Button,CheckboxGroup, FactorRange,
                          StringEditor, StringFormatter,Spinner, TableColumn,CustomJS, Select,LassoSelectTool, 
                          Panel, RadioGroup, Tabs,DatePicker,MultiSelect, RangeSlider,TextInput, Slider,CustomJS)
from bokeh.transform import factor_cmap
from bokeh.plotting import figure
from csv import reader
from datetime import datetime,timedelta,date
from scipy import stats
from scipy.stats import chisquare

#--------------------------------------------------------------------------------------------------------
#                                          Datos
#--------------------------------------------------------------------------------------------------------
ind = erk.get_ind_returns()
#--------------------------------------------------------------------------------------------------------
#                                          Widgets
#--------------------------------------------------------------------------------------------------------
## Tab1
titulo_lab1 = Div(text="<b>Frontera Efectiva </b>",
               style={'font-size': '150%', 'color': 'steelblue',
                      'text-align': 'center'})


subtitulo_lab1 = Paragraph(text="""En esta sección se introduce el cálculo de la
frontera efectiva""",
width=200, height=100)

selectm_lab1 = MultiSelect(value=["Food","Smoke","Coal","Beer","Fin"], options=ind.columns.tolist())
date_i = DatePicker(title='Seleccione fecha inicial', value="1926-07", min_date="1926-07", max_date="2018-12")
date_f = DatePicker(title='Seleccione fecha final',  value="2018-12", min_date="1926-07", max_date="2018-12")
boton_lab1=Button(label="enter",button_type ='primary',width=200)

## Tab2
titulo_lab2 = Div(text="<b>Frontera Eficiente de Activos </b>",
               style={'font-size': '150%', 'color': 'steelblue',
                      'text-align': 'center'})


subtitulo_lab2 = Paragraph(text="""En esta sección se introduce el cálculo de la
frontera efectiva""",
width=200, height=100)


boton_lab2=Button(label="enter",button_type ='primary',width=200)

## Tab3

titulo_lab3 = Div(text="<b>Quadprog </b>",
               style={'font-size': '150%', 'color': 'steelblue',
                      'text-align': 'center'})


subtitulo_lab3 = Paragraph(text="""Aplicación de Quadprog para dibujar la 
frontera efectiva""",
width=200, height=100)
boton_lab3=Button(label="enter",button_type ='primary',width=200)

#--------------------------------------------------------------------------------------------------------
#                                          Tablas vacias
#--------------------------------------------------------------------------------------------------------
## Tab1
tabla_ind=ColumnDataSource(data=dict(
      ind
    ))
## Tab2
## Tab3
#--------------------------------------------------------------------------------------------------------
#                                          Funciones
#--------------------------------------------------------------------------------------------------------
## Tab1

def carga():
    a=selectm_lab1.valuea
    ind_datos=np.round(ind[a],decimals=4)
    fi=date_i.value
    ff=date_f.value
    mask = (ind_datos.index > fi) & (ind_datos.index <= ff)
    mask1 =(ind_datos.index > fi) & (ind_datos.index <= ff)
    ind_datos=ind_datos.loc[mask1]
    
    tabla_ind.data=dict(
    np.round(ind_datos,decimals=3))
    
    
     
   
## Tab2
## Tab3
#--------------------------------------------------------------------------------------------------------
#                                          Plots
#--------------------------------------------------------------------------------------------------------
## Tab1
## Tab2
## Tab3
#--------------------------------------------------------------------------------------------------------
#                                          Tablas de datos
#--------------------------------------------------------------------------------------------------------
## Tab1
boton_lab1.on_click(carga)
Cind=[TableColumn(field=Ci, title=Ci) for Ci in tabla_ind.data]
dind= DataTable(source=tabla_ind, columns=Cind, width=300, height=300, index_position=None)
## Tab2
## Tab3


#--------------------------------------------------------------------------------------------------------
#                                          Inputs
#--------------------------------------------------------------------------------------------------------

inputs1 = column(titulo_lab1,subtitulo_lab1,selectm_lab1,date_i,date_f,boton_lab1)
inputs2 = column(titulo_lab2,subtitulo_lab2,boton_lab2)
inputs3 = column(titulo_lab3,subtitulo_lab3,boton_lab3)
#inputs4 = column(titulo_lab4,subtitulo_lab4)
#inputs5 = column(titulo_lab5,subtitulo_lab5)
#inputs6 = column(titulo_lab6,subtitulo_lab6)
layout1=gridplot([[inputs1,dind]])
layout2=gridplot([[inputs2]])
layout3=gridplot([[inputs3]])
#layout4=gridplot([[inputs4]])
#layout5=gridplot([[inputs5]])
#layout6=gridplot([[inputs6]])
tab1 = Panel(child=layout1,title="Laboratorio 7")
tab2 = Panel(child=layout2,title="Laboratorio 8")
tab3 = Panel(child=layout3,title="Laboratorio 9")
#tab4 = Panel(child=layout4,title="Laboratorio 10")
#tab5 = Panel(child=layout5,title="Laboratorio 11")
#tab6 = Panel(child=layout6,title="Laboratorio 12")

tabs = Tabs(tabs=[tab1,tab2,tab3])
curdoc().add_root(tabs)
curdoc().title = "Grafico de escenario"
