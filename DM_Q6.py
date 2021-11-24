#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 11:29:09 2021

@author: sharanya
"""

import pandas as pd
df=pd.read_excel('Datasets/DDW-C19-0000.xlsx',engine='openpyxl')
df.columns=['State Code','District Code','Area','Total/Rural/Urban','Education Level','2Persons','2Males','2Females','3Persons','3Males','3Females']
df=df.drop([0,1,2,3,4])
df=df[['State Code','Total/Rural/Urban','Education Level','3Persons']]
df=df.loc[df['Total/Rural/Urban']=='Total']
df=df.loc[df['Education Level']!='Total']
df.sort_values(by=['State Code','Education Level'],inplace=True)
df=df.reset_index()
df=df[['State Code','Education Level','3Persons']]

df1=pd.read_excel('Datasets/DDW-0000C-08.xlsx',engine='openpyxl')
cols = [0,2,3,6,7,8,10,11,13,14,16,17,19,20,22,23,25,26,28,29,31,32,34,35,37,38,40,41,43,44]
df1.drop(df1.columns[cols],axis=1,inplace=True)
df1.columns=['State Code','Total/Rural/Urban','Age','Illiterate','Literate','Literate w/o ed level','Below Primary','Primary','Middle','Matric','HS','NTD','TD','Graduate and above','Unclassified']
df1=df1.drop([0,1,2,3,4,5])
df1=df1.loc[df1['Total/Rural/Urban']=='Total']
df1=df1.loc[df1['Age']=='All ages'].reset_index()



required_cols={'Illiterate':'Illiterate','Literate':'Literate','Literate but below primary':'Below Primary','Primary but below middle':'Primary','Middle but below matric/secondary':'Middle','Matric/Secondary but below graduate':'Matric','HS':'HS','NTD':'NTD','TD':'TD','Graduate and above':'Graduate and above'}
req=[]
for j in required_cols.keys() :
    for i in range(len(df1)) :
        required={}
        required['State Code']=df1.loc[i,'State Code']
        required['Education Level']=j
        required['3Persons']=df1.loc[i,required_cols[j]]
        req.append(required)

dfr=pd.DataFrame(req)
dfr.sort_values(by=['State Code','Education Level'],inplace=True)
dfr=dfr.reset_index()
dfr=dfr[['State Code','Education Level','3Persons']]

dfr.loc[dfr['Education Level'] == "NTD" , "Education Level"] = "Matric/Secondary but below graduate"
dfr.loc[dfr['Education Level'] == "TD" , "Education Level"] = "Matric/Secondary but below graduate"
dfr.loc[dfr['Education Level'] == "HS" , "Education Level"] = "Matric/Secondary but below graduate"

dfr_merged=pd.DataFrame({'3Persons':dfr.groupby(['State Code','Education Level'])['3Persons'].sum()}).reset_index()


df['percentage']=df['3Persons']/dfr_merged['3Persons']
df['percentage']=df['percentage']*100

states=list(df['State Code'])
highest={}
for state in states :
    rows=[]
    rows.append(state)
    df_state=df[df['State Code']==state].reset_index()
    df_state['percentage'] = pd.to_numeric(df_state['percentage'])
    maxloc = df_state['percentage'].idxmax()
    literacy_group=df_state['Education Level'].iloc[maxloc]
    maxp=df_state['percentage'].iloc[maxloc]
    rows.append(literacy_group)
    rows.append(maxp)
    highest[state]=rows
    
dff=pd.DataFrame.from_dict(highest, orient='index',columns=['state/ut','literacy-group','percentage'])

dff.to_csv('Outputs/literacy-india.csv',index=False)