# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 08:48:49 2021

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
from bokeh.models import  (BoxSelectTool, Circle, Column, ColumnDataSource,ranges, PreText,Legend,
                          DataTable, Grid, HoverTool, IntEditor, LinearAxis, DateRangeSlider,Div,
                          NumberEditor, NumberFormatter, Plot, SelectEditor,Button,CheckboxGroup, FactorRange,
                          StringEditor, StringFormatter,Spinner, TableColumn,CustomJS, Select,LassoSelectTool, 
                          Panel, RadioGroup, Tabs,DatePicker,MultiSelect, RangeSlider,TextInput, Slider)
from bokeh.transform import factor_cmap
from bokeh.plotting import figure
from csv import reader
from datetime import datetime,timedelta,date
from scipy import stats
from scipy.stats import chisquare

#--------------------------------------------------------------------------------------------------------
#                                           Datos
#--------------------------------------------------------------------------------------------------------

prices1 = pd.read_csv('C:/Users/Hp/Documents/FINAC/data/sample_prices.csv')
prices1.columns=["Blue","Orange"]
returns = prices1.pct_change()
returns = returns.dropna()

## segunda base da datos
returns1 = pd.read_csv('C:/Users/Hp/Documents/FINAC/data/Portfolios_Formed_on_ME_monthly_EW.csv',
                       header=0,index_col=0,parse_dates=True,na_values=-99.99)
returns1.index = pd.to_datetime(returns1.index,format="%Y%m")


#returns1.index = returns1.index.to_period("M")
columns = ["Lo 10", "Hi 10"]
returns1 = returns1[columns]
returns1 = returns1/100
returns1.columns =['SmallCap','LargeCap']
## se divide por 100 por que los retornos estan en porcentajes
returns1 = returns1/100
returns1.columns =['SmallCap','LargeCap']
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

columnas1=returns1.columns.tolist()
columnas1.append("Todos")
### Desviación de la normalidad

hfi = erk.get_hfi_returns()
columnass=hfi.columns.tolist()
columnass.append("Todos")
var_list = [erk.var_gaussian(hfi),erk.var_gaussian(hfi,modified=True),erk.var_historic(hfi)]
comparacion = pd.concat(var_list, axis =1)
comparacion.columns= ["Gausiana","Cornish-Fisher","Historic"]

#--------------------------------------------------------------------------------------------------------
#                                          Widgets
#--------------------------------------------------------------------------------------------------------

## tab 1
titulo_tabla_strikes = Div(text="<b>Strikes </b>",
               style={'font-size': '150%', 'color': 'blue',
                      'text-align': 'center'})

text = TextInput(title="Base de datos",value="Serie de tiempo de 2 acciones",width=300)
text2 = TextInput(title="Retornos",value="Calculo de los retornos para cada accion",width=300)
boton=Button(label="enter",button_type ='primary',width=300)
pre = PreText(text="""Conceptos Básicos de retornos.
                         
En esta sección se introduce el calculo de los 

retornos, su anualización y visualización""",
width=100, height=100)

## Tab 2

a1 = PreText(text="""Riesgo ajustado de los retornos.
                         
Esta sección contiene el calculo de la volatilidad 

de los retornos, su respectiva anulización y 

calculo del Sharpe Ratio""",
width=200, height=200)
text3 = TextInput(title="Base de datos",value="Volatilidad de Portafolio",width=300)
boton2=Button(label="enter",button_type ='primary',width=300)


## Tab 3

selector = Select(title="Serie de tiempo", value='SmallCap',
               options=columnas1)

date_i = DatePicker(title='Seleccione fecha inicial', value="1926-07", min_date="1926-07", max_date="2018-12")
date_f = DatePicker(title='Seleccione fecha final',  value="2018-12", min_date="1926-07", max_date="2018-12")
boton3=Button(label="enter",button_type ='primary',width=300)

## tab 4 y 5

selector2 = Select(title="Serie de tiempo", value='Convertible Arbitrage',
               options=columnass)

date_i2 = DatePicker(title='Seleccione fecha inicial', value="1997-01", min_date="1997-01", max_date="2018-11")
date_f2 = DatePicker(title='Seleccione fecha final',  value="2018-11", min_date="1997-01", max_date="2018-11")
boton4=Button(label="enter",button_type ='primary',width=300)
spinner = Spinner(title="Seleccione nivel de significancia", low=0.01, high=0.1, step=0.01, value=0.05)


## tab 6
date_i3 = DatePicker(title='Seleccione fecha inicial', value="1997-01", min_date="1997-01", max_date="2018-11")
date_f3 = DatePicker(title='Seleccione fecha final',  value="2018-11", min_date="1997-01", max_date="2018-11")
boton6=Button(label="enter",button_type ='primary',width=300)
#--------------------------------------------------------------------------------------------------------
#                                          Tablas 
#--------------------------------------------------------------------------------------------------------

## Tab 1
precios=ColumnDataSource(data=dict(
      prices1
    ))

retornos=ColumnDataSource(data=dict(
    returns
    ))

estadisticas=ColumnDataSource(data=dict(
    Medidas=[],
    Blue=[],
    Orange=[]))

estadisticas1=ColumnDataSource(data=dict(
    Medidas=[],
    Blue=[],
    Orange=[]))

precios1=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[]))

prep=ColumnDataSource(data=dict(
    azules=[],
    naranjas=[]))


re=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[]))

rep=ColumnDataSource(data=dict(
    azules=[],
    naranjas=[],
    dias=[]))


## tab 2
retornos1=ColumnDataSource(data=dict(
    returns1
    ))

retornos2=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[]))

retornos3=ColumnDataSource(data=dict(
    Medidas=[],
    SmallCap=[],
    LargeCap=[]))

## tab 3

retornos4=ColumnDataSource(data=dict(
    erk.drawdown(returns1["SmallCap"])
    ))

retornos5=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[]))

retornos6=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[]))

retornos7=ColumnDataSource(data=dict(
    Medidas=[],
    Valor=[],
    Periodo=[]))

retornos8=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[]))

# tab 4 y 5

retornos9=ColumnDataSource(data=dict(
    dias=[],
    valores=[],
    palet=[],
    co=[]))

retornos10=ColumnDataSource(data=dict(
Serie=[],
Media=[],
Mediana=[],
Simetria=[]
))

retornos11=ColumnDataSource(data=dict(
    freq=[],
    left=[],
    right=[],
    x=[],
    cdf=[]
    ))

retornos12=ColumnDataSource(data=dict(
    Serie=[],
    Asimetria=[],
    Curtosis=[],
    Normalidad=[]
    ))

retornos13=ColumnDataSource(data=dict(
    Serie=[],
    Gausiano=[],
    Cornish=[],
    Historico=[]
    ))



#--------------------------------------------------------------------------------------------------------
#                                          Plots
#--------------------------------------------------------------------------------------------------------
def get_N_HexCol(N):
    HSV_tuples = [(x * 1.0 / N, 0.5, 0.5) for x in range(N)]
    hex_out = []
    for rgb in HSV_tuples:
        rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*rgb))
        hex_out.append('#%02x%02x%02x' % tuple(rgb))
    return hex_out



plot=figure(plot_height=300,plot_width=450,title='',
                    tooltips=[('dias','$x'),('valores','$y')],
                        sizing_mode = "scale_width",
           toolbar_location="above") 

plot.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=precios1,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
plot.add_tools(HoverTool(show_arrow=False,
                      line_policy='nearest',
                      tooltips=None))

plot.xaxis.axis_label = 'dias'
plot.yaxis.axis_label = 'valor estimado'
plot.title.align = 'center'


p2 = figure(plot_height=300,plot_width=450,title='',
                    tooltips=[('dias','$x'),('valor accion','$y')],
                        sizing_mode = "scale_width",
           toolbar_location="above")

p2.vbar(x=dodge('dias',0.0), top='azules', width=0.3, source=prep,
       color="blue", legend_label="Blue")
p2.vbar(x=dodge('dias', 0.35), top='naranjas', width=0.3, source=prep,
       color="orange", legend_label="Orange")

p2.add_tools(HoverTool(show_arrow=True,
                      line_policy='nearest',
                      tooltips=None))


p2.xaxis.axis_label = 'dias'
p2.title.align = 'center'
p2.legend.location = "top_right"
p2.legend.orientation = "vertical"

plot1=figure(plot_height=300,plot_width=450,title='',
                    tooltips=[('dias','$x'),('valores','$y')],
                        sizing_mode = "scale_width",
           toolbar_location="above") 

plot1.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=re,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
plot1.add_tools(HoverTool(show_arrow=False,
                      line_policy='nearest',
                      tooltips=None))

plot1.xaxis.axis_label = 'dias'
plot1.yaxis.axis_label = 'valor retorno'
plot1.title.align = 'center'


p1 = figure(plot_height=300,plot_width=450,title='',
                    tooltips=[('dias','$x'),('valor','$y')],
                        sizing_mode = "scale_width",
           toolbar_location="above")

p1.vbar(x=dodge('dias',0.0), top='azules', width=0.3, source=rep,
       color="blue", legend_label="Blue")
p1.vbar(x=dodge('dias', 0.35), top='naranjas', width=0.3, source=rep,
       color="orange", legend_label="Orange")

p1.add_tools(HoverTool(show_arrow=True,
                      line_policy='nearest',
                      tooltips=None))


p1.xaxis.axis_label = 'dias'
p1.title.align = 'center'
p1.legend.location = "top_right"
p1.legend.orientation = "vertical"


### Tab 2
p=figure(plot_height=400,plot_width=550,title='',
                    tooltips=[('año','$x'),('retorno','$y')],
                        sizing_mode = "scale_width",
           toolbar_location="above",x_axis_type="datetime") 


p.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=retornos2,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
p.add_tools(HoverTool(show_arrow=True,
                      line_policy='nearest',
                      tooltips=None))

p.xaxis.axis_label = 'años'
p.yaxis.axis_label = 'retorno'
p.title.align = 'center'

## tab 3

p3=figure(plot_height=300,plot_width=450,title='',
                    tooltips=[('Fecha','$x'),("valor","$y")],
                        sizing_mode = "scale_width",
           toolbar_location="above",x_axis_type="datetime") 


p3.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=retornos5,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
p3.add_tools(HoverTool(show_arrow=True,
                      line_policy='next',
                      tooltips=None))


p3.legend.location = "bottom_right"
p3.yaxis.axis_label = 'retorno'
p3.title.align = 'center'

p4=figure(plot_height=300,plot_width=450,title='',
                    tooltips=[('Año','$x'),('Valor','$y')],
                        sizing_mode = "scale_width",
           toolbar_location="above",x_axis_type="datetime") 


p4.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=retornos6,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
p4.add_tools(HoverTool(show_arrow=True,
                      line_policy='next',
                      tooltips=None))

p4.xaxis.axis_label = 'años'
p4.legend.location = "bottom_right"
p4.yaxis.axis_label = 'Reducción Máxima'
p4.title.align = 'center'

p5=figure(plot_height=400,plot_width=550,title='',
                    tooltips=[('año','$x'),('retorno','$y')],
                        sizing_mode = "scale_width",
           toolbar_location="above",x_axis_type="datetime") 


p5.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=retornos8,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
p5.add_tools(HoverTool(show_arrow=True,
                      line_policy='nearest',
                      tooltips=None))

p5.xaxis.axis_label = 'años'
p5.yaxis.axis_label = 'retorno'
p5.title.align = 'center'


# tab 4 y 5

p6=figure(plot_height=300,plot_width=450,title='',
                    tooltips=[('año','$x'),('retorno','$y')],
                        sizing_mode = "scale_width",
           toolbar_location="above",x_axis_type="datetime") 


p6.multi_line(xs='dias',
              ys='valores',
              line_color='palet',
              line_width=2, source=retornos9,alpha=0.5,
              hover_line_alpha=1.0,legend_field='co')
p6.add_tools(HoverTool(show_arrow=True,
                      line_policy='nearest',
                      tooltips=None))

p6.xaxis.axis_label = 'años'
p6.yaxis.axis_label = 'retorno'
p6.title.align = 'center'

p7 = figure(toolbar_location=None, width=450, height=300, min_border=10,
            tooltips=[('freq','$x')])
p7.quad(top='freq', bottom=0, right='left',left="right", 
         color="white", line_color="navy",source=retornos11,alpha=0.5)
p7.line('x','freq', line_color="#ff8888", line_width=4, alpha=0.7, legend_label="PDF",source=retornos11)
p7.line('x','cdf', line_color="orange", line_width=2, alpha=0.7, legend_label="CDF",source=retornos11)

p7.legend.location = "center_right"
p7.legend.background_fill_color = "#fefefe"
p7.xaxis.axis_label = 'Valor serie'
p7.yaxis.axis_label = 'Frecuencia'

# tab 6

  
#--------------------------------------------------------------------------------------------------------
#                                          Funciones
#--------------------------------------------------------------------------------------------------------

def upload():
    
    ## tab 1
    precios.data=dict(
    prices1)
    
    retornos.data=dict(
    np.round(returns,decimals=3))
    
    t1=np.round(prices1.mean(),decimals=3).tolist()
    t2=np.round(prices1.std(),decimals=3).tolist()
    
    tes1=np.round(returns.mean(),decimals=3).tolist()
    tes2=np.round(returns.std(),decimals=3).tolist()
    tes3=np.round(((((returns - returns.mean())**2).sum())/(returns.shape[0]-1))**0.5,decimals=3).tolist()
    tes4=np.round(returns.std()*np.sqrt(12),decimals=3).tolist()
    
    estadisticas.data=dict(
        Medidas=["Media","Desviación"],
        Blue=[t1[0],t2[0]],
        Orange=[t1[1],t2[1]])
    
    estadisticas1.data=dict(
        Medidas=["Media","Desviación","Volatilidad","Anualización"],
        Blue=[tes1[0],tes2[0],tes3[0],tes4[0]],
        Orange=[tes1[1],tes2[1],tes3[1],tes4[1]])
    
    blue=[]
    orange=[]
    for i in range(0,prices1.shape[0]):
        blue.append("Blue")
    for i in range(0,prices1.shape[0]):
        orange.append("Orange")
    

    precios1.data=dict(
    dias=[prices1.index.tolist() for i in prices1.columns],
    valores=[prices1[columnas] for columnas in prices1.columns],
    palet=["blue","orange"],
    co=prices1.columns.tolist())
    
    prep.data=dict(
    azules=np.round(prices1["Blue"],decimals=3).tolist(),
    naranjas=np.round(prices1["Orange"],decimals=3).tolist(),
    dias=prices1.index.tolist())
    
    re.data=dict(
    dias=[returns.index.tolist() for i in returns.columns],
    valores=np.round([returns[columnas] for columnas in returns.columns],decimals=3).tolist(),
    palet=["blue","orange"],
    co=returns.columns.tolist())
    
    rep.data=dict(
    azules=np.round(returns["Blue"],decimals=3).tolist(),
    naranjas=np.round(returns["Orange"],decimals=3).tolist(),
    dias=returns.index.tolist())
    
def upload2():
    
    ## tab 2
    retornos1.data=dict(
    np.round(returns1,decimals=6))
    
    retornos2.data=dict(
    dias=[returns1.index.tolist() for i in returns1.columns],
    valores=[returns1[columnas] for columnas in returns1.columns],
    palet=["blue","purple"],
    co=returns1.columns.tolist())
    

    v=np.round(returns1.std(),decimals=5).tolist()
    va=np.around(returns1.std()*np.sqrt(12),decimals=5).tolist()
    rm=np.round((returns1+1).prod()**(1/returns1.shape[0])-1,decimals=5).tolist()
    ra=np.round((returns1+1).prod()**(12/returns1.shape[0])-1,decimals=5).tolist()
    er=np.round(annualized_return -riskfree_rate,decimals=5).tolist()
    sr=np.round(excess_return/annualized_vol,decimals=5).tolist()
    
    retornos3.data=dict(
        Medidas=["Volatilidad","Volatilidad_Anualizada","Retornos_Mensuales","Retornos_Anualizados","Excess_return","Sharpe_Ratio"],
        SmallCap=[v[0],va[0],rm[0],ra[0],er[0],sr[0]],
        LargeCap=[v[1],va[1],rm[1],ra[1],er[1],sr[1]]
     )
    
def upload3(): 
    a=selector.value
    ri=np.round(erk.drawdown(returns1[a]),decimals=4)
    rr=pd.DataFrame(np.round(returns1[a],decimals=4))
    fi=date_i.value
    ff=date_f.value
    mask = (ri.index > fi) & (ri.index <= ff)
    mask1 =(rr.index > fi) & (rr.index <= ff)
    rr=rr.loc[mask1]
    ri=ri.loc[mask]
    retornos4.data=dict(
      ri
        )
    ri1=ri.iloc[:,0:2]
    ri2=pd.DataFrame(ri.iloc[:,2])


    retornos5.data=dict(
    dias=[ri1.index.tolist() for i in ri1.columns],
    valores=[ri1[columnas] for columnas in ri1.columns],
    palet=["blue","green"],
    co=ri1.columns.tolist()
        )
    
    ri2.index =pd.to_datetime(ri2.index,format="%Y%m%d")
    retornos6.data=dict(
    dias=[ri2.index.tolist() for i in ri2.columns],
    valores=[ri2[columnas] for columnas in ri2.columns],
    palet=["red"],
    co=ri2.columns.tolist()
        )
    
    ri2=pd.DataFrame(ri.iloc[:,2])
    ri2.index =pd.to_datetime(ri2.index,format="%Y%m").strftime('%Y-%m-%d')
    retornos7.data=dict(
    Medidas=["Minimo","Maximo"],
    Valor=[ri2.min()[0],ri2.max()[0]],
    Periodo=[ri2.idxmin()[0],ri2.idxmax()[0]] 
    )
    
    retornos8.data=dict(
    dias=[rr.index.tolist() for i in rr.columns],
    valores=[rr[columnas] for columnas in rr.columns],
    palet=["purple"],
    co=rr.columns.tolist())
    
def upload4():
    a=selector2.value
    sr=pd.DataFrame(np.round(hfi[a],decimals=4))
    fi=date_i2.value
    ff=date_f2.value
    mask = (sr.index > fi) & (sr.index <= ff)
    sr=sr.loc[mask]
    
    retornos9.data=dict(
    dias=[sr.index.tolist() for i in sr.columns],
    valores=[sr[columnas] for columnas in sr.columns],
    palet=["purple"],
    co=sr.columns.tolist())
    
    mask1 = (hfi.index > fi) & (hfi.index <= ff)
    me=hfi.loc[mask1]
    me=np.round(pd.concat([me.mean(),me.median(),me.mean()>me.median()],axis="columns"),decimals=4)
   
    retornos10.data=dict(
        Serie=hfi.columns.tolist(),
        Media=me.iloc[:,0].tolist(),
        Mediana=me.iloc[:,1].tolist(),
        Simetria=me.iloc[:,2].tolist()
        )
    mini=np.array(sr).min()
    maxi=np.array(sr).max()
    nbin=int(np.around(np.sqrt(sr.shape[0]), decimals=0))

    arr_hist, edges = np.histogram(sr, 
                                bins = nbin, 
                               range = [np.array(sr).min(),np.array(sr).max()])
    
    mu,sigma=sr.mean()[0],sr.std()[0]
    x=np.linspace(mini, maxi,len(edges)-1)
    
    retornos11.data=dict(
        freq=arr_hist.tolist(),
        left=edges[:-1].tolist(),
        right=edges[1:].tolist(),
        x=np.linspace(mini, maxi, nbin).tolist(),
        cdf= (1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))).tolist()
        )
    ns=spinner.value
    var_list=[erk.skewness(hfi),erk.kurtosis(hfi), erk.is_normal(hfi,ns)]
    comparacion = pd.concat(var_list, axis =1)
    
    retornos12.data=dict(
    Serie=hfi.columns.tolist(),
    Asimetria=np.round(comparacion.iloc[:,0],decimals=4).tolist(),
    Curtosis=np.round(comparacion.iloc[:,1],decimals=4).tolist(),
    Normalidad=comparacion.iloc[:,2].tolist()
    )
    
def upload6():
    fi=date_i3.value
    ff=date_f3.value
    mask = (hfi.index > fi) & (hfi.index <= ff)
    sr=hfi.loc[mask]
    var_list = [erk.var_gaussian(sr),erk.var_gaussian(sr,modified=True),erk.var_historic(sr)]
    comparacion = pd.concat(var_list, axis =1)
    comparacion.columns= ["Gausiana","Cornish-Fisher","Historic"]
    
    retornos13.data=dict(
    Serie=sr.columns.tolist(),
    Gausiano=np.round(comparacion.iloc[:,0],decimals=4).tolist(),
    Cornish=np.round(comparacion.iloc[:,1],decimals=4).tolist(),
    Historico=np.round(comparacion.iloc[:,2],decimals=4).tolist()
        )
    
    
    
    

## tab 1
boton.on_click(upload)
Cp=[TableColumn(field=Ci, title=Ci) for Ci in precios.data]
dp= DataTable(source=precios, columns=Cp, width=300, height=200, index_position=None)

Cr=[TableColumn(field=Ci, title=Ci) for Ci in retornos.data]
dr= DataTable(source=retornos, columns=Cr, width=300, height=200, index_position=None)

Ce=[TableColumn(field=Ci, title=Ci) for Ci in estadisticas.data]
de= DataTable(source=estadisticas, columns=Ce, width=300, height=200, index_position=None)

Ce1=[TableColumn(field=Ci, title=Ci) for Ci in estadisticas1.data]
de1= DataTable(source=estadisticas1, columns=Ce1, width=300, height=200, index_position=None)

# tab 2
boton2.on_click(upload2)
Cr2=[TableColumn(field=Ci, title=Ci) for Ci in retornos1.data]
dr2= DataTable(source=retornos1, columns=Cr2, width=300, height=400, index_position=None)

Cr3=[TableColumn(field=Ci, title=Ci) for Ci in retornos3.data]
dr3= DataTable(source=retornos3, columns=Cr3, width=300, height=400, index_position=None)

# tab 3
boton3.on_click(upload3)
Cr4=[TableColumn(field=Ci, title=Ci) for Ci in retornos4.data]
dr4= DataTable(source=retornos4, columns=Cr4, width=400, height=300, index_position=None)

Cr5=[TableColumn(field=Ci, title=Ci) for Ci in retornos7.data]
dr5= DataTable(source=retornos7, columns=Cr5, width=400, height=300, index_position=None)

# tab 4 y 5
boton4.on_click(upload4)
Cr6=[TableColumn(field=Ci, title=Ci) for Ci in retornos10.data]
dr6= DataTable(source=retornos10, columns=Cr6, width=450, height=250, index_position=None)

Cr7=[TableColumn(field=Ci, title=Ci) for Ci in retornos12.data]
dr7= DataTable(source=retornos12, columns=Cr7, width=400, height=250, index_position=None)

# tab 6

boton6.on_click(upload6)
Cr8=[TableColumn(field=Ci, title=Ci) for Ci in retornos13.data]
dr8= DataTable(source=retornos13, columns=Cr8, width=450, height=250, index_position=None)

inputs = column(selector,date_i,date_f,boton3)
inputs1 = column(selector2,date_i2,date_f2,spinner,boton4)
inputs2 = column(date_i3,date_f3,boton6)
layout1=gridplot([[pre,None,None,None],[text,None,None,None],[dp,plot,p2,de],[text2,None,None,None],[dr,plot1,p1,de1],[boton,None,None,None]])
layout2=gridplot([[a1,None,None],[text2,None,None],[dr2,p,dr3],[boton2,None,None]])
layout3=gridplot([[inputs,p3,dr4],[None,p4,dr5],[None,p5,None]])
layout4=gridplot([[inputs1,p6,dr6],[None,p7,dr7],[None,]])
layout6=gridplot([[inputs2,dr8]])
tab1 = Panel(child=layout1,title="Laboratorio 1")
tab2 = Panel(child=layout2,title="Laboratorio 2")
tab3 = Panel(child=layout3,title="Laboratorio 3")
tab4 = Panel(child=layout4,title="Laboratorio 4 y 5")
tab6 = Panel(child=layout6,title="Laboratorio 6")
tabs = Tabs(tabs=[tab1,tab2,tab3,tab4,tab6])
curdoc().add_root(tabs)
curdoc().title = "Grafico de escenario"