#!/usr/bin/env python
# coding: utf-8

# In[1]:


from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual, Layout
import ipywidgets as widgets
import numpy as np
import pandas as pd
import geopandas as gpd
import folium
from folium import plugins
import ipywidgets
import geocoder
import geopy
from vega_datasets import data as vds
import plotly.express as px
import voila


# In[2]:


df = pd.read_excel('/Users/vadimvorobyev/Documents/map_portfolio/tmp.xlsx')


# In[3]:


df.head(10)


# In[16]:


list(df['КП'].unique())


# In[4]:


originality = widgets.SelectMultiple(
    options = list(df['ЗаКем'].unique()),
    value = list(df['ЗаКем'].unique()),
    description='ЗаКем',
    disabled=False,
    rows=len(pd.unique(df['ЗаКем']))
)


# In[5]:


worker = widgets.SelectMultiple(
    options = list(df['Сотрудник'].unique()),
    value = list(df['Сотрудник'].unique()),
    description='Сотрудник',
    disabled=False,
    rows=len(pd.unique(df['Сотрудник']))
)


# In[6]:


op = widgets.SelectionRangeSlider(
    options=df['СрокПЗ'],
    description='Срок просроченной задолженности, дни',
    disabled=False,
    style={'background-color': '#000'}
)


# In[7]:


oa = widgets.SelectionRangeSlider(
    options=df['КП'],
    description='Размер кредитного портфеля, рубли',
    disabled=False,
    style={'background-color': '#000'}
)


# In[8]:


def generate_color(kp):
    if kp <= 10:
        c_outline, c_fill = '#FFC0CB', '#FFC0CB'
        m_opacity, f_opacity = 1, 1
    else:
        c_outline, c_fill = '#c0392b', '#e74c3c'
        m_opacity, f_opacity = 1, 1
    return c_outline, c_fill, m_opacity, f_opacity


# In[9]:


def generate_popup(КД, ФИО):
    return f'''<strong>Номер КД:</strong> {КД}<br><strong>ФИО:</strong> {ФИО}'''


# In[10]:


def change_parameters(originality, worker, op, oa):

    low_op = op[0]
    high_op = op[1]
    
    low_oa = oa[0]
    high_oa = oa[1]
    
    df_update = df[df['ЗаКем'].isin(originality)]
    df_update1 = df_update[df_update['Сотрудник'].isin(worker)]
    df_update2 = df_update1[df_update1['СрокПЗ'].between(low_op,high_op)]
    df_update3 = df_update2[df_update2['КП'].between(low_oa,high_oa)]
    
    m_tmp = folium.Map(location=[63.391522, 96.328125], zoom_start=3,  control_scale = True)
  
    for _, row in df_update3.iterrows():
        c_outline, c_fill, m_opacity, f_opacity = generate_color(row['КП'])
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            popup=generate_popup(row['КД'], row['ФИО']),
            color=c_outline,
            fill=True,
            fillColor=c_fill,
            opacity=m_opacity,
            fillOpacity=f_opacity,
            radius=0.1
        ).add_to(m_tmp)
    display(m_tmp)


# In[11]:


out = widgets.interactive_output(
        change_parameters, 
          {'originality': originality,
           'worker': worker, 
           'op': op, 
           'oa': oa
          }
      )
ui = widgets.HBox(
        [originality, 
         worker,
          op, 
          oa
        ], 
        layout=Layout(display='flex', flex_flow='row wrap', justify_content='space-between')
    )


# In[12]:


display(ui, out)


# In[ ]:




