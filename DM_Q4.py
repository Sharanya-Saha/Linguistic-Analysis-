#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 23:59:48 2021

@author: sharanya
"""

import pandas as pd

df=pd.read_excel('Datasets/DDW-C18-0000.xlsx',engine='openpyxl')
df.columns=['State','District Code','Area','Total/Rural/Urban','Age Group','2Persons','2Males','2Females','3Persons','3Males','3Females']
df=df.drop([0,1,2,3,4])
df=df[['State','Total/Rural/Urban','Age Group','2Persons','3Persons']]
df=df.loc[df['Total/Rural/Urban']=='Total']
df=df.loc[df['State']!='00']
df=df.loc[df['Age Group']=='Total']
df.sort_values(by=['State'],inplace=True)
df=df.reset_index()
df=df[['State','2Persons','3Persons']]
df['2languages']=df['2Persons']-df['3Persons']
df['ratio']=df['3Persons']/df['2languages']
df.sort_values(by=['ratio'],inplace=True)
lower=list(df[0:3].State)
higher=list(df[-3:].State)
higher.reverse()
for ele in lower :
    higher.append(ele)
    
df1=pd.DataFrame(higher)
df1.columns=['state/ut']
df1.to_csv('Outputs/3-to-2-ratio.csv',index=False)