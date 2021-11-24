#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 21:32:53 2021

@author: sharanya
"""

import pandas as pd
df=pd.read_excel('Datasets/DDW-C18-0000.xlsx',engine='openpyxl')
df.columns=['State Code','District Code','Area','Total/Rural/Urban','Age Group','2Persons','2Males','2Females','3Persons','3Males','3Females']
df=df.drop([0,1,2,3,4])
df=df[['State Code','Total/Rural/Urban','Age Group','2Persons','3Persons']]
df=df.loc[df['Total/Rural/Urban']=='Total']
df=df.loc[df['Age Group']=='Total']


dfcensus=pd.read_excel('Datasets/DDW_PCA0000_2011_Indiastatedist.xlsx',engine='openpyxl')
dfcensus=dfcensus[['Level','State','TRU','TOT_P']]
dfcensus=dfcensus.loc[dfcensus['Level'] != 'DISTRICT']
dfcensus=dfcensus.loc[dfcensus['TRU']=='Total']


df.sort_values(by=['State Code'],inplace=True)
df=df.reset_index()
df=df[['State Code','2Persons','3Persons']]
dfcensus.sort_values(by=['State'],inplace=True)
dfcensus=dfcensus.reset_index()
dfcensus=dfcensus[['State','TOT_P']]

df['1language']=dfcensus['TOT_P']-df['2Persons']
df['2languages']=df['2Persons']-df['3Persons']
df['2languagespercentage']=(df['2languages']/dfcensus['TOT_P'])*100
df['1languagepercentage']=(df['1language']/dfcensus['TOT_P'])*100
df['3languagespercentage']=(df['3Persons']/dfcensus['TOT_P'])*100

df=df[['State Code','1languagepercentage','2languagespercentage','3languagespercentage']]
df.columns=['state-code','percent-one','percent-two','percent-three']
df.to_csv('Outputs/percent-india.csv',index=False)