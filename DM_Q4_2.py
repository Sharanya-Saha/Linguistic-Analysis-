#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 00:37:06 2021

@author: sharanya
"""

import pandas as pd
df=pd.read_excel('Datasets/DDW-C18-0000.xlsx',engine='openpyxl')
df.columns=['Area','District Code','State Code','Total/Rural/Urban','Age Group','2Persons','2Males','2Females','3Persons','3Males','3Females']
df=df.drop([0,1,2,3,4])
df=df[['Area','Total/Rural/Urban','Age Group','2Persons','3Persons']]
df=df.loc[df['Total/Rural/Urban']=='Total']
df=df.loc[df['Area']!='00']
df=df.loc[df['Age Group']=='Total']


dfcensus=pd.read_excel('Datasets/DDW_PCA0000_2011_Indiastatedist.xlsx',engine='openpyxl')
dfcensus=dfcensus[['Level','State','TRU','TOT_P']]
dfcensus=dfcensus.loc[dfcensus['Level']=='STATE']
dfcensus=dfcensus.loc[dfcensus['TRU']=='Total']


df.sort_values(by=['Area'],inplace=True)
df=df.reset_index()
df=df[['Area','2Persons','3Persons']]
dfcensus.sort_values(by=['State'],inplace=True)
dfcensus=dfcensus.reset_index()
dfcensus=dfcensus[['State','TOT_P']]

df['1language']=dfcensus['TOT_P']-df['2Persons']
df['2languages']=df['2Persons']-df['3Persons']
df['ratio']=df['2languages']/df['1language']

df.sort_values(by=['ratio'],inplace=True)
lower=list(df[0:3].Area)
higher=list(df[-3:].Area)

higher.reverse()
for ele in lower :
    higher.append(ele)
    
df1=pd.DataFrame(higher)
df1.columns=['state/ut']
df1.to_csv('Outputs/2-to-1-ratio.csv',index=False)