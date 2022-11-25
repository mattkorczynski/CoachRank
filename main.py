import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree
from pprint import pprint
from html_table_parser.parser import HTMLTableParser
from html.parser import HTMLParser
import urllib.request
import numpy as np

URL = "https://www.fsf.fo/landslidini/menn/a-landslidid/landsdystir-1988-2022/"

def url_get_contents(url):
    """ Opens a website and read its binary contents (HTTP Response Body) """
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    return f.read()

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find("table")
header = table.find_all("td")
n_rows = 0
n_columns = 0
column_names = []
for row in table.find_all('tr'):
    td_tags = row.find_all('td')
    column_names.append(td_tags)
df_matches = pd.DataFrame(columns=['No','Date','Round','Opponent','Result', 'H/A', 'W/D/L', 'Scored', 'Conceded'])
print(len(column_names))
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
print(df_matches)
bramki_strzelone = df_matches["Scored"].sum()
print(bramki_strzelone)
bramki_puszczone = df_matches["Conceded"].sum()
print(bramki_puszczone)
print(len(df_matches[df_matches['W/D/L'] == 'W']))
print(len(df_matches[df_matches['W/D/L'] == 'D']))
print(len(df_matches[df_matches['W/D/L'] == 'L']))
#print(column_names[2][0])
parser = HTMLParser()
parser.feed(str(column_names[2][0]))
#print(parser.handle_data(str(column_names[2][0])))
#print(column_names[2][1])
#print(column_names[2][2])
#print(column_names[2][3])
#print(column_names[2][4])
#print('_-_-_-_-_-_-_')
#print(column_names[3][0])
#print(column_names[3][1])
#print(column_names[3][2])
#print(column_names[3][3])
#print(column_names[3][4])
#print(len(column_names[3]))
# xhtml = url_get_contents(URL).decode('iso-8859-2')
# p = HTMLTableParser()
# p.feed(xhtml)
# pprint(p.tables)
# print('* * * * *')
# pprint(p.rawdata)
