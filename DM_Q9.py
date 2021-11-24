#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 21:17:51 2021

@author: sharanya
"""

import pandas as pd
df=pd.read_excel('Datasets/DDW-C19-0000.xlsx',engine='openpyxl')
df.columns=['State Code','District Code','Area','Total/Rural/Urban','Education Level','2Persons','2Males','2Females','3Persons','3Males','3Females']
df=df.drop([0,1,2,3,4])
df=df[['State Code','Total/Rural/Urban','Education Level','2Males','2Females','3Males','3Females']]
df=df.loc[df['Total/Rural/Urban']=='Total']
df=df.loc[df['Education Level']!='Total']
df.sort_values(by=['State Code','Education Level'],inplace=True)
df=df.reset_index()
df=df[['State Code','Education Level','2Males','2Females','3Males','3Females']]

df1=pd.read_excel('Datasets/DDW-0000C-08.xlsx',engine='openpyxl')
cols = [0,2,3,6,7,8,9,12,15,18,21,24,27,30,33,36,39,42]
df1.drop(df1.columns[cols],axis=1,inplace=True)
df1.columns=['State Code','Total/Rural/Urban','Age','male_Illiterate','female_Illiterate','male_Literate','female_Literate','male_Literate w/o ed level','female_Literate w/o ed level','male_Below Primary','female_Below Primary','male_Primary','female_Primary','male_Middle','female_Middle','male_Matric','female_Matric','male_HS','female_HS','male_NTD','female_NTD','male_TD','female_TD','male_Graduate and above','female_Graduate and above','male_Unclassified','female_Unclassified']
df1=df1.drop([0,1,2,3,4,5])
df1=df1.loc[df1['Total/Rural/Urban']=='Total']
df1=df1.loc[df1['Age']=='All ages'].reset_index()


required_cols={'male_Illiterate':'male_Illiterate','male_Literate':'male_Literate','male_Literate but below primary':'male_Below Primary','male_Primary but below middle':'male_Primary','male_Middle but below matric/secondary':'male_Middle','male_Matric/Secondary but below graduate':'male_Matric','male_HS':'male_HS','male_Td':'male_TD','male_NTD':'male_NTD','male_Graduate and above':'male_Graduate and above'}
req=[]
for j in required_cols.keys() :
    for i in range(len(df1)) :
        required={}
        required['State Code']=df1.loc[i,'State Code']
        required['Education Level']=j
        required['Males']=df1.loc[i,required_cols[j]]
        req.append(required)


dfr=pd.DataFrame(req)
dfr.sort_values(by=['State Code','Education Level'],inplace=True)
dfr=dfr.reset_index()
dfr=dfr[['State Code','Education Level','Males']]

dfr.loc[dfr['Education Level'] == "male_NTD" , "Education Level"] = "male_Matric/Secondary but below graduate"
dfr.loc[dfr['Education Level'] == "male_Td" , "Education Level"] = "male_Matric/Secondary but below graduate"
dfr.loc[dfr['Education Level'] == "male_HS" , "Education Level"] = "male_Matric/Secondary but below graduate"

male_dfr_merged=pd.DataFrame({'Male':dfr.groupby(['State Code','Education Level'])['Males'].sum()}).reset_index()


def ed_level(ed_level) :
    _,ed=ed_level.split('_')
    return ed.strip()


mlevel=list(male_dfr_merged['Education Level'])

for edl in mlevel :
    male_dfr_merged.loc[male_dfr_merged['Education Level']==edl,'Education Level']=ed_level(edl)
    
    
    
required_cols={'female_Illiterate':'female_Illiterate','female_Literate':'female_Literate','female_Literate but below primary':'female_Below Primary','female_Primary but below middle':'female_Primary','female_Middle but below matric/secondary':'female_Middle','female_Matric/Secondary but below graduate':'female_Matric','female_HS':'female_HS','female_Td':'female_TD','female_NTD':'female_NTD','female_Graduate and above':'female_Graduate and above'}
req=[]
for j in required_cols.keys() :
    for i in range(len(df1)) :
        required={}
        required['State Code']=df1.loc[i,'State Code']
        required['Education Level']=j
        required['Females']=df1.loc[i,required_cols[j]]
        req.append(required)


dfr1=pd.DataFrame(req)
dfr1.sort_values(by=['State Code','Education Level'],inplace=True)
dfr1=dfr1.reset_index()
dfr1=dfr1[['State Code','Education Level','Females']]

dfr1.loc[dfr1['Education Level'] == "female_NTD" , "Education Level"] = "female_Matric/Secondary but below graduate"
dfr1.loc[dfr1['Education Level'] == "female_Td" , "Education Level"] = "female_Matric/Secondary but below graduate"
dfr1.loc[dfr1['Education Level'] == "female_HS" , "Education Level"] = "female_Matric/Secondary but below graduate"

female_dfr_merged=pd.DataFrame({'Female':dfr1.groupby(['State Code','Education Level'])['Females'].sum()}).reset_index()

flevel=list(female_dfr_merged['Education Level'])

for edl in flevel :
    female_dfr_merged.loc[female_dfr_merged['Education Level']==edl,'Education Level']=ed_level(edl)


df['male_1language']=male_dfr_merged['Male']-df['2Males']
df['female_1language']=female_dfr_merged['Female']-df['2Females']

df['male_2language']=df['2Males']-df['3Males']
df['female_2language']=df['2Females']-df['3Females']

df['male1']=df['male_1language']/male_dfr_merged['Male']
df['female1']=df['female_1language']/female_dfr_merged['Female']

states=list(df['State Code'])
highest={}
for state in states :
    rows=[]
    rows.append(state)
    df_state=df[df['State Code']==state].reset_index()
    df_state['male1'] = pd.to_numeric(df_state['male1'])
    maxloc = df_state['male1'].idxmax()
    age_group=df_state['Education Level'].iloc[maxloc]
    maxpmale=df_state['male1'].iloc[maxloc]
    rows.append(age_group)
    rows.append(maxpmale)
    df_state['female1'] = pd.to_numeric(df_state['female1'])
    maxloc = df_state['female1'].idxmax()
    age_group=df_state['Education Level'].iloc[maxloc]
    maxpfemale=df_state['female1'].iloc[maxloc]
    rows.append(age_group)
    rows.append(maxpfemale)
    highest[state]=rows
    
    
dff1=pd.DataFrame.from_dict(highest, orient='index',columns=['state/ut','literacy-group-males','ratio-males','literacy-group-females','ratio-females'])
dff1.to_csv('Outputs/literacy-gender-c.csv',index=False)

df['male2']=df['male_2language']/male_dfr_merged['Male']
df['female2']=df['female_2language']/female_dfr_merged['Female']

states=list(df['State Code'])
highest={}
for state in states :
    rows=[]
    rows.append(state)
    df_state=df[df['State Code']==state].reset_index()
    df_state['male2'] = pd.to_numeric(df_state['male2'])
    maxloc = df_state['male2'].idxmax()
    age_group=df_state['Education Level'].iloc[maxloc]
    maxpmale=df_state['male2'].iloc[maxloc]
    rows.append(age_group)
    rows.append(maxpmale)
    df_state['female2'] = pd.to_numeric(df_state['female2'])
    maxloc = df_state['female2'].idxmax()
    age_group=df_state['Education Level'].iloc[maxloc]
    maxpfemale=df_state['female2'].iloc[maxloc]
    rows.append(age_group)
    rows.append(maxpfemale)
    highest[state]=rows
    
dff2=pd.DataFrame.from_dict(highest, orient='index',columns=['state/ut','literacy-group-males','ratio-males','literacy-group-females','ratio-females'])
dff2.to_csv('Outputs/literacy-gender-b.csv',index=False)

df['male3']=df['3Males']/male_dfr_merged['Male']
df['female3']=df['3Females']/female_dfr_merged['Female']

states=list(df['State Code'])
highest={}
for state in states :
    rows=[]
    rows.append(state)
    df_state=df[df['State Code']==state].reset_index()
    df_state['male3'] = pd.to_numeric(df_state['male3'])
    maxloc = df_state['male3'].idxmax()
    age_group=df_state['Education Level'].iloc[maxloc]
    maxpmale=df_state['male3'].iloc[maxloc]
    rows.append(age_group)
    rows.append(maxpmale)
    df_state['female3'] = pd.to_numeric(df_state['female3'])
    maxloc = df_state['female3'].idxmax()
    age_group=df_state['Education Level'].iloc[maxloc]
    maxpfemale=df_state['female3'].iloc[maxloc]
    rows.append(age_group)
    rows.append(maxpfemale)
    highest[state]=rows
    
dff3=pd.DataFrame.from_dict(highest, orient='index',columns=['state/ut','literacy-group-males','ratio-males','literacy-group-females','ratio-females'])
dff3.to_csv('Outputs/literacy-gender-a.csv',index=False)

