# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 13:35:32 2021

@author: angie.sarmiento
"""

import numpy as np
import pandas as pd
import colorsys
import random
#import dash_html_components as html
import statsmodels.api as sm
import edhec_risk_kit_116 as erk
from bokeh.palettes import Category10, Category20
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
                          Panel, RadioGroup, Tabs,DatePicker,MultiSelect, RangeSlider,TextInput, Slider,CustomJS,
                          MultiChoice,LinearAxis,Range1d,RadioButtonGroup)
from bokeh.transform import factor_cmap
from bokeh.plotting import figure
from csv import reader
from datetime import datetime,timedelta,date
from scipy import stats
from scipy.stats import chisquare

#--------------------------------------------------------------------------------------------------------
#                                          Datos
#--------------------------------------------------------------------------------------------------------
ind_returns = erk.get_ind_returns()
ind_nfirms = erk.get_ind_nfirms()
ind_size = erk.get_ind_size()
ind_mktcap = (ind_nfirms * ind_size)
total_mktcap = ind_mktcap.sum(axis="columns")
ind_capweight = ind_mktcap.divide(total_mktcap,axis = "rows")
total_market_return = (ind_capweight*ind_returns).sum(axis="columns")
total_market_index = erk.drawdown(total_market_return).Wealth

## tab 2

## tab 3

ind_return = erk.get_ind_returns()
tmi_return = erk.get_total_market_index_returns()

#--------------------------------------------------------------------------------------------------------
#                                          Widgets
#--------------------------------------------------------------------------------------------------------
## Tab1
titulo_lab1 = Div(text="<b>Capitalización del mercado </b>",
               style={'font-size': '150%', 'color': 'steelblue',
                      'text-align': 'center'})


subtitulo_lab1 = Paragraph(text="""Que sucede cuando los mercados caen en terminos de las correlaciones
entre las industrias en el mercado""",
width=200, height=100)
selectm_lab1 = MultiChoice(value=["Food",'Beer', 'Smoke', 'Games', 'Books', 'Hshld'], options= ind_mktcap.columns.tolist())
date_i = DatePicker(title='Seleccione fecha inicial', value="1926-07", min_date="1926-07", max_date="2018-12")
date_f = DatePicker(title='Seleccione fecha final',  value="2018-12", min_date="1926-07", max_date="2018-12")
boton_lab1=Button(label="enter",button_type ='primary',width=200)

titulo_lab11 = Div(text="<b>Retornos de industrias</b>",
               style={'font-size': '150%', 'color': 'steelblue',
                      'text-align': 'center'})
## Tab2
titulo_lab2 = Div(text="<b>Medias moviles </b>",
               style={'font-size': '150%', 'color': 'steelblue',
                      'text-align': 'center'})


subtitulo_lab2 = Paragraph(text="""En esta sección se desarrolla el cálculo
de la media movil y la correlación movil""",
width=200, height=100)
date_i2 = DatePicker(title='Seleccione fecha inicial', value="1926-07", min_date="1926-07", max_date="2018-12")
date_f2 = DatePicker(title='Seleccione fecha final',  value="2018-12", min_date="1926-07", max_date="2018-12")
spinner2 = Spinner(title="Seleccione la duración del periodo", low=1, high=455, step=1, value=36, width=80)

boton_lab2=Button(label="enter",button_type ='primary',width=200)

## Tab3

titulo_lab3 = Div(text="<b>Implementación del seguro de cartera de proporción constante (CPPI) </b>",
               style={'font-size': '150%', 'color': 'steelblue',
                      'text-align': 'center'})
titulo_lab31 = Div(text="<b>Ingreso de los párametros del CPPI </b>",
               style={'font-size': '150%', 'color': 'steelblue',
                      'text-align': 'center'})

titulo_lab32 = Div(text="<b> Account History </b>",
               style={'font-size': '150%', 'color': 'steelblue',
                      'text-align': 'center'})

titulo_lab33 = Div(text="<b>CPPI para el Indice total del Mercado </b>",
               style={'font-size': '150%', 'color': 'steelblue',
                      'text-align': 'center'})

titulo_lab34 = Div(text="<b>Resumen de Estadisticas</b>",
               style={'font-size': '150%', 'color': 'steelblue',
                      'text-align': 'center'})

titulo_lab35 = Div(text="<b>Drawdown</b>",
               style={'font-size': '150%', 'color': 'steelblue',
                      'text-align': 'center'})

subtitulo_lab3 = Paragraph(text="""Implementando el algoritmo básico de presupuestación de riesgos 
                           dinámicos del seguro de cartera de proporción constante y lo pruebas
                           con diferentes carteras.
                           """,
width=200, height=100)

subtitulo_lab31 = Paragraph(text="""Implementación del seguro de cartera de proporción constante 
                            para el indice total del mercado.
                           """,
width=200, height=100)
date_i3 = DatePicker(title='Seleccione fecha inicial', value="2000-01", min_date="1926-07", max_date="2018-12")
date_f3 = DatePicker(title='Seleccione fecha final',  value="2018-12", min_date="1926-07", max_date="2018-12")
selectm_lab3 = MultiChoice(value=["Steel", "Fin", "Beer"], options= ind_mktcap.columns.tolist())
start1 = Spinner(title="Dinero Inicial (Start)", low=1000, high=10000000000, step=10, value=1000)
floor1 = Slider(title="Seleccione % de riqueza actual(Floor) ",start=0, end=1, value=0.8, step=0.01)
riskfree_ratio = Slider(title="Seleccione tasa libre de riesgo(Riskfree rate) ",start=0, end=1, value=0.03, step=0.01)
m = Slider(start=0, end=100, value=2, step=1, title="Seleccione el multiplicador (m)")
selector31=Select(title="Seleccione una salida del CPPI:", value="Wealth", options=["Wealth","Risky Wealth","Risk Budget","risky_r","safe_r"])
boton_lab3=Button(label="enter",button_type ='primary')

## 2DA PARTE

selector32=Select(title="Seleccione una industria:", value="Fin", options=ind_returns.columns.tolist())
selector33=Select(title="Seleccione una industria:", value="Fin", options=ind_returns.columns.tolist())
selector34=Select(title="Seleccione una industria:", value="Fin", options=ind_returns.columns.tolist())
selector35=Select(title="Seleccione una salida del CPPI:", value="Wealth", options=["Wealth","Risky Wealth","Risk Budget","risky_r","safe_r"])
selector36=Select(title="Seleccione una industria:", value="Fin", options=ind_returns.columns.tolist())
boton_lab31=Button(label="enter",button_type ='primary')


## tab 4

titulo_lab4= Div(text="<b>Caminatas al azar y simulación de montecarlo </b>",
               style={'font-size': '150%', 'color': 'steelblue',
                      'text-align': 'center'})


subtitulo_lab4 = Paragraph(text="""En esta sección se  intoducen los conceptos de paseos aleatorios con retornos de activos y
                           simulaciones de montecarlo.""",
width=200, height=100)

slider41 = Slider(start=0, end=1000, value=10, step=1, title=" Seleccione el número de años")
spinner42 = Spinner(title="Seleccione el número de escenarios", low=0, high=1000, step=1, value=100)
titulo_lab41= Div(text="<b>Parámetros Simulación de Montecarlo</b>",
               style={'font-size': '120%', 'color': 'steelblue',
                      'text-align': 'center'})
slider43 = Slider(start=0, end=1000, value=0.07, step=0.01, title=" Seleccione el valor de mu")
slider44 = Slider(start=0, end=1000, value=0.15, step=0.1, title=" Seleccione el valor de sigma")
spinner43 = Spinner(title="Seleccione el precio inicial de las acciones", low=0, high=1000, step=1, value=100)
spinner44 = Spinner(title="Seleccione el numero de pasos por año", low=0, high=1000, step=1, value=12)
boton_lab4=Button(label="enter",button_type ='primary')

## tab 5

titulo_lab5= Div(text="<b>Simulaciones de Montecarlo de CPPI y GMB</b>",
               style={'font-size': '150%', 'color': 'steelblue',
                      'text-align': 'center'})


subtitulo_lab5 = Paragraph(text="""En esta sección se realizan simulaciónes
                           de Montecarlo para la estrategia de seguros de 
                           portafolio con proporción constante.""",
width=200, height=100)
spinner51 = Spinner(title="Seleccione el número de escenarios", low=1, high=40, step=0.5, value=1000)
spinner52 = Spinner(title="Seleccione el valor de mu", low=0, high=1000, step=0.5, value=0.07)
spinner53 = Spinner(title="Seleccione el valor de sigma", low=0, high=100, step=0.5, value=0.15)
floor2 = Slider(title="Seleccione % de riqueza actual(Floor) ",start=0, end=1, value=0.70, step=0.01)
m1 = Slider(start=0, end=100, value=3, step=1, title="Seleccione el multiplicador (m)")
spinner54 = Spinner(title="Seleccione el número de años", low=1, high=40, step=0.5, value=5)
spinner55 = Spinner(title="Seleccione el número de pasos por año", low=1, high=40, step=0.5, value=52)

spinner57 = Spinner(title="Glyph size", low=1, high=40, step=0.5, value=4, width=80)
boton_lab5=Button(label="enter",button_type ='primary')

#--------------------------------------------------------------------------------------------------------
#                                          Tablas vacias
#--------------------------------------------------------------------------------------------------------
## Tab1
tabla_ind=ColumnDataSource(data=dict(
     ind_returns
    ))

ind_mercado=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[]))

ind_total=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[]))


tabla_ind_weight=ColumnDataSource(data=dict(
    ind_capweight
    ))

ind_weights=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[]))

market_index=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[]))

market_return=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[]))

## Tab2
media_movil_total=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[]))

media_movil_retornos=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[]))

media_movil_correlaciones=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[]))

## Tab3
riqueza_arriesgado=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[]))

selector=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[]))

# 2da parte
aht=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[],
    das=[]))

vs=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[],
    das=[]))

## Tab4


tablas_put=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[]))

tabla1=ColumnDataSource(data=dict(
    freq=[],
    left=[],
    right=[],
    x=[],
    cdf=[]
    ))

## tab 5
tablas_put5=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[]
    ))

tabla5=ColumnDataSource(data=dict(
    freq=[],
    left=[],
    right=[],
    x=[],
    cdf=[]
    ))
#--------------------------------------------------------------------------------------------------------
#                                          Plots
#--------------------------------------------------------------------------------------------------------
## Tab1
plot_mercado=figure(plot_height=300,plot_width=450,title='Capitalización de las industrias del mercado',
                        sizing_mode = "scale_width",
           toolbar_location="above",x_axis_type="datetime",y_axis_type="linear") 

plot_mercado.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=ind_mercado,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
plot_mercado.add_tools(HoverTool(tooltips=[('Fecha', '$x{%F}'),("Valor", "$y{0,0f}"),("Industria","@co")],
          formatters={'$x': 'datetime',
                      '@{y}' : 'printf',
                      '@co' : 'printf'}))

plot_mercado.legend.location = "bottom_left"
plot_mercado.xaxis.axis_label = 'Periodo'
plot_mercado.yaxis.axis_label = 'Capitalizacion'
plot_mercado.title.align = 'center'


# plot 1

plot_total=figure(plot_height=300,plot_width=450,title='Capitalización Total del mercado',
                        sizing_mode = "scale_width",
           toolbar_location="above",x_axis_type="datetime") 

plot_total.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=ind_total,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
plot_total.add_tools(HoverTool(tooltips=[('Fecha', '$x{%F}'),("Valor", "$y{0,0f}")],
          formatters={'$x': 'datetime',
                      '@{y}' : 'printf'}))

plot_total.legend.location = "top_left"
plot_total.xaxis.axis_label = 'Periodo'
plot_total.yaxis.axis_label = 'Capitalizacion Total'
plot_total.title.align = 'center'

# plot 2
plot_weights=figure(plot_height=300,plot_width=450,title='Participación de Industrias en el mercado',
                        sizing_mode = "scale_width",
           toolbar_location="above",x_axis_type="datetime") 

plot_weights.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=ind_weights,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
plot_weights.add_tools(HoverTool(tooltips=[('Fecha', '$x{%F}'),("Valor", "$y{0.000}"),("Industria","@co")],
          formatters={'$x': 'datetime',
                      '@{y}' : 'printf',
                      '@co' : 'printf'}))

plot_weights.legend.location = "top_right"
plot_weights.xaxis.axis_label = 'Periodo'
plot_weights.yaxis.axis_label = 'Porcentaje Representativo'
plot_weights.title.align = 'center'


plot_index=figure(plot_height=300,plot_width=450,title='',
                        sizing_mode = "scale_width",
           toolbar_location="above",x_axis_type="datetime") 

# plot 3
plot_market_r=figure(plot_height=300,plot_width=450,title='Retorno total del Mercado',
                        sizing_mode = "scale_width",
           toolbar_location="above",x_axis_type="datetime") 

plot_market_r.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=market_return,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
plot_market_r.add_tools(HoverTool(tooltips=[('Fecha', '$x{%F}'),("Valor", "$y{0.00}")],
          formatters={'$x': 'datetime',
                      '@{y}' : 'printf'}))

plot_market_r.legend.location = "top_right"
plot_market_r.xaxis.axis_label = 'Periodo'
plot_market_r.yaxis.axis_label = 'retorno total'
plot_market_r.title.align = 'center'

# plot 4
plot_index=figure(plot_height=300,plot_width=450,title='Indice del mercado total',
                        sizing_mode = "scale_width",
           toolbar_location="above",x_axis_type="datetime") 

plot_index.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=market_index,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
plot_index.add_tools(HoverTool(tooltips=[('Fecha', '$x{%F}'),("Valor", "$y{0,00f}")],
          formatters={'$x': 'datetime',
                      '@{y}' : 'printf'
                      }))

plot_index.legend.location = "top_left"
plot_index.xaxis.axis_label = 'Periodo'
plot_index.yaxis.axis_label = 'Indice total del mercado'
plot_index.title.align = 'center'


## Tab2

# plot 1
plot_media=figure(plot_height=400,plot_width=550,title='Indice mercado total Media Movil',
                        sizing_mode = "scale_width",
           toolbar_location="above",x_axis_type="datetime") 

plot_media.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=media_movil_total,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
plot_media.add_tools(HoverTool(tooltips=[('Fecha', '$x{%F}'),("Valor", "$y{0,00f}"),("Indicador","@co")],
          formatters={'$x': 'datetime',
                      '@{y}' : 'printf',
                      '@co' : 'printf'
                      }))

plot_media.legend.location = "top_left"
plot_media.xaxis.axis_label = 'Periodo'
plot_media.yaxis.axis_label = 'Indice total del mercado'
plot_media.title.align = 'center'

### plot 2

plot_media_r=figure(plot_height=400,plot_width=550,title='Indice del mercado total retornos media movil',
                        sizing_mode = "scale_width",
           toolbar_location="above",x_axis_type="datetime") 

plot_media_r.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=media_movil_retornos,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
plot_media_r.add_tools(HoverTool(tooltips=[('Fecha', '$x{%F}'),("Valor", "$y{0,0.00f}"),("Indicador","@co")],
          formatters={'$x': 'datetime',
                      '@{y}' : 'printf',
                      '@co' : 'printf'
                      }))

plot_media_r.legend.location = "top_left"
plot_media_r.xaxis.axis_label = 'Periodo'
plot_media_r.yaxis.axis_label = 'Indice total del mercado'
plot_media_r.title.align = 'center'

## plot 3
plot_media_c=figure(plot_height=400,plot_width=550,title='Correlaciones Media movil',
                        sizing_mode = "scale_width",
           toolbar_location="above",x_axis_type="datetime") 

plot_media_c.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=media_movil_correlaciones,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
plot_media_c.add_tools(HoverTool(tooltips=[('Fecha', '$x{%F}'),("Valor", "$y{0,0.00f}"),("Indicador","@co")],
          formatters={'$x': 'datetime',
                      '@{y}' : 'printf',
                      '@co' : 'printf'
                      }))

plot_media_c.legend.location = "top_left"
plot_media_c.xaxis.axis_label = 'Periodo'
plot_media_c.yaxis.axis_label = 'Indice total del mercado'
plot_media_c.title.align = 'center'

plot_media_c.extra_y_ranges ={'CloseAxis' : Range1d(start= 0.3, end = 0.8)
    }
plot_media_c.add_layout(LinearAxis(y_range_name = 'CloseAxis'),
             'right')
plot_media_c.yaxis[1].axis_label = 'Correlaciones'
plot_media_c.yaxis[1].axis_line_width = 2
plot_media_c.yaxis.axis_label_text_color = 'navy'
plot_media_c.yaxis[1].axis_line_color = 'navy'
plot_media_c.yaxis[1].major_label_text_color = 'navy'
plot_media_c.yaxis.axis_label_text_color = 'darkred'
plot_media_c.yaxis[0].axis_line_color = 'darkred'
plot_media_c.yaxis[0].major_label_text_color = 'darkred'

## tab 4

# plot1
plot=figure(plot_height=450, width=500,title='',
                        sizing_mode = "scale_width",
           toolbar_location="above") 

plot.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=tablas_put,alpha=0.5,
                hover_line_alpha=1.0,hover_line_color='palet')

plot.add_tools(HoverTool(tooltips=[('Valor acción', '$x{0,0.00f}'),("Anos", "$y{0,0.00f}")],
          formatters={'@{x}': 'printf',
                      '@{y}' : 'printf'}))

plot.xaxis.axis_label = 'Valor de la acción'
plot.yaxis.axis_label = 'Años seleccionados'
plot.title.align = 'center'

# plot 2

p = figure(toolbar_location=None, width=500, height=450,
            y_range=plot.y_range, min_border=10, y_axis_location="right",x_axis_location="above",
            tooltips=[('freq','$x')])
p.quad(top='right', bottom='left', right='freq',left=0, 
         color="white", line_color="#3A5785",source=tabla1,
          hover_fill_alpha = 1.0, hover_fill_color = 'navy',alpha=0.5)
p.line('freq','x', line_color="#ff8888", line_width=4, alpha=0.7, legend_label="Densidad",source=tabla1)
#p.line('cdf','x', line_color="orange", line_width=2, alpha=0.7, legend_label="Densidad_A",source=tabla1)

#p.xaxis.axis_label = 'frecuencias'
p.yaxis.axis_label = 'Años seleccionados'
p.title.align = 'center'
p.xaxis.major_label_orientation = np.pi/4

## Tab3

# plot 1
plot_ra=figure(plot_height=400,plot_width=450,title='Risky Wealth',
                        sizing_mode = "scale_width",
           toolbar_location="above",x_axis_type="datetime",y_axis_type="linear") 

plot_ra.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=riqueza_arriesgado,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
plot_ra.add_tools(HoverTool(tooltips=[('Fecha', '$x{%F}'),("Valor", "$y{0,0f}"),("Industria","@co")],
          formatters={'$x': 'datetime',
                      '@{y}' : 'printf',
                      '@co' : 'printf'}))

plot_ra.legend.location = "top_left"
plot_ra.xaxis.axis_label = 'Periodo'
plot_ra.yaxis.axis_label = 'Activo'
plot_ra.title.align = 'center'

# plot 2
plot_ss=figure(plot_height=400,plot_width=450,
                        sizing_mode = "scale_width",
           toolbar_location="above",x_axis_type="datetime",y_axis_type="linear") 

plot_ss.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=selector,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
plot_ss.add_tools(HoverTool(tooltips=[('Fecha', '$x{%F}'),("Valor", "$y{0,0f}"),("Industria","@co")],
          formatters={'$x': 'datetime',
                      '@{y}' : 'printf',
                      '@co' : 'printf'}))

plot_ss.legend.location = "top_left"
plot_ss.xaxis.axis_label = 'Periodo'
plot_ss.yaxis.axis_label = 'Activo'
plot_ss.title.align = 'center'

#plot 3

p3=figure(plot_height=100,plot_width=140,
                        sizing_mode = "scale_width",
           toolbar_location="below",x_axis_type="datetime",y_axis_type="linear") 

p3.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_dash='das',
              line_width=2, source=aht,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
p3.add_tools(HoverTool(tooltips=[('Fecha', '$x{%F}'),("Valor", "$y{0,0f}"),("Industria","@co")],
          formatters={'$x': 'datetime',
                      '@{y}' : 'printf',
                      '@co' : 'printf'}))

p3.legend.location = "top_left"
p3.xaxis.axis_label = 'Periodo'
p3.title.align = 'center'

# plot 4

p4=figure(plot_height=100,plot_width=140,
                        sizing_mode = "scale_width",
           toolbar_location="below",x_axis_type="datetime",y_axis_type="linear") 

p4.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_dash='das',
              line_width=2, source=vs,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
p4.add_tools(HoverTool(tooltips=[('Fecha', '$x{%F}'),("Valor", "$y{0,0f}"),("Industria","@co")],
          formatters={'$x': 'datetime',
                      '@{y}' : 'printf',
                      '@co' : 'printf'}))

p4.legend.location = "top_left"
p4.xaxis.axis_label = 'Periodo'
p4.title.align = 'center'

# tab 5
# plot1
plot5=figure(plot_height=450, width=500,title='',
                        sizing_mode = "scale_width",
           toolbar_location="above") 

plot5.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=tablas_put5,alpha=0.5,
                hover_line_alpha=1.0,hover_line_color='palet')




plot5.add_tools(HoverTool(tooltips=[('Valor acción', '$x{0,0.00f}'),("Anos", "$y{0,0.00f}")],
          formatters={'@{x}': 'printf',
                      '@{y}' : 'printf'}))

plot5.xaxis.axis_label = 'Valor de la acción'
plot5.yaxis.axis_label = 'Años seleccionados'
plot5.title.align = 'center'

# plot 2

p5 = figure(toolbar_location=None, width=500, height=450,
            y_range=plot.y_range, min_border=10, y_axis_location="right",x_axis_location="above",
            tooltips=[('freq','$x')])
p5.quad(top='right', bottom='left', right='freq',left=0, 
         color="white", line_color="#3A5785",source=tabla5,
          hover_fill_alpha = 1.0, hover_fill_color = 'navy',alpha=0.5)
p5.line('freq','x', line_color="#ff8888", line_width=4, alpha=0.7, legend_label="Densidad",source=tabla5)
#p.line('cdf','x', line_color="orange", line_width=2, alpha=0.7, legend_label="Densidad_A",source=tabla1)

#p.xaxis.axis_label = 'frecuencias'
p5.yaxis.axis_label = 'Años seleccionados'
p5.title.align = 'center'
p5.xaxis.major_label_orientation = np.pi/4

#--------------------------------------------------------------------------------------------------------
#                                          Funciones
#--------------------------------------------------------------------------------------------------------
## Tab1

def get_N_HexCol(N):
    HSV_tuples = [(x * 1.0 / N, 0.5, 0.5) for x in range(N)]
    hex_out = []
    for rgb in HSV_tuples:
        rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*rgb))
        hex_out.append('#%02x%02x%02x' % tuple(rgb))
    return hex_out

def carga():
    ##tabla de capitalizacion del mercado
     
    a=selectm_lab1.value
    fi=date_i.value
    ff=date_f.value
    mask = (ind_mktcap.index > fi) & (ind_mktcap.index <= ff)
    ind_datos=np.round(ind_mktcap.loc[mask])
    
    ind_mercado.data=dict(
        
    dias=[ind_datos.index.tolist() for i in ind_datos.columns],
    valores=[ind_datos[columnas] for columnas in ind_datos.columns],
    palet=get_N_HexCol(ind_datos.shape[1]),
    co=ind_datos.columns.tolist()
        )
    
    to_mktcap = np.round(pd.DataFrame(ind_datos.sum(axis="columns")),decimals=0)
    to_mktcap.columns=["Total_mercado"]
    
    ind_capweight = ind_datos.divide(total_mktcap,axis = "rows")
    ind_capw1 = ind_capweight[a]
    mask1 = (ind_capw1.index > fi) & (ind_capw1.index <= ff)
    ind_capw = ind_capw1.loc[mask1]
    total_market_return = (ind_capw*ind_returns[mask]).sum(axis="columns")
    total_market_index = pd.DataFrame(erk.drawdown(total_market_return).Wealth)
    total_market_return = pd.DataFrame(total_market_return)
    
    tabla_ind.data=dict(
    np.round(ind_returns,decimals=3))
    
    ind_total.data=dict(
        
    dias=[to_mktcap.index.tolist() for i in to_mktcap.columns],
    valores=[to_mktcap[columnas] for columnas in to_mktcap.columns],
    palet=["steelblue"],
    co=["Capitalización Total del Mercado"]
        )
    
    tabla_ind_weight.data=dict(
    np.round(ind_capw,decimals=3)
    )
     
    ind_weights.data=dict(
        
    dias=[ind_capw.index.tolist() for i in ind_capw.columns],
    valores=[(ind_capw)[columnas] for columnas in ind_capw.columns],
    palet=(Category20[20])[0:ind_capw.shape[1]],
    co=ind_capw.columns.tolist()
        )
    
    market_return.data=dict(
        
    dias=[total_market_return.index.tolist() for i in total_market_return.columns],
    valores=[total_market_return[columnas] for columnas in total_market_return.columns],
    palet=["blue"],
    co=["Retorno Total del mercado"])
    
    market_index.data=dict(
        
    dias=[total_market_index.index.tolist() for i in total_market_index.columns],
    valores=[total_market_index[columnas] for columnas in total_market_index.columns],
    palet=["purple"],
    co=["Indice total del mercado"])
## Tab2
def carga2():
    a=spinner2.value
    fi2=date_i2.value
    ff2=date_f2.value
    
    total_market_index = pd.DataFrame(erk.drawdown(total_market_return).Wealth)
    mask = (total_market_index.index > fi2) & (total_market_index.index <= ff2)
    
    total_market_index= total_market_index.loc[mask]
    retornosm=total_market_return[mask]
    total_market_index["medias moviles"]=np.round(total_market_index.rolling(window=a).mean())
    
    media_movil_total.data=dict(
    dias=[total_market_index.index.tolist() for i in total_market_index.columns],
    valores=[total_market_index[columnas] for columnas in total_market_index.columns],
    palet=["blue","orange"],
    co=["Indice total Mercado","Media movil a 36 dias"])
    
    tmi_tr36rets = pd.DataFrame(total_market_return.rolling(window=a).aggregate(erk.annualize_rets,periods_per_year=12))[mask]
    tmi_tr36rets["retornos"]=retornosm

    media_movil_retornos.data=dict(
    dias=[tmi_tr36rets.index.tolist() for i in tmi_tr36rets.columns],
    valores=[tmi_tr36rets[columnas] for columnas in tmi_tr36rets.columns],
    palet=["red","purple"],
    co=["Media movil a 36 dias","Retornos total del mercado",])
    
    ts_corr = ind_returns[mask].rolling(window=a).corr()
    ts_corr.index.names = ["date","industry"]
    ind_tr36corr = pd.DataFrame(ts_corr.groupby(level="date").apply(lambda cormat:cormat.values.mean() ))
    ind_tr36corr["tmi_tr36rets"]=pd.DataFrame(total_market_return.rolling(window=a).aggregate(erk.annualize_rets,periods_per_year=12))
    
    media_movil_correlaciones.data=dict(
    dias=[ind_tr36corr.index.tolist() for i in ind_tr36corr.columns],
    valores=[ind_tr36corr[columnas] for columnas in ind_tr36corr.columns],
    palet=["navy","darkred"],
    co=["Correlaciones","Retornos total del mercado",])

## Tab3
def carga3():
    a=selectm_lab3.value
    fi=date_i3.value
    ff=date_f3.value
    mask = (ind_return.index >= fi) & (ind_return.index <= ff)
    risr = ind_return[a]
    risky = risr.loc[mask]
    s1=start1.value
    s2=floor1.value
    s3=riskfree_ratio.value
    s0=m.value
    s4=selector31.value
    #run_cppi(risky_r, safe_r=None, m=3, start=1000, floor=0.8, riskfree_rate=0.03, drawdown=None)
    bb=erk.run_cppi(risky, safe_r=None, m=s0, start=s1, floor=s2, riskfree_rate=s3, drawdown=None)
    ra=bb["Risky Wealth"]
    ## 1er lista
    riqueza_arriesgado.data=dict(
    dias=[ra.index.tolist() for i in ra.columns],
    valores=[ra[columnas] for columnas in ra.columns],
    palet=(Category20[20])[0:ra.shape[1]],
    co=ra.columns.tolist())
    ss=bb[s4]
     ## 2er lista
    selector.data=dict(
    dias=[ss.index.tolist() for i in ss.columns],
    valores=[ss[columnas] for columnas in ss.columns],
    palet=(Category20[20])[0:ss.shape[1]],
    co=ss.columns.tolist())
    
    
def carga31():
    a=ind_returns.columns.tolist()
    fi=date_i3.value
    ff=date_f3.value
    mask = (ind_return.index >= fi) & (ind_return.index <= ff)
    risr = ind_return[a]
    risky = risr.loc[mask]
    s1=start1.value
    s2=floor1.value
    s3=riskfree_ratio.value
    s0=m.value
    
    #run_cppi(risky_r, safe_r=None, m=3, start=1000, floor=0.8, riskfree_rate=0.03, drawdown=None)
    bb=erk.run_cppi(risky, safe_r=None, m=s0, start=s1, floor=s2, riskfree_rate=s3, drawdown=None)

    sah=selector32.value
    svs=selector33.value
    #sss=selector34.value
   # scppi=selector35.value
    #sd=selector36.value
    ah=pd.DataFrame(bb["Wealth"][sah])
    ah["floor"]=pd.DataFrame(bb["floor"][sah])
    ah["Risky Wealth"]=pd.DataFrame(bb["Risky Wealth"][sah])
    
    # 1er grafico
    aht.data=dict(
    dias=[ah.index.tolist() for i in ah.columns],
    valores=[ah[columnas] for columnas in ah.columns],
    palet=(Category10[10])[0:ah.shape[1]],
    co=["Account History","Floor","Risky Wealth"],
    das=["dashed","dotdash","solid"])
    
    
    r=erk.run_cppi(tmi_return[mask])
    rw=pd.DataFrame(r["Wealth"])
    rw["Risky Wealth"]=pd.DataFrame(r["Risky Wealth"])
    rw.columns=["Wealth","Risky Wealth"]
    # 2do grafico
    vs.data=dict(
    dias=[rw.index.tolist() for i in rw.columns],
    valores=[rw[columnas] for columnas in rw.columns],
    palet=(Category10[10])[0:rw.shape[1]],
    co=["Account History","Risky Wealth"],
    das=["dashed","dotdash"])

## tab 4
def carga4():
    n_años=slider41.value
    n_escenarios=spinner42.value
    mu=slider43.value
    sigma=slider44.value
    vi_acciones=spinner43.value
    pasos=spinner44.value
    d=erk.gbm(n_años,n_escenarios,mu,sigma,vi_acciones,pasos)

   
    tablas_put.data=dict(
    dias=[d.index.tolist() for i in d.columns],
    valores=[d[columnas] for columnas in d.columns],
    palet=get_N_HexCol(d.shape[1]))
    mini=np.array(d).min()
    maxi=np.array(d).max()
    n=int(np.round(np.sqrt(d.shape[1])))

    arr_hist, edges = np.histogram(d, 
                                bins = n, 
                                range = [np.array(d).min(),np.array(d).max()],density=True)
   
    tabla1.data=dict(
        freq=arr_hist.tolist(),
        left=edges[:-1].tolist(),
        right=edges[1:].tolist(),
        x=np.linspace(mini, maxi, n).tolist(),
        cdf=np.cumsum(arr_hist).tolist()
        )
  
# tab5
def carga5():
    ne=spinner51.value
    muv=spinner52.value
    sigmav=spinner53.value
    d=erk.gbm(n_scenarios=ne,mu=muv,sigma=sigmav)
    
    
    tablas_put5.data=dict(
    dias=[d.index.tolist() for i in d.columns],
    valores=[d[columnas] for columnas in d.columns],
    palet=get_N_HexCol(d.shape[1]))
    
    mini=np.array(d).min()
    maxi=np.array(d).max()

    arr_hist, edges = np.histogram(d, 
                                bins = 14, 
                                range = [np.array(d).min(),np.array(d).max()],density=True)
   
    tabla5.data=dict(
        freq=arr_hist.tolist(),
        left=edges[:-1].tolist(),
        right=edges[1:].tolist(),
        x=np.linspace(mini, maxi, 14).tolist(),
        cdf=np.cumsum(arr_hist).tolist()
        )


    
    
    
#--------------------------------------------------------------------------------------------------------
#                                          Tablas de datos
#--------------------------------------------------------------------------------------------------------
## Tab1

boton_lab1.on_click(carga)
Cind=[TableColumn(field=Ci, title=Ci) for Ci in tabla_ind.data]
dind= DataTable(source=tabla_ind, columns=Cind, width=300, height=200, index_position=None)

Cind_w=[TableColumn(field=Ci, title=Ci) for Ci in tabla_ind_weight.data]
dind_w= DataTable(source=tabla_ind_weight, columns=Cind_w,editable=True, width=400, height=300, index_position=None)


## Tab2
boton_lab2.on_click(carga2)

## Tab3
boton_lab3.on_click(carga3)
boton_lab31.on_click(carga31)

## tab 4
boton_lab4.on_click(carga4)

## tab 5
boton_lab5.on_click(carga5)

#--------------------------------------------------------------------------------------------------------
#                                          Inputs
#--------------------------------------------------------------------------------------------------------

inputs1 = column(titulo_lab1,subtitulo_lab1,date_i,date_f,selectm_lab1,boton_lab1)
inputs2 = column(titulo_lab2,subtitulo_lab2,date_i2,date_f2,spinner2,boton_lab2)
inputs3 = column(titulo_lab3,subtitulo_lab3,date_i3,date_f3,selectm_lab3)
inputs30 = column(titulo_lab31,m,start1,floor1,riskfree_ratio,selector31,boton_lab3)
inputs31 = column(titulo_lab32,selector32,boton_lab31)
inputs32 = column(titulo_lab33,subtitulo_lab31,boton_lab31)
inputs33 = column(titulo_lab34,selector35,boton_lab31)
inputs34 = column(titulo_lab35,selector36,boton_lab31)
inputs4 = column(titulo_lab4,subtitulo_lab4,slider41,spinner42,titulo_lab41,slider43,slider44,spinner43,spinner44,boton_lab4)
inputs5 = column(titulo_lab5,subtitulo_lab5,spinner51,spinner52,spinner53,floor2,m1,spinner54,spinner55,boton_lab5)
#inputs6 = column(titulo_lab6,subtitulo_lab6)
layout1=gridplot([[inputs1,plot_mercado,plot_total],[titulo_lab11],[dind_w,plot_weights,plot_market_r],[None,plot_index]])
layout2=gridplot([[inputs2,plot_media,plot_media_r],[None,plot_media_c]])
layout3=gridplot([[inputs3,inputs30,plot_ra,plot_ss],[inputs31,inputs32,inputs33,inputs34],[p3,p4]])
layout4=gridplot([[inputs4,plot,p]])

layout5=gridplot([[inputs5,plot5,p5]])
#layout6=gridplot([[inputs6]])
tab1 = Panel(child=layout1,title="Laboratorio 12")
tab2 = Panel(child=layout2,title="Laboratorio 13")
tab3 = Panel(child=layout3,title="Laboratorio 14 y 15")
tab4 = Panel(child=layout4,title="Laboratorio 16")
tab5 = Panel(child=layout5,title="Laboratorio 17 y 18")
#tab6 = Panel(child=layout6,title="Laboratorio 12")

tabs = Tabs(tabs=[tab1,tab2,tab3,tab4,tab5])
curdoc().add_root(tabs)
curdoc().title = "Grafico de escenario"

