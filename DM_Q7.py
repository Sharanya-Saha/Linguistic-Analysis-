#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 00:48:54 2021

@author: sharanya
"""

import os
import pandas as pd

output=[]
output1=[]
filename={}
CSV=[]
regions=['North','West','Central','East','South','NorthEast']
for region in regions :
    csvs = os.listdir(f"Datasets/{region}")
    #csvs = [f"Datasets/{region}/{x}" for x in csvs]
    for x in csvs :
        filename[f"Datasets/{region}/{x}"]=x
        CSV.append(f"Datasets/{region}/{x}")
    region_df=pd.DataFrame(columns=["lang","person"])
    region1_df=pd.DataFrame(columns=["lang","person"])
    for file in CSV :
        print(file)
        print(filename[file])
        df=pd.read_excel(file, engine="openpyxl")
        df.rename(columns={"Unnamed: 3":"lang1", "Unnamed: 4":"person1","Unnamed: 8":"lang2", "Unnamed: 9":"person2","Unnamed: 13":"lang3", "Unnamed: 14":"person3"},inplace=True)
        columns = ["lang1","person1","lang2","person2","lang3","person3"]
        df = df[columns]
        df = df.drop([0,1,2,3])
        l1 = df[["lang1", "person1"]]
        l1=l1.dropna()
        l1.columns = ["lang","person"]
        region_df=region_df.append(l1)
        region1_df=region1_df.append(l1)
        l2 = df[["lang2", "person2"]]
        l2=l2.dropna()
        l2.columns = ["lang","person"]
        region_df=region_df.append(l2)
        l3 = df[["lang3", "person3"]]
        l3=l3.dropna()
        l3.columns = ["lang","person"]
        region_df=region_df.append(l3)
    
    region_df=pd.DataFrame({'person':region_df.groupby(['lang'])['person'].sum()}).reset_index()
    region_df = region_df.sort_values(by="person", ascending=False)
    top3=list(region_df[0:3].lang)
    output.append([region]+top3)
    
    region1_df=pd.DataFrame({'person':region1_df.groupby(['lang'])['person'].sum()}).reset_index()
    region1_df = region1_df.sort_values(by="person", ascending=False)
    top_3=list(region1_df[0:3].lang)
    output1.append([region]+top_3)
    
dff = pd.DataFrame(output, columns =["region","language-1","language-2","language-3"])
dff.loc[dff.region == "NorthEast" , "region"] = "North-East"
dff.sort_values(by=['region'],inplace=True)
dff.to_csv('Outputs/region-india-b.csv',index=False)

dff1 = pd.DataFrame(output1, columns =["region","language-1","language-2","language-3"])
dff1.loc[dff1.region == "NorthEast" , "region"] = "North-East"
dff1.sort_values(by=['region'],inplace=True)
dff1.to_csv('Outputs/region-india-a.csv',index=False)
