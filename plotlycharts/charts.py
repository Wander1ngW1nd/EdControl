# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 16:12:00 2023

@author: PC
"""

import plotly.express as px

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

def pie_chart():
    pass

