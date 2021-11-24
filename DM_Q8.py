#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 20:34:03 2021

@author: sharanya
"""


import pandas as pd
df=pd.read_excel('Datasets/DDW-C18-0000.xlsx',engine='openpyxl')
df.columns=['State Code','District Code','Area','Total/Rural/Urban','Age Group','2Persons','2Males','2Females','3Persons','3Males','3Females']
df=df.drop([0,1,2,3,4])
df=df[['State Code','Total/Rural/Urban','Age Group','2Males','2Females','3Males','3Females']]
df=df.loc[df['Total/Rural/Urban']=='Total']
df=df.loc[df['Age Group']!='Total']
df=df.loc[df['Age Group']!='Age not stated']
df.sort_values(by=['State Code','Age Group'],inplace=True)
df=df.reset_index()
df=df[['State Code','Age Group','2Males','2Females','3Males','3Females']]

df1=pd.read_excel('Datasets/DDW-0000C-14.xls')
df1.columns=['Table','State Code','District Code','Area','Age Group','TP','TM','TF','RP','RM','RF','UP','UM','UF']
df1=df1.drop([0,1,2,3,4,5])
df1=df1.loc[df1['Age Group']!='All ages']
df1=df1.loc[df1['Age Group']!='0-4']
df1=df1.loc[df1['Age Group']!='Age not stated']
df1=df1[['State Code','Age Group','TM','TF']]

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

df1_merged=pd.DataFrame({'Male':df1.groupby(['State Code','Age Group'])['TM'].sum(),'Female':df1.groupby(['State Code','Age Group'])['TF'].sum()}).reset_index()


df1_merged.sort_values(by=['State Code','Age Group'],inplace=True)
df1_merged=df1_merged.reset_index()
df1_merged=df1_merged[['State Code','Age Group','Male','Female']]

df['1language_male']=df1_merged['Male']-df['2Males']
df['1language_female']=df1_merged['Female']-df['2Females']
df['2language_male']=df['2Males']-df['3Males']
df['2language_female']=df['2Females']-df['3Females']

df['male1']=df['1language_male']/df1_merged['Male']
df['female1']=df['1language_female']/df1_merged['Female']


states=list(df['State Code'])
highest={}
for state in states :
    rows=[]
    rows.append(state)
    df_state=df[df['State Code']==state].reset_index()
    df_state['male1'] = pd.to_numeric(df_state['male1'])
    maxloc = df_state['male1'].idxmax()
    age_group=df_state['Age Group'].iloc[maxloc]
    maxpmale=df_state['male1'].iloc[maxloc]
    rows.append(age_group)
    rows.append(maxpmale)
    df_state['female1'] = pd.to_numeric(df_state['female1'])
    maxloc = df_state['female1'].idxmax()
    age_group=df_state['Age Group'].iloc[maxloc]
    maxpfemale=df_state['female1'].iloc[maxloc]
    rows.append(age_group)
    rows.append(maxpfemale)
    highest[state]=rows
    
    
dff=pd.DataFrame.from_dict(highest, orient='index',columns=['state/ut','age-group-males','ratio-males','age-group-females','ratio-females'])
dff.to_csv('Outputs/age-gender-c.csv',index=False)

df['male2']=df['2language_male']/df1_merged['Male']
df['female2']=df['2language_female']/df1_merged['Female']

states=list(df['State Code'])
highest={}
for state in states :
    rows=[]
    rows.append(state)
    df_state=df[df['State Code']==state].reset_index()
    df_state['male2'] = pd.to_numeric(df_state['male2'])
    maxloc = df_state['male2'].idxmax()
    age_group=df_state['Age Group'].iloc[maxloc]
    maxpmale=df_state['male2'].iloc[maxloc]
    rows.append(age_group)
    rows.append(maxpmale)
    df_state['female2'] = pd.to_numeric(df_state['female2'])
    maxloc = df_state['female2'].idxmax()
    age_group=df_state['Age Group'].iloc[maxloc]
    maxpfemale=df_state['female2'].iloc[maxloc]
    rows.append(age_group)
    rows.append(maxpfemale)
    highest[state]=rows
    
dff2=pd.DataFrame.from_dict(highest, orient='index',columns=['state/ut','age-group-males','ratio-males','age-group-females','ratio-females'])
dff2.to_csv('Outputs/age-gender-b.csv',index=False)


df['male3']=df['3Males']/df1_merged['Male']
df['female3']=df['3Females']/df1_merged['Female']

states=list(df['State Code'])
highest={}
for state in states :
    rows=[]
    rows.append(state)
    df_state=df[df['State Code']==state].reset_index()
    df_state['male3'] = pd.to_numeric(df_state['male3'])
    maxloc = df_state['male3'].idxmax()
    age_group=df_state['Age Group'].iloc[maxloc]
    maxpmale=df_state['male3'].iloc[maxloc]
    rows.append(age_group)
    rows.append(maxpmale)
    df_state['female3'] = pd.to_numeric(df_state['female3'])
    maxloc = df_state['female3'].idxmax()
    age_group=df_state['Age Group'].iloc[maxloc]
    maxpfemale=df_state['female3'].iloc[maxloc]
    rows.append(age_group)
    rows.append(maxpfemale)
    highest[state]=rows
    
dff3=pd.DataFrame.from_dict(highest, orient='index',columns=['state/ut','age-group-males','ratio-males','age-group-females','ratio-females'])
dff3.to_csv('Outputs/age-gender-a.csv',index=False)
