#!/usr/bin/env python
# coding: utf-8

# In[117]:


import pandas as pd #yoo
from datetime import datetime
df = pd.read_csv ('https://epistat.sciensano.be/Data/COVID19BE_MORT.csv')
df2 = pd.read_csv ('https://app.workbenchdata.com/workflows/146407/steps/step-4iDaSZZRjoSs/current-result-table.csv')


# In[118]:


df = df.groupby(['DATE'], as_index=False)['DEATHS'].sum()


# In[119]:


df['deces1'] = df['DEATHS'].cumsum()
df['deces2'] = (df['DEATHS'].rolling(window=7).mean()).round(1)
print(df)


# In[120]:


df['deces1'] = df['deces1'].tail(1)
df['deces1'] = df['deces1'].bfill(axis = 0)
df['DATE'] = df['DATE'].tail(4)
df.dropna(subset = ['DATE'], inplace=True)
df['DATE'] = df['DATE'].head(1)
df.dropna(subset = ['DATE'], inplace=True)


# In[121]:


df = pd.merge(df, df2)
df['deces1'] = float(df['deces1'])
df['deces2'] = float(df['deces2'])
print(df)


# In[125]:


df['deces1'] = df['deces1'].map('{: ,.0f}'.format)
df['deces2'] = df['deces2'].map('{: ,.0f}'.format)


# In[131]:


df['deces1'] = df['deces1'].str.replace(',','.')


# In[134]:


date = df.iloc[0,4]
deces = df.iloc[0,3]
deces_total = df.iloc[0,2]

## enclose your variable within the {} to display it's value in the output
df4 = (F"<strong>Décès</strong> : {date},{deces} personnes sont décédées en moyenne des suites du virus. Depuis le début de l'épidémie,{deces_total} personnes sont mortes du coronavirus.")
print(df4)


# In[135]:


text = ""
with open('file.md', 'w') as md:
    md.write(df4)

