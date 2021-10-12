#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from datetime import datetime
df_deces = pd.read_csv ('https://epistat.sciensano.be/Data/COVID19BE_MORT.csv')
df_cas = pd.read_csv ('https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv')
df_date = pd.read_csv ('https://raw.githubusercontent.com/amcaw/textauto/main/dates.csv')
df_test = pd.read_csv ('https://epistat.sciensano.be/Data/COVID19BE_tests.csv')
df_admissions = pd.read_csv ('https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv')
df_hospi = pd.read_csv ('https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv')
df_pos = pd.read_csv ('https://epistat.sciensano.be/Data/COVID19BE_tests.csv')
df_RT = pd.read_csv ('https://raw.githubusercontent.com/amcaw/reproduction_rate/main/result.csv')

# Pour afficher la date de mise à jour

df_maj = datetime.today().strftime("%d/%m/%Y à %Hh%M")

# Astuce pour éviter un trou dans les dates

df_astuce = df_RT
df_astuce = pd.DataFrame(df_astuce)
df_astuce['CASES'] = 0
df_astuce['DEATHS'] = 0
df_astuce = df_astuce.tail(1)

# Calcul des décès

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
df_deces['deces2'] = df_deces['deces2'].map('{: ,.1f}'.format)
df_deces['deces1'] = df_deces['deces1'].str.replace(',','.')
df_deces['deces2'] = df_deces['deces2'].str.replace('.',',')
df_deces['deces2'] = df_deces['deces2'].str.replace(',0','')

# Calcul des cas
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

# Calcul des tests
df_test = df_test[['DATE', 'TESTS_ALL']]
df_test = df_test.groupby(['DATE'], as_index=False)['TESTS_ALL'].sum()
df_test['tests1'] = (df_test['TESTS_ALL'].rolling(window=7).mean()).round(0)
df_test['tests2'] = ((df_test['tests1'].pct_change(7)) * 100).round(0)
df_test['DATE'] = df_test['DATE'].tail(4)
df_test.dropna(subset = ['DATE'], inplace=True)
df_test['DATE'] = df_test['DATE'].head(1)
df_test.dropna(subset = ['DATE'], inplace=True)
df_test = pd.merge(df_test, df_date)
df_test['tests1'] = df_test['tests1'].map('{: ,.0f}'.format)
df_test['tests2'] = df_test['tests2'].map('{:+,.0f}'.format)
df_test['tests1'] = df_test['tests1'].str.replace(',','.')
df_test['tests2'] = df_test['tests2'].replace({'\+':'en hausse de '}, regex = True)
df_test['tests2'] = df_test['tests2'].replace({'\-':'en baisse de '}, regex = True)

# Calcul des admissions
df_admissions = df_admissions[['DATE', 'NEW_IN']]
df_admissions = df_admissions.groupby(['DATE'], as_index=False)['NEW_IN'].sum()
df_admissions['hospi'] = df_admissions['NEW_IN'].cumsum()
df_admissions['hospi_dif'] = df_admissions['hospi'].diff()
df_admissions['hospi1'] = (df_admissions['hospi_dif'].rolling(window=7).mean()).round(1)
df_admissions['hospi2'] = (df_admissions['hospi1'].diff(7)).round(0)
df_admissions['hospi3'] = ((df_admissions['hospi1'].pct_change(7) * 100)).round()
df_admissions['DATE'] = df_admissions['DATE'].tail(1)
df_admissions.dropna(subset = ['DATE'], inplace=True)
df_admissions = pd.merge(df_admissions, df_date)
df_admissions['hospi1'] = df_admissions['hospi1'].map('{: ,.1f}'.format)
df_admissions['hospi3'] = df_admissions['hospi3'].map('{:+,.0f}'.format)
df_admissions['hospi1'] = df_admissions['hospi1'].replace({'\.':','}, regex = True)
df_admissions['hospi1'] = df_admissions['hospi1'].str.replace(',0','')
df_admissions['hospi3'] = df_admissions['hospi3'].replace({'\+':'une augmentation de '}, regex = True)
df_admissions['hospi3'] = df_admissions['hospi3'].replace({'\-':'une diminution de '}, regex = True)

# Calcul des hospitalisations
df_hospi1 = df_hospi[['DATE', 'TOTAL_IN']]
df_hospi2 = df_hospi[['DATE', 'TOTAL_IN_ICU']]
df_hospi1 = df_hospi1.groupby(['DATE'], as_index=False)['TOTAL_IN'].sum()
df_hospi2 = df_hospi2.groupby(['DATE'], as_index=False)['TOTAL_IN_ICU'].sum()
df_hospi = pd.merge(df_hospi1, df_hospi2)
df_hospi['DATE'] = df_hospi['DATE'].tail(1)
df_hospi.dropna(subset = ['DATE'], inplace=True)

# Calcul du taux de positivité
df_pos1 = df_pos[['DATE', 'TESTS_ALL']]
df_pos2 = df_pos[['DATE', 'TESTS_ALL_POS']]
df_pos1 = df_pos1.groupby(['DATE'], as_index=False)['TESTS_ALL'].sum()
df_pos2 = df_pos2.groupby(['DATE'], as_index=False)['TESTS_ALL_POS'].sum()
df_pos = pd.merge(df_pos1, df_pos2)
df_pos['tests1'] = (df_pos['TESTS_ALL'].rolling(window=7).mean()).round(0)
df_pos['tests2'] = (df_pos['TESTS_ALL_POS'].rolling(window=7).mean()).round(0)
df_pos['tests3'] = ((df_pos['tests2'] * 100) / df_pos['tests1']).round(1)
df_pos['tests4'] = (df_pos['tests3'].diff(7)).round(1)
df_pos['DATE'] = df_pos['DATE'].tail(4)
df_pos.dropna(subset = ['DATE'], inplace=True)
df_pos['DATE'] = df_pos['DATE'].head(1)
df_pos.dropna(subset = ['DATE'], inplace=True)
df_pos = pd.merge(df_pos, df_date)
df_pos['tests4'] = df_pos['tests4'].map('{:+,.1f}'.format)
df_pos['tests4'] = df_pos['tests4'].replace({'\.':','}, regex = True)
df_pos['tests4'] = df_pos['tests4'].replace({'\+':'en hausse de '}, regex = True)
df_pos['tests4'] = df_pos['tests4'].replace({'\-':'en baisse de '}, regex = True)
df_pos['tests5'] = df_pos['tests3'].astype(str)
df_pos['tests5'] = df_pos['tests5'].str.replace('.',',')
df_pos['tests5'] = df_pos['tests5'].str.replace(',0','')


# Calcul du Rt
df_RT = df_RT[['DATE', 'Rt']]
df_RT['DATE'] = df_RT['DATE'].tail(1)
df_RT.dropna(subset = ['DATE'], inplace=True)
df_RT['Rt'] = df_RT['Rt'].astype(str)
df_RT['Rt'] = df_RT['Rt'].str.replace('.',',')

# Création du texte

date_cas = df_cas.iloc[0,6]
cas = df_cas.iloc[0,4]
cas_pc = df_cas.iloc[0,5]

date_test = df_test.iloc[0,4]
test = df_test.iloc[0,2]
test_pc = df_test.iloc[0,3]

date_admissions = df_admissions.iloc[0,7]
admissions = df_admissions.iloc[0,4]
admissions_pc = df_admissions.iloc[0,6]

date_deces = df_deces.iloc[0,4]
deces = df_deces.iloc[0,3]
deces_total = df_deces.iloc[0,2]

hospi1 = df_hospi.iloc[0,1]
hospi2 = df_hospi.iloc[0,2]

date_pos = df_pos.iloc[0,7]
pos = df_pos.iloc[0,8]
pos_pc = df_pos.iloc[0,6]

Rt = df_RT.iloc[0,1]

maj = df_maj

texte = (F"<strong>Texte mis à jour le {maj}</strong><h2>Les chiffres consolidés du tableau de Sciensano</h2><p>Note : ces chiffres sont tirés des données actualisées publiées par Sciensano en open data <a href='https://datastudio.google.com/embed/u/0/reporting/c14a5cfc-cab7-4812-848c-0369173148ab/page/ZwmOB_blank'>et mises sous forme de tableau ici</a>.<p><strong>Cas détectés¹</strong> : {date_cas},<strong>{cas}</strong> nouvelles infections au coronavirus ont été détectées en moyenne chaque jour. C'est {cas_pc}% par rapport à la semaine précédente.<p><strong>Tests</strong> : {date_test}, une moyenne de<strong>{test}</strong> tests ont été effectués quotidiennement, un total {test_pc}% par rapport à la semaine précédente.<p><strong>Admissions</strong> : elles s'élèvent en moyenne à <strong>{admissions}</strong> {date_admissions}. C'est {admissions_pc}% par rapport à la semaine précédente.<p><strong>Personnes hospitalisées²</strong> : <strong>{hospi1}</strong> patients sont actuellement hospitalisés en lien avec le Covid-19, dont <strong>{hospi2}</strong> patients traités en soins intensifs.<p><strong>Taux de positivité³</strong> : sur la base des résultats des tests obtenus {date_pos}, il est de <strong>{pos}%</strong>, {pos_pc}% par rapport à la semaine dernière.<p><strong>Taux de reproduction</strong> : calculé sur la base de l'évolution des admissions, le Rt du coronavirus s'établit aujourd'hui à <strong>{Rt}</strong>. Lorsqu'il est supérieur à 1, cela signifie que la transmission du virus s'accélère.<p><strong>Décès</strong> : {date_deces},<strong>{deces}</strong> personnes sont décédées en moyenne des suites du virus. Depuis le début de l'épidémie,{deces_total} personnes sont mortes du coronavirus.<p>¹ Les cas détectés sont le nombre de patients pour lesquels un test positif a confirmé la présence du virus. La date qui est considérée est celle du diagnostic, pas du résultat du test. Les données sont considérées comme consolidées après 4 jours. Le nombre de cas peut dépendre en partie de la stratégie de testing : si on teste plus systématiquement, on détecte aussi plus de cas.<p>² Dans les personnes hospitalisées sont comptabilisés des patients déjà hospitalisés pour une autre raison, et qui ont effectué un test positif.<p>³ Le taux de positivité est le nombre de tests positifs par rapport au nombre de tests effectués. Une même personne peut être testée plusieurs fois. Il dépend lui aussi de la stratégie de testing : si on ne teste pas assez, le taux de positivité va être plus élevé.")

text = ""
with open('README.md', 'w') as md:
    md.write(texte)
