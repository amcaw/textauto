#!/usr/bin/env python
# coding: utf-8

import pandas as pd #yoo
from datetime import datetime
df = pd.read_csv ('https://epistat.sciensano.be/Data/COVID19BE_MORT.csv')
df2 = pd.read_csv ('https://app.workbenchdata.com/workflows/146407/steps/step-4iDaSZZRjoSs/current-result-table.csv')
df = df.groupby(['DATE'], as_index=False)['DEATHS'].sum()
df['link'] = 'link'
df['deces1'] = df['DEATHS'].cumsum()
df['deces2'] = (df['DEATHS'].rolling(window=7).mean()).round(1)
df['deces1'] = df['deces1'].tail(1)
df['deces1'] = df['deces1'].bfill(axis = 0)
df['DATE'] = df['DATE'].tail(4)
df.dropna(subset = ['DATE'], inplace=True)
df['DATE'] = df['DATE'].head(1)
df.dropna(subset = ['DATE'], inplace=True)
df = pd.merge(df,df2,on='DATE')
deces = df.iloc[0,4]
deces_total = df.iloc[0,3]
df = (F"Décès : {deces} personnes sont décédées en moyenne des suites du virus. Depuis le début de l'épidémie, {deces_total} personnes sont mortes du coronavirus.")
df.to_csv("./test.csv")



