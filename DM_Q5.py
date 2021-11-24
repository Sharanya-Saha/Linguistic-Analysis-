#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 18:18:03 2021

@author: sharanya
"""

import pandas as pd
df=pd.read_excel('Datasets/DDW-C18-0000.xlsx',engine='openpyxl')
df.columns=['State Code','District Code','Area','Total/Rural/Urban','Age Group','2Persons','2Males','2Females','3Persons','3Males','3Females']
df=df.drop([0,1,2,3,4])
df=df[['State Code','Total/Rural/Urban','Age Group','3Persons']]
df=df.loc[df['Total/Rural/Urban']=='Total']
df=df.loc[df['Age Group']!='Total']
df=df.loc[df['Age Group']!='Age not stated']
df.sort_values(by=['State Code','Age Group'],inplace=True)
df=df.reset_index()
df=df[['State Code','Age Group','3Persons']]

df1=pd.read_excel('Datasets/DDW-0000C-14.xls')
df1.columns=['Table','State Code','District Code','Area','Age Group','TP','TM','TF','RP','RM','RF','UP','UM','UF']
df1=df1.drop([0,1,2,3,4,5])
df1=df1.loc[df1['Age Group']!='All ages']
df1=df1.loc[df1['Age Group']!='0-4']
df1=df1.loc[df1['Age Group']!='Age not stated']
df1=df1[['State Code','Age Group','TP']]

df1.loc[df1['Age Group'] == "30-34" , "Age Group"] = "30-49"
df1.loc[df1['Age Group'] == "35-39" , "Age Group"] = "30-49"
df1.loc[df1['Age Group'] == "40-44" , "Age Group"] = "30-49"
df1.loc[df1['Age Group'] == "45-49" , "Age Group"] = "30-49"
df1.loc[df1['Age Group'] == "50-54" , "Age Group"] = "50-69"
df1.loc[df1['Age Group'] == "55-59" , "Age Group"] = "50-69"
df1.loc[df1['Age Group'] == "60-64" , "Age Group"] = "50-69"
df1.loc[df1['Age Group'] == "65-69" , "Age Group"] = "50-69"
df1.loc[df1['Age Group'] == "70-74" , "Age Group"] = "70+"
df1.loc[df1['Age Group'] == "75-79" , "Age Group"] = "70+"
df1.loc[df1['Age Group'] == "80+" , "Age Group"] = "70+"

df1_merged=pd.DataFrame({'Population':df1.groupby(['State Code','Age Group'])['TP'].sum()}).reset_index()


df1_merged.sort_values(by=['State Code','Age Group'],inplace=True)
df1_merged=df1_merged.reset_index()
df1_merged=df1_merged[['State Code','Age Group','Population']]

df['percentage']=df['3Persons']/df1_merged['Population']
df['percentage']=df['percentage']*100

states=list(df['State Code'])
highest={}
for state in states :
    rows=[]
    rows.append(state)
    df_state=df[df['State Code']==state].reset_index()
    df_state['percentage'] = pd.to_numeric(df_state['percentage'])
    maxloc = df_state['percentage'].idxmax()
    age_group=df_state['Age Group'].iloc[maxloc]
    maxp=df_state['percentage'].iloc[maxloc]
    rows.append(age_group)
    rows.append(maxp)
    highest[state]=rows
    
dff=pd.DataFrame.from_dict(highest, orient='index',columns=['state/ut','age-group','percentage'])
dff.to_csv('Outputs/age-india.csv',index=False)