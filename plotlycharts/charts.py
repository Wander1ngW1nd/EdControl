# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 16:12:00 2023

@author: PC
"""

import plotly.express as px
import pandas as pd
 

def radio_chart():
    
    fig = px.line_polar( 
                        r = [1, 2, 3, 4, 5, 6],
                        theta = ["Злость", "Отвращение","Страх",\
                                 "Счастье","Грусть","Удивление"], 
                        line_close=True,    
                        color_discrete_sequence=px.colors.sequential.Plasma_r,
                        template="plotly_dark")
    fig.update_layout(
                        autosize=False,
                        width=400,
                        height=300,
                        paper_bgcolor="Black")
    

    return fig

def bar_chart():
    
    df = pd.DataFrame(dict(
        x=[1, 5, 2, 2, 3, 2],
        y=['processing cost','mechanical properties','chemical stability',
           'thermal stability', 'device integration','add emotion']))
    fig = px.bar(df, x = "x", y ='y', barmode = 'group', labels={'x': '', 'y':''}, width=500, height=300)
    #fig.update_layout(showlegend=False)
    fig.update_traces(marker_color = ['#f5800d','#f2ce4d','#047e79','#a69565','#cfc1af','#574c31'], marker_line_color = 'black',
                  marker_line_width = 2, opacity = 1)
    return fig

