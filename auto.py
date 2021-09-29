#!/usr/bin/env python
# coding: utf-8

# In[122]:


import pandas as pd
from datetime import datetime
df_deces = pd.read_csv ('https://epistat.sciensano.be/Data/COVID19BE_MORT.csv')
df_cas = pd.read_csv ('https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv')
df_date = pd.read_csv ('https://app.workbenchdata.com/workflows/146407/steps/step-4iDaSZZRjoSs/current-result-table.csv')
df_test = pd.read_csv ('https://epistat.sciensano.be/Data/COVID19BE_tests.csv')
df_admissions = pd.read_csv ('https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv')
df_hospi = pd.read_csv ('https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv')
df_pos = pd.read_csv ('https://epistat.sciensano.be/Data/COVID19BE_tests.csv')
df_RT = pd.read_csv ('https://raw.githubusercontent.com/amcaw/reproduction_rate/main/result.csv')


# In[123]:


# astuce date cas/décès

df_astuce = df_RT
df_astuce = pd.DataFrame(df_astuce)
df_astuce['CASES'] = 0
df_astuce['DEATHS'] = 0
df_astuce = df_astuce.tail(1)
display(df_astuce)


# In[124]:


#décès
df_deces = pd.concat([df_deces,df_astuce], join="outer", sort=False)
df_deces = df_deces[['DATE', 'DEATHS']]
df_deces = df_deces.groupby(['DATE'], as_index=False)['DEATHS'].sum()
df_deces['deces1'] = df_deces['DEATHS'].cumsum()
df_deces['deces2'] = (df_deces['DEATHS'].rolling(window=7).mean()).round(1)
df_deces['deces1'] = df_deces['deces1'].tail(1)
df_deces['deces1'] = df_deces['deces1'].bfill(axis = 0)
df_deces['DATE'] = df_deces['DATE'].tail(4)
df_deces.dropna(subset = ['DATE'], inplace=True)
df_deces['DATE'] = df_deces['DATE'].head(1)
df_deces.dropna(subset = ['DATE'], inplace=True)
df_deces = pd.merge(df_deces, df_date)
df_deces['deces1'] = float(df_deces['deces1'])
df_deces['deces2'] = float(df_deces['deces2'])
df_deces['deces1'] = df_deces['deces1'].map('{: ,.0f}'.format)
df_deces['deces2'] = df_deces['deces2'].map('{: ,.0f}'.format)
df_deces['deces1'] = df_deces['deces1'].str.replace(',','.')
display(df_deces)


# In[125]:


df_cas = pd.concat([df_cas,df_astuce], join="outer", sort=False)
df_cas = df_cas[['DATE', 'CASES']]
df_cas = df_cas.groupby(['DATE'], as_index=False)['CASES'].sum()
df_cas['CAS'] = df_cas['CASES'].cumsum()
df_cas['CAS_dif'] = df_cas['CAS'].diff()
df_cas['Cas1'] = (df_cas['CAS_dif'].rolling(window=7).mean()).round(0)
df_cas['Cas2'] = ((df_cas['Cas1'].pct_change(7) * 100)).round()
df_cas['DATE'] = df_cas['DATE'].tail(4)
df_cas.dropna(subset = ['DATE'], inplace=True)
df_cas['DATE'] = df_cas['DATE'].head(1)
df_cas.dropna(subset = ['DATE'], inplace=True)
df_cas = pd.merge(df_cas, df_date)
df_cas['Cas1'] = float(df_cas['Cas1'])
df_cas['Cas2'] = float(df_cas['Cas2'])
df_cas['Cas1'] = df_cas['Cas1'].map('{: ,.0f}'.format)
df_cas['Cas2'] = df_cas['Cas2'].map('{:+,.0f}'.format)
df_cas['Cas1'] = df_cas['Cas1'].str.replace(',','')
df_cas['Cas2'] = df_cas['Cas2'].replace({'\+':'une hausse de '}, regex = True)
df_cas['Cas2'] = df_cas['Cas2'].replace({'\-':'une baisse de '}, regex = True)
display(df_cas)


# In[127]:


date_cas = df_cas.iloc[0,6]
cas = df_cas.iloc[0,4]
cas_pc = df_cas.iloc[0,5]

date_deces = df_deces.iloc[0,4]
deces = df_deces.iloc[0,3]
deces_total = df_deces.iloc[0,2]


df4 = (F"<strong>Cas détectés¹</strong> : {date_cas},<strong>{cas}</strong> nouvelles infections au coronavirus ont été détectées en moyenne chaque jour. C'est {cas_pc}% par rapport à la semaine précédente.<p></p><strong>Décès</strong> : {date_deces},{deces} personnes sont décédées en moyenne des suites du virus. Depuis le début de l'épidémie,{deces_total} personnes sont mortes du coronavirus.")
print(df4)


# In[ ]:





# In[140]:





# In[141]:





# In[142]:





# In[143]:





# In[135]:


text = ""
with open('file.md', 'w') as md:
    md.write(df4)

