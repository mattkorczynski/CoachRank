import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
from dash import Dash, html, dcc, Input, Output, dash_table, State, ctx
import plotly.express as px
import pandas as pd
import time
import dash
import dash_html_components as html
import dash_core_components as dcc
import os
from os import walk
import sys
import dash_bootstrap_components as dbc
import dash_loading_spinners as dls
from dash.exceptions import PreventUpdate

import libs.tab_styles as tabs
from datetime import date, datetime
import random
from pandas import Timestamp
from math import modf
import dash_auth as auth
import base64
import io
import dash_uploader as du


import unittest


# Password pairs defined by external library

app = Dash(__name__)
app.title="Coach rank ESA PL"


#==================== CONSTANTS ==========================================

COLORS = [
  '#3B8EA5', # Blue Munsell
  '#F5EE9E', # Green Yellow Crayola
  '#F49E4C', # Sandy Brown
  '#AB3428', # Sweet Brown
  '#F71735', # Imperial Red
  '#99C24D'  # Android Green
  ]

BACKGROUND = '#2E2E2E'
#================    HTML STRUCTURE   ====================================
app.layout = html.Div(   
  children=[
    html.Div(
      id="div-loading",
      children=[
        dls.Hash(
          fullscreen=True, 
          id="loading-whole-app"
            )
        ]
      ),
    html.Div(
      className = "div-app", 
      id = "div-app", 
      style={'backgroundColor': '#2E2E2E'}, 
      children=[
      dcc.Tabs([
        dcc.Tab(
          label = 'Coach rank', 
          style = tabs.tab_style, 
          selected_style=tabs.tab_selected_style, 
          children = [
          html.Div([
            html.H1('Coach rank - Poland'),
            # dash_table.DataTable(
            #   df_machines_analysis.to_dict('records'), 
            #   [{"name": i, "id": i} for i in df_machines_analysis.columns], 
            #   id='tbl', 
            #   page_action='none',
            #   style_table={
            #     'height':'700px',
            #     'width':'900px', 
            #     'font':"Hemi Head Rg", 
            #     'position': 'relative', 
            #     'left':50,
            #     'top':30},
            #   style_cell={
            #     'text-align':'center', 
            #     'minWidth': '90px', 
            #     'width': '180px', 
            #     'maxWidth': '180px'},
            #   style_data={
            #     'font-family':'Segoe, sans-serif', 
            #     'color':'white', 
            #     'background-color':'#2e2e2e', 
            #     'fontSize':12, 
            #     'border':'rgb(46,46,46)'},
            #   style_header={
            #           'font-family':'Hemi Head Rg',
            #           'background-color': COLORS[0],
            #           'fontSize':12,
            #           'color':'white'},
            #   style_data_conditional=[
            #     {'if':{'filter_query':'{Typ}="E"'}, 'backgroundColor':'#006600'},
            #     {'if': {'column_id': 'Nr'}, 'width': '10%'}, 
            #     {'if': {'column_id': 'Typ'}, 'width': '10%'},
            #     ]    
            #   )
            ], className="six columns"),
                ]),
        dcc.Tab(
          label='Informacje ogólne', 
          style = tabs.tab_style, 
          id = "Zakladka_ogolne", 
          selected_style=tabs.tab_selected_style, 
          disabled_style=tabs.tab_disabled_style,
          disabled = True, 
          children=[
          html.Div([    
            html.Div([
              html.Div(id='Machine_header'),
              dash_table.DataTable(
                id = 'tablica_danych',
                page_size=1000, 
                style_table={
                  'height':'70px', 
                  'overflowY':'auto', 
                  'font':"Hemi Head Rg"},
                style_cell={'text-align':'center'},
                style_data={
                  'font-family':'Segoe, sans-serif', 
                  'color':'white', 
                  'background-color':'#2e2e2e', 
                  'fontSize':12, 
                  'border':'rgb(46,46,46)'},
                style_header={
                  'font-family':'Hemi Head Rg',
                  'background-color': COLORS[0],
                  'color':'white'}
                )
              #html.Img(src=app.get_asset_url('PM_R.png'))
              ]),
              html.Div([
                  dls.Hash(
                    dcc.Graph(
                      id='czas_pracy_graph', 
                      style={
                        'vertical-align': 'top', 
                        'margin-left': '2vw', 
                        'margin-top': '2vw', 
                        'margin-right':'2vw', 
                        'width' :'1700px'}
                      ), 
                      color="white", 
                      speed_multiplier = 2,
                      size = 100,)
              ]),
              html.H1('Dostępne dane dzienne'),
              html.Div([
                dls.Hash(
                  dash_table.DataTable(id = 'tablica_dostepnych_dni',
                    page_size=1000, 
                    style_table={
                      'height':'1400px', 
                      'overflowY':'auto', 
                      'font':"Hemi Head Rg"},
                    style_cell={'text-align':'center'},
                    style_data={
                      'font-family':'Segoe, sans-serif', 
                      'color':'white', 
                      'background-color':'#2e2e2e', 
                      'fontSize':12, 
                      'border':'rgb(46,46,46)'},
                    style_header={
                      'font-family':'Hemi Head Rg',
                      'background-color': COLORS[0],
                      'color':'white'},
                    style_data_conditional=[
                      {'if':{'filter_query':'{Temp. cieczy chł. - max}>100', 
                      'column_id':'Temp. cieczy chł. - max'}, 
                      'backgroundColor':'#F7B305'},
                      {'if':{'filter_query':'{Temp. cieczy chł. - max}>110', 
                      'column_id':'Temp. cieczy chł. - max'}, 
                      'backgroundColor':'#C42904'},
                      {'if':{'filter_query':'{Temp. oleju ZM - max}>90', 
                      'column_id':'Temp. oleju ZM - max'}, 
                      'backgroundColor':'#F7B305'},
                      {'if':{'filter_query':'{Temperatura aku 1 max}>280', 
                      'column_id':'Temperatura aku 1 max'}, 
                      'backgroundColor':'#F7B305'},
                      {'if':{'filter_query':'{Temperatura aku 2 max}>280', 
                      'column_id':'Temperatura aku 2 max'}, 
                      'backgroundColor':'#F7B305'},
                      {'if':{'filter_query':'{Temperatura aku 3 max}>280', 
                      'column_id':'Temperatura aku 3 max'}, 
                      'backgroundColor':'#F7B305'},
                      {'if':{'filter_query':'{Temperatura aku 4 max}>280', 
                      'column_id':'Temperatura aku 4 max'}, 
                      'backgroundColor':'#F7B305'},
                      {'if':{'filter_query':'{Temperatura aku 5 max}>280', 
                      'column_id':'Temperatura aku 5 max'}, 
                      'backgroundColor':'#F7B305'},
                      {'if':{'filter_query':'{Temperatura aku 1 max}>300', 
                      'column_id':'Temperatura aku 1 max'}, 
                      'backgroundColor':'#C42904'},
                      {'if':{'filter_query':'{Temperatura aku 2 max}>300', 
                      'column_id':'Temperatura aku 2 max'}, 
                      'backgroundColor':'#C42904'},
                      {'if':{'filter_query':'{Temperatura aku 3 max}>300', 
                      'column_id':'Temperatura aku 3 max'}, 
                      'backgroundColor':'#C42904'},
                      {'if':{'filter_query':'{Temperatura aku 4 max}>300', 
                      'column_id':'Temperatura aku 4 max'}, 
                      'backgroundColor':'#C42904'},
                      {'if':{'filter_query':'{Temperatura aku 5 max}>300', 
                      'column_id':'Temperatura aku 5 max'}, 
                      'backgroundColor':'#C42904'},

                    ]
                ), color="white", 
              speed_multiplier = 2,
              size = 100,)
            ]) 
          ]) 
        ]),
        dcc.Tab(
          label = 'Wykresy', 
          id = "Zakladka_temperatury", 
          style = tabs.tab_style, 
          selected_style=tabs.tab_selected_style, 
          disabled_style=tabs.tab_disabled_style,
          disabled = True, 
          children = [
            html.Div(id='Plot_header'),
              dls.Hash(
                dcc.Graph(
                  id='2nd-example-graph', 
                  style={
                    'vertical-align': 'top', 
                    'margin-left': '2vw', 
                    'margin-top': '1vw', 
                    'margin-right':'2vw', 
                    'height':900}
                  ), 
                color="white", 
                speed_multiplier = 2,
                size = 100,)
              
          ]),
      
        dcc.Tab(
          label = 'Ustawienia', 
          id = "Zakladka_adminstratora", 
          style = tabs.tab_style, 
          selected_style=tabs.tab_selected_style, 
          disabled_style=tabs.tab_disabled_style,
          disabled = False, 
          children = [
            html.H1("Ustawienia systemu"),
            # html.Small(ling.polski[0], \
            #   style={"color":"white"}),
            du.Upload(
              id='dash_uploader',
              text="Wrzuć tutaj pliki do wysłania",
              text_completed="Wrzucono ",
              filetypes = ['csv'],
              ),
            html.Button('Test', id='test_button'),
            html.Div(id='testowy_tekst')
        ])
      ])
    ])
])
# ================   END OF HTML STRUCTURE   =================================

# ====================     CALLBACKS      =================================


@app.callback(
    Output('testowy_tekst', 'children'),
    Input('test_button', 'n_clicks')
)
def przygotuj_analizy(btn1):
    return html.Div('tekst')


# Loading bar
@app.callback(
        Output("div-loading", "children"),
        [Input("div-app", "loading_state")],
        [State("div-loading", "children"),]
    )
def hide_loading_after_startup(loading_state, children):
  if children:
    return None
  raise PreventUpdate

# START SERVER
if __name__ == '__main__':
  app.run_server(debug=True)