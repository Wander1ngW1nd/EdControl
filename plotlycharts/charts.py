# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 16:12:00 2023

@author: PC
"""

import plotly.express as px
import pandas as pd
#import streamlit as st

def radio_chart():

    df = pd.DataFrame(dict(
        r=[1, 5, 2, 2, 3],
        theta=['processing cost','mechanical properties','chemical stability',
           'thermal stability', 'device integration']))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.update_layout(
    autosize=False,
    width=400,
    height=300,
    paper_bgcolor="DarkBlue"
)
    return fig

def pie_chart():
    pass
