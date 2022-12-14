import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree
from pprint import pprint
from html_table_parser.parser import HTMLTableParser
from html.parser import HTMLParser
import urllib.request
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

URL_FAROESE = "https://www.fsf.fo/landslidini/menn/a-landslidid/landsdystir-1988-2022/"


def url_get_contents(url):
    """ Opens a website and read its binary contents (HTTP Response Body) """
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    return f.read()


def get_data_faroese_national_team(url_faroese, colors):
    page = requests.get(url_faroese)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find("table")
    column_names = []
    for row in table.find_all('tr'):
        td_tags = row.find_all('td')
        column_names.append(td_tags)
    df_matches = pd.DataFrame(columns=['No', 'Date', 'Round', 'Opponent', 'Result',
                                       'H/A', 'W/D/L', 'Scored', 'Conceded'])
    table_items = len(column_names)
    for i in range(1, table_items):
        df_matches.at[i, "No"] = str(column_names[i][0])[4:-5]
        df_matches.at[i, "Date"] = str(column_names[i][1])[4:-5]
        if str(column_names[i][2])[4:-5] == "Venjingardystur":
            df_matches.at[i, "Round"] = "Friendly"
        else:
            df_matches.at[i, "Round"] = str(column_names[i][2])[4:-5]
        df_matches.at[i, "Opponent"] = str(column_names[i][3])[4:-5]
        if str(column_names[i][3])[4:9] == "Føroy":
            where = "H"
            df_matches.at[i, "H/A"] = "H"
        else:
            where = "A"
            df_matches.at[i, "H/A"] = "A"
        df_matches.at[i, "Result"] = str(column_names[i][4])[4:-5]
        h_goals = int(str(column_names[i][4])[4:5])
        a_goals = int(str(column_names[i][4])[6:7])
        if where == "H":
            df_matches.at[i, "Scored"] = h_goals
            df_matches.at[i, "Conceded"] = a_goals
            if h_goals > a_goals:
                df_matches.at[i, "W/D/L"] = "W"
            elif h_goals < a_goals:
                df_matches.at[i, "W/D/L"] = "L"
            else:
                df_matches.at[i, "W/D/L"] = "D"
        else:
            df_matches.at[i, "Scored"] = a_goals
            df_matches.at[i, "Conceded"] = h_goals
            if h_goals > a_goals:
                df_matches.at[i, "W/D/L"] = "L"
            elif h_goals < a_goals:
                df_matches.at[i, "W/D/L"] = "W"
            else:
                df_matches.at[i, "W/D/L"] = "D"

    bramki_strzelone = df_matches["Scored"].sum()

    bramki_puszczone = df_matches["Conceded"].sum()

    wins = len(df_matches[df_matches['W/D/L'] == 'W'])
    draws = len(df_matches[df_matches['W/D/L'] == 'D'])
    losses = len(df_matches[df_matches['W/D/L'] == 'L'])
    return df_matches
