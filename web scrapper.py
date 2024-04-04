import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO


def scrape_table(url):
    with requests.get(url) as r:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        if table:
            html_string = str(table)
            html_data = StringIO(html_string)
            df = pd.read_html(html_data)[0]
            return df
        else:
            return None


def scrape_text(url):
    with requests.get(url) as r:
        soup = BeautifulSoup(r.content, 'html.parser')
        content_div = soup.find('div', class_='mw-content-container')  #div   caption
        if content_div:
            paragraphs = content_div.find_all('p')
            text_data = '\n'.join([p.get_text() for p in paragraphs])
            return text_data
        else:
            return None


URL = 'https://en.wikipedia.org/wiki/Artificial_intelligence'#https://www.geeksforgeeks.org/python-programming-language/

scrape_table_data = int(input("enter 1 if you want to scrape  table or 2 to scrape text :"))

if scrape_table_data == 1:
    table_data = scrape_table(url=URL)
    if table_data is not None and not table_data.empty:
        print("Table data found:")
        print(table_data.head())
    else:
        print("No table data found.")
else:
    text_data = scrape_text(URL)
    if text_data:
        print("Text data found:")
        print(text_data)
    else:
        print("No text data found.")