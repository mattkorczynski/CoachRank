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
from dash import html
from dash import dcc
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
import GetDataFromWeb as gd
import libs.figures_faroe_football as figlib
import unittest
import libs.translator as trl

# Password pairs defined by external library

app = Dash(__name__)
app.title = "Faroe Islands football leagues"


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

URL_FAROESE = "https://www.fsf.fo/landslidini/menn/a-landslidid/landsdystir-1988-2022/"

df_table_2022 = pd.read_csv("F:\\PROGRAMOWANIE\\CoachRank\\data\\league_table_2022.csv",
                            sep=';',
                            error_bad_lines=False)
df_table_2022_2 = pd.read_csv("F:\\PROGRAMOWANIE\\CoachRank\\data\\league_table_2022_2.csv",
                            sep=';',
                            error_bad_lines=False)

df_national_team_results = gd.get_data_faroese_national_team(URL_FAROESE, COLORS)
df_national_team_results = trl.translate_faroese_countries(df_national_team_results)

wins = len(df_national_team_results[df_national_team_results['W/D/L'] == 'W'])
draws = len(df_national_team_results[df_national_team_results['W/D/L'] == 'D'])
losses = len(df_national_team_results[df_national_team_results['W/D/L'] == 'L'])
figure = figlib.draw_plot_wins(wins, draws, losses, COLORS)
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
          label = 'Betri Deildin (1)',
          style = tabs.tab_style, 
          selected_style=tabs.tab_selected_style, 
          children = [
          html.Div([
            html.H1('Betri Deildin - 1st level football league stats 2022'),
            dash_table.DataTable(
               df_table_2022.to_dict('records'),
               [{"name": i, "id": i} for i in df_table_2022.columns],
               id='tbl',
               page_action='none',
               style_table={
                 'height':'400px',
                 'width':'900px',
                 'font':"Signika-Regular",
                 'position': 'relative',
                 'left':50,
                 'top':30},
               style_cell={
                 'text-align':'center',
                 'minWidth': '90px',
                 'width': '180px',
                 'maxWidth': '180px'},
               style_data={
                 'font-family':'Signika-Regular',
                 'color':'white',
                 'background-color':'#2e2e2e',
                 'fontSize':16,
                 'border':'rgb(46,46,46)'},
               style_header={
                       'font-family':'Signika-Regular',
                       'background-color': COLORS[0],
                       'fontSize':18,
                       'color':'white'},
               style_data_conditional=[
                  {'if':{'filter_query':'{Pos}="1"'}, 'backgroundColor': COLORS[5]},
                  {'if':{'filter_query':'{Pos}="10"'}, 'backgroundColor': COLORS[3]},
                  {'if': {'filter_query': '{Pos}="2"'}, 'backgroundColor': COLORS[2]},
                  {'if': {'filter_query': '{Pos}="3"'}, 'backgroundColor': COLORS[2]},
                  {'if': {'filter_query': '{Pos}="4"'}, 'backgroundColor': COLORS[2]},
                  {'if': {'filter_query': '{Pos}="9"'}, 'backgroundColor': COLORS[4]}
            #     {'if': {'column_id': 'Nr'}, 'width': '10%'},
            #     {'if': {'column_id': 'Typ'}, 'width': '10%'},
                 ]
               )
            ], className="six columns"),
            html.H3('1st - UEFA Champions League - preliminary round'),
            html.H3('2nd and 3rd - UEFA Europe Conference League - first qualifying round'),
            html.H3('Cup winner - UEFA Europe Conference League - first qualifying round'),
            html.H3('9th - relegation play-offs'),
            html.H3('10th - relegated'),
                ]),
        dcc.Tab(
          label='Division 1 (2)',
          style = tabs.tab_style, 
          id = "Zakladka_ogolne", 
          selected_style=tabs.tab_selected_style, 
          disabled_style=tabs.tab_disabled_style,
          disabled = False,
          children=[
            html.Div([
              html.H1('2nd level football league stats 2022'),
              dash_table.DataTable(
                df_table_2022_2.to_dict('records'),
                [{"name": i, "id": i} for i in df_table_2022_2.columns],
                id='tbl_2',
                page_action='none',
                style_table={
                  'height': '400px',
                  'width': '900px',
                  'font': "Signika-Regular",
                  'position': 'relative',
                  'left': 50,
                  'top': 30},
                style_cell={
                  'text-align': 'center',
                  'minWidth': '90px',
                  'width': '180px',
                  'maxWidth': '180px'},
                style_data={
                  'font-family': 'Signika-Regular',
                  'color': 'white',
                  'background-color': '#2e2e2e',
                  'fontSize': 16,
                  'border': 'rgb(46,46,46)'},
                style_header={
                  'font-family': 'Signika-Regular',
                  'background-color': COLORS[0],
                  'fontSize': 18,
                  'color': 'white'},
                style_data_conditional=[
                  {'if': {'filter_query': '{Pos}="1"'}, 'backgroundColor': COLORS[5]},
                  {'if': {'filter_query': '{Pos}="10"'}, 'backgroundColor': COLORS[3]},
                  {'if': {'filter_query': '{Pos}="3"'}, 'backgroundColor': COLORS[2]},
                  {'if': {'filter_query': '{Pos}="9"'}, 'backgroundColor': COLORS[4]}
                  #     {'if': {'column_id': 'Nr'}, 'width': '10%'},
                  #     {'if': {'column_id': 'Typ'}, 'width': '10%'},
                ]
              )
            ], className="six columns"),
            html.H3('R - Reserve Team')
          ]),
        dcc.Tab(
          label = 'National team',
          id = "National team",
          style = tabs.tab_style, 
          selected_style=tabs.tab_selected_style, 
          disabled_style=tabs.tab_disabled_style,
          disabled = False,
          children = [
            html.Div([
              html.H1('National team results in history'),
              dash_table.DataTable(
                df_national_team_results.to_dict('records_2'),
                [{"name": i, "id": i} for i in df_national_team_results.columns],
                id='tbl2',
                page_action='none',
                style_table={
                  'height': '6900px',
                  'width': '900px',
                  'font': "Signika-Regular",
                  'position': 'absolute',
                  'left': '50px',
                  'top': '30px'},
                style_cell={
                  'text-align': 'center',
                  'minWidth': '90px',
                  'width': '180px',
                  'maxWidth': '180px'},
                style_data={
                  'font-family': 'Signika-Regular',
                  'color': 'white',
                  'background-color': '#2e2e2e',
                  'fontSize': 16,
                  'border': 'rgb(46,46,46)'},
                style_header={
                  'font-family': 'Signika-Regular',
                  'background-color': COLORS[0],
                  'fontSize': 18,
                  'color': 'white'},
                style_data_conditional=[
                  {'if': {'filter_query': '{W/D/L}="W"'}, 'backgroundColor': COLORS[5]},
                  {'if': {'filter_query': '{W/D/L}="L"'}, 'backgroundColor': COLORS[3]},
                  {'if': {'filter_query': '{W/D/L}="D"'}, 'backgroundColor': COLORS[2]}
                  #     {'if': {'column_id': 'Nr'}, 'width': '10%'},
                  #     {'if': {'column_id': 'Typ'}, 'width': '10%'},
                ]
              ),
              dcc.Graph(
                id='czas_pracy_graph_slupki',
                      style={
                        'vertical-align': 'top',
                        'margin-left': '1vw',
                        'margin-top': '1vw',
                        'margin-right':'2vw',
                        'width' :'500px',
                        'height' : '400px',
                        'display':"inline-block",
                        'position': 'absolute',
                        'left': '970px',
                        'top': '30px'
                        }
                      )
          ])
         ]),
        dcc.Tab(
          label='Settings',
          id="Zakladka_adminstratora",
          style = tabs.tab_style, 
          selected_style=tabs.tab_selected_style, 
          disabled_style=tabs.tab_disabled_style,
          disabled = False, 
          children = [
            html.H1("System settings"),
            # html.Small(ling.polski[0], \
            #   style={"color":"white"}),
            du.Upload(
              id='dash_uploader',
              text="Put here the file",
              text_completed="File uploaded",
              filetypes=['csv'],
              ),
            html.Button('Test', id='test_button'),
            html.Div(id='testowy_tekst')
        ]),
        dcc.Tab(
          label='Team Info',
          id="tab_team_info",
          style=tabs.tab_style,
          selected_style=tabs.tab_selected_style,
          disabled_style=tabs.tab_disabled_style,
          disabled=True,
          children=[
            html.Div(id='Plot_header_2'),
            dls.Hash(
              dcc.Graph(
                id='2nd-example-graph-2',
                style={
                  'vertical-align': 'top',
                  'margin-left': '2vw',
                  'margin-top': '1vw',
                  'margin-right': '2vw',
                  'height': 900}
              ),
              color="white",
              speed_multiplier=2,
              size=100, )

          ])
      ])
    ])
])
# ================   END OF HTML STRUCTURE   =================================

# ====================     CALLBACKS      =================================


@app.callback(
    Output('testowy_tekst', 'children'),
    Output('czas_pracy_graph_slupki','figure'),
    Input('test_button', 'n_clicks')
  )
def przygotuj_analizy(btn1):
  global figure
  return html.Div('tekst'), figure


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