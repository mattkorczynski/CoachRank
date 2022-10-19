import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree
from pprint import pprint
from html_table_parser.parser import HTMLTableParser
from html.parser import HTMLParser
import urllib.request
import numpy as np

URL = "http://www.90minut.pl/mecze_druzyna.php?id=330&id_sezon=101"

def url_get_contents(url):
    """ Opens a website and read its binary contents (HTTP Response Body) """
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    return f.read()

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find("table",attrs={"class":"mecze"} )
header = table.find_all("td")
print(header)
print('*******')
n_rows = 0
n_columns = 0
column_names = []
for row in table.find_all('tr'):
    td_tags = row.find_all('td')
    column_names.append(td_tags)
    
print(len(column_names))
print(column_names[2][0])
parser = HTMLParser()
parser.feed(str(column_names[2][0]))
print(parser.handle_data(str(column_names[2][0])))
print(column_names[2][1])
print(column_names[2][2])
print(column_names[2][3])
print(column_names[2][4])
print('_-_-_-_-_-_-_')
print(column_names[3][0])
print(column_names[3][1])
print(column_names[3][2])
print(column_names[3][3])
print(column_names[3][4])
print(len(column_names[3]))
# xhtml = url_get_contents(URL).decode('iso-8859-2')
# p = HTMLTableParser()
# p.feed(xhtml)
# pprint(p.tables)
# print('* * * * *')
# pprint(p.rawdata)
