#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 00:45:45 2021

@author: sharanya
"""

import pandas as pd
from scipy.stats import ttest_ind
df=pd.read_excel('Datasets/DDW-C18-0000.xlsx',engine='openpyxl')
df.columns=['State Code','District Code','Area','Total/Rural/Urban','Age Group','2Persons','2Males','2Females','3Persons','3Males','3Females']
df=df.drop([0,1,2,3,4])
df=df[['State Code','Total/Rural/Urban','Age Group','2Males','2Females','3Males','3Females']]
df=df.loc[df['Total/Rural/Urban']=='Total']
df=df.loc[df['Age Group']=='Total']

dfcensus=pd.read_excel('Datasets/DDW_PCA0000_2011_Indiastatedist.xlsx',engine='openpyxl')
dfcensus=dfcensus[['Level','State','TRU','TOT_M','TOT_F']]
dfcensus=dfcensus.loc[dfcensus['Level']!='DISTRICT']
dfcensus=dfcensus.loc[dfcensus['TRU']=='Total']

df.sort_values(by=['State Code'],inplace=True)
df=df.reset_index()
df=df[['State Code','2Males','2Females','3Males','3Females']]
dfcensus.sort_values(by=['State'],inplace=True)
dfcensus=dfcensus.reset_index()
dfcensus=dfcensus[['State','TOT_M','TOT_F']]




df['1Males']=dfcensus['TOT_M']-df['2Males']
df['1Females']=dfcensus['TOT_F']-df['2Females']

df['2M']=df['2Males']-df['3Males']
df['2F']=df['2Females']-df['3Females']



def cal_pval(ratio, background) :
    t, p = ttest_ind(ratio, background,equal_var=False)
    #print(p)
    return p
    

required={}
for state in list(df['State Code']) :
    #print(state)
    state_df=df[df['State Code']==state]
    ratio=[]
    ratio.append(float(state_df['1Males']/state_df['1Females']))
    ratio.append(float(state_df['2M']/state_df['2F']))
    ratio.append(float(state_df['3Males']/state_df['3Females']))
    state_df1=dfcensus[dfcensus['State']==int(state)]
    background=state_df1['TOT_M'].values/state_df1['TOT_F'].values
    bg=[background]*3
    required[state]=cal_pval(ratio,bg)

df['3male-percentage']=df['3Males']/dfcensus['TOT_M']*100
df['3female-percentage']=df['3Females']/dfcensus['TOT_F']*100
df['2male-percentage']=df['2M']/dfcensus['TOT_M']*100
df['2female-percentage']=df['2F']/dfcensus['TOT_F']*100
df['1male-percentage']=df['1Males']/dfcensus['TOT_M']*100
df['1female-percentage']=df['1Females']/dfcensus['TOT_F']*100

df['p-value']=0

for state in required.keys() :
    df.loc[df['State Code'] == state, "p-value"] = required[state]
    
df3=df[['State Code','3male-percentage','3female-percentage','p-value']]
df3.columns=['state-code','male-percentage','female-percentage','p-value']
df3.to_csv('Outputs/gender-india-c.csv',index=False)

df2=df[['State Code','2male-percentage','2female-percentage','p-value']]
df2.columns=['state-code','male-percentage','female-percentage','p-value']
df2.to_csv('Outputs/gender-india-b.csv',index=False)

df1=df[['State Code','1male-percentage','1female-percentage','p-value']]
df1.columns=['state-code','male-percentage','female-percentage','p-value']
df1.to_csv('Outputs/gender-india-a.csv',index=False)
