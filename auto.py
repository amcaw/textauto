import requests
import pandas as pd
import datetime as dt    
from bs4 import BeautifulSoup
import json

#import data

url_lux = "https://carbu.com/luxembourg//prixmaximum"
data_lux = requests.get(url_lux).text
url_be = "https://carbu.com/belgique//prixmaximum"
data_be = requests.get(url_be).text

soup_lux = BeautifulSoup(data_lux, 'html.parser')
soup_be = BeautifulSoup(data_be, 'html.parser')

tables_lux = soup_lux.find_all('table')
tables_be = soup_be.find_all('table')

table_lux = soup_lux.find('table', class_='prix-officiel')
table_be = soup_be.find('table', class_='prix-officiel')

#Collecting Data Lux

df_lux = pd.DataFrame(columns=['carburants', 'prix'])

for row in table_lux.tbody.find_all('tr'):    
    # Find all data for each column
    columns = row.find_all('td')
    
    if(columns != []):
        carburants = columns[0].text.strip()
        prix = columns[1].text.strip()

        df_lux = df_lux.append({'carburants': carburants,  'prix': prix}, ignore_index=True)
        
#Nettoyage pour merge après

df_lux['carburants'] = df_lux['carburants'].str.replace('Super 95','Super 95 (E5)')
df_lux['carburants'] = df_lux['carburants'].str.replace('Super 98','Super 98 (E5)')
df_lux['carburants'] = df_lux['carburants'].str.replace('Diesel','Diesel (B7)')

#Collecting Data Be

df_be = pd.DataFrame(columns=['carburants', 'prix'])

for row in table_be.tbody.find_all('tr'):    
    # Find all data for each column
    columns = row.find_all('td')
    
    if(columns != []):
        carburants = columns[0].text.strip()
        prix = columns[1].text.strip()

        df_be = df_be.append({'carburants': carburants,  'prix': prix}, ignore_index=True)
        
#On merge

result = pd.merge(df_be, df_lux, on='carburants')
result = result.rename(columns={'prix_x': 'Belgique', 'prix_y': 'Luxembourg'})

#vire euros, espace, virgule, date

result['Belgique'] = result['Belgique'].str.replace(' €/l','')
result['Belgique'] = result['Belgique'].str.replace(',','.')
result['Luxembourg'] = result['Luxembourg'].str.replace(' €/l','')
result['Luxembourg'] = result['Luxembourg'].str.replace(',','.')

result['Belgique'] = result['Belgique'].astype(float)
result['Luxembourg'] = result['Luxembourg'].astype(float)

result['prix'] = 'prix'

result = pd.pivot_table(result, values=['Belgique', 'Luxembourg'], index='prix',columns='carburants')

result.columns = result.columns.map('_'.join)

#On ajoute la date du jour

result['date'] = dt.datetime.today().strftime("%e %B")

result['date'] = result['date'].str.replace('March','mars')


#On exporte en Json en forçant Unicode
with open('./result.json', 'w') as output_file:
    result.to_json(output_file, force_ascii=False, orient='index')
