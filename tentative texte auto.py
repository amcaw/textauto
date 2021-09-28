#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd #yoo
from datetime import datetime
df = pd.read_csv ('https://epistat.sciensano.be/Data/COVID19BE_MORT.csv')
df2 = pd.read_csv ('https://app.workbenchdata.com/workflows/146407/steps/step-4iDaSZZRjoSs/current-result-table.csv')


# In[10]:


df = df.groupby(['DATE'], as_index=False)['DEATHS'].sum()


# In[11]:


df['link'] = 'link'
df['deces1'] = df['DEATHS'].cumsum()
df['deces2'] = (df['DEATHS'].rolling(window=7).mean()).round(1)


# In[12]:


df['deces1'] = df['deces1'].tail(1)
df['deces1'] = df['deces1'].bfill(axis = 0)
df['DATE'] = df['DATE'].tail(4)
df.dropna(subset = ['DATE'], inplace=True)
df['DATE'] = df['DATE'].head(1)
df.dropna(subset = ['DATE'], inplace=True)


# In[43]:


df = pd.merge(df,df2,on='DATE')


# In[49]:


date = df.iloc[0,6]
deces = df.iloc[0,4]
deces_total = df.iloc[0,3]

## enclose your variable within the {} to display it's value in the output
df4 = (F"Décès : {date}, {deces} personnes sont décédées en moyenne des suites du virus. Depuis le début de l'épidémie, {deces_total} personnes sont mortes du coronavirus.")


# In[50]:


print(df4)


# In[ ]:





# In[ ]:




