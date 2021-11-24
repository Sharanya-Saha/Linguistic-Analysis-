#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 10:54:49 2021

@author: sharanya
"""

import pandas as pd
pd.options.mode.chained_assignment = None
from scipy.stats import ttest_ind
df=pd.read_excel('Datasets/DDW-C18-0000.xlsx',engine='openpyxl')
df.columns=['State Code','District Code','Area','Total/Rural/Urban','Age Group','2Persons','2Males','2Females','3Persons','3Males','3Females']
df=df.drop([0,1,2,3,4])
df=df[['State Code','Total/Rural/Urban','Age Group','2Persons','3Persons']]
dfrural=df.loc[df['Total/Rural/Urban']=='Rural']
dfrural=dfrural.loc[dfrural['Age Group']=='Total']

dfurban=df.loc[df['Total/Rural/Urban']=='Urban']
dfurban=dfurban.loc[dfurban['Age Group']=='Total']

dfrural.rename(columns = {'3Persons': '3Rural_Persons'}, inplace = True)
dfurban.rename(columns = {'3Persons': '3Urban_Persons'}, inplace = True)
dfrural.rename(columns = {'2Persons': '2Rural_Persons'}, inplace = True)
dfurban.rename(columns = {'2Persons': '2Urban_Persons'}, inplace = True)
dfrural.sort_values(by=['State Code'],inplace=True)
dfrural=dfrural.reset_index()
dfurban.sort_values(by=['State Code'],inplace=True)
dfurban=dfurban.reset_index()
dfrural['3Urban_Persons']=dfurban['3Urban_Persons']
dfrural['2Urban_Persons']=dfurban['2Urban_Persons']
dff=dfrural[['State Code','2Rural_Persons','2Urban_Persons','3Rural_Persons','3Urban_Persons']]

dfcensus=pd.read_excel('Datasets/DDW_PCA0000_2011_Indiastatedist.xlsx',engine='openpyxl')
dfcensus=dfcensus[['Level','State','TRU','TOT_P']]
dfcensus=dfcensus.loc[dfcensus['Level']!='DISTRICT']
dfcrural=dfcensus.loc[dfcensus['TRU']=='Rural']
dfcurban=dfcensus.loc[dfcensus['TRU']=='Urban']

dfcrural.rename(columns = {'TOT_P': 'Rural_Pop'}, inplace = True)
dfcurban.rename(columns = {'TOT_P': 'Urban_Pop'}, inplace = True)
dfcrural.sort_values(by=['State'],inplace=True)
dfcrural=dfcrural.reset_index()
dfcurban.sort_values(by=['State'],inplace=True)
dfcurban=dfcurban.reset_index()
dfcrural['Urban_Pop']=dfcurban['Urban_Pop']
dffcensus=dfcrural[['State','Rural_Pop','Urban_Pop']]

dff['Urban_Pop']=dffcensus['Urban_Pop']
dff['Rural_Pop']=dffcensus['Rural_Pop']

dff['1Rural_Persons']=dff['Rural_Pop']-dff['2Rural_Persons']
dff['1Urban_Persons']=dff['Urban_Pop']-dff['2Urban_Persons']
dff['o2Rural_Persons']=dff['2Rural_Persons']-dff['3Rural_Persons']
dff['o2Urban_Persons']=dff['2Urban_Persons']-dff['3Urban_Persons']


def cal_pval(ratio, background) :
    t, p = ttest_ind(ratio, background,equal_var=False)
    return p

required={}
for state in list(dff['State Code']) :
    #print(state)
    state_df=dff[dff['State Code']==state]
    ratio=[]
    ratio.append(float(state_df['1Urban_Persons']/state_df['1Rural_Persons']))
    ratio.append(float(state_df['o2Urban_Persons']/state_df['o2Rural_Persons']))
    ratio.append(float(state_df['3Urban_Persons']/state_df['3Rural_Persons']))
    state_df1=dffcensus[dffcensus['State']==int(state)]
    background=state_df1['Urban_Pop']/state_df1['Rural_Pop']
    bg=[background]*3
    required[state]=cal_pval(ratio,bg)
    

dff['3urban-percentage']=dff['3Urban_Persons']/dff['Urban_Pop']*100
dff['3rural-percentage']=dff['3Rural_Persons']/dff['Rural_Pop']*100
dff['2urban-percentage']=dff['o2Urban_Persons']/dff['Urban_Pop']*100
dff['2rural-percentage']=dff['o2Rural_Persons']/dff['Rural_Pop']*100
dff['1urban-percentage']=dff['1Urban_Persons']/dff['Urban_Pop']*100
dff['1rural-percentage']=dff['1Rural_Persons']/dff['Rural_Pop']*100

dff['p-value']=0

for state in required.keys() :
    dff.loc[dff['State Code'] == state, "p-value"] = required[state]
    
    
dff3=dff[['State Code','3urban-percentage','3rural-percentage','p-value']]
dff3.columns=['state-code','urban-percentage','rural-percentage','p-value']
dff3.to_csv('Outputs/geography-india-c.csv',index=False)

dff2=dff[['State Code','2urban-percentage','2rural-percentage','p-value']]
dff2.columns=['state-code','urban-percentage','rural-percentage','p-value']
dff2.to_csv('Outputs/geography-india-b.csv',index=False)

dff1=dff[['State Code','1urban-percentage','1rural-percentage','p-value']]
dff1.columns=['state-code','urban-percentage','rural-percentage','p-value']
dff1.to_csv('Outputs/geography-india-a.csv',index=False)
