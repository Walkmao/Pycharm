# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 16:04:21 2020

@author: Betty
"""

import os
import xlrd
import pandas as pd
import numpy as np

 
path = r'C:\\Users\\Betty\\Desktop\区政府个人报告2018'
total_data={}
j=0
filenames = os.listdir(path)
for filename in filenames:
    j+=1
    print(filename)
    data_all= pd.read_excel('C:\\Users\\Betty\\Desktop\区政府个人报告2018\\'+filename)
    
    dict={}
    
    name=data_all.iloc[0,4]
    identifier=data_all.iloc[0,1]
    dict["姓名"]=name
    dict["体检编号"]=identifier
   

    lenght=data_all.shape[0]

    for i in range(lenght):
        if data_all.iloc[i,0]=="身高":
            height=data_all.iloc[i,1]
            dict["身高"]=height
        if data_all.iloc[i,0]=="体重":
            weight=data_all.iloc[i,1]
            dict["体重"]=weight
        if data_all.iloc[i,0]=="血压（收缩压）":
            BP1=data_all.iloc[i,1]
            dict["血压（收缩压）"]=BP1
        if data_all.iloc[i,0]=="血压（舒张压）":
            BP2=data_all.iloc[i,1]
            dict["血压（舒张压）"]=BP2
        if data_all.iloc[i,0]=="HDL胆固醇(HDL-CH)":
            HDL=data_all.iloc[i,1]
            dict["HDL胆固醇"]=HDL
        if data_all.iloc[i,0]=="LDL胆固醇(LDL-CH)":
            LDL=data_all.iloc[i,1]
            dict["LDL胆固醇"]=LDL
        if data_all.iloc[i,0]=="谷草转氨酶(AST)":
            AST=data_all.iloc[i,1]
            dict["谷草转氨酶"]=AST
        if data_all.iloc[i,0]=="谷丙转氨酶(ALT)":
            ALT=data_all.iloc[i,1]
            dict["谷丙转氨酶"]=ALT
        if data_all.iloc[i,0]=="尿酸(UA)":
            UA=data_all.iloc[i,1]
            dict["尿酸"]=UA
        if data_all.iloc[i,0]=="甘油三脂(TRIG)":
            TRIG=data_all.iloc[i,1]
            dict["甘油三酯"]=TRIG
        if data_all.iloc[i,0]=="血清总胆固醇(CHOL)":
            CHOL=data_all.iloc[i,1]
            dict["总胆固醇"]=CHOL
        if data_all.iloc[i,0]=="空腹血糖(GLU)":
            GLU=data_all.iloc[i,1]
            dict["空腹葡萄糖"]=GLU
        if data_all.iloc[i,0]=="糖化血红蛋白(GHb)":
            GHb=data_all.iloc[i,1]
            dict["糖化血红蛋白"]=GHb
    total_data[str(j)]=dict


total_data_1=pd.DataFrame.from_dict(total_data,orient="index")
total_data_1.to_excel('E:\干保委\总数据.xlsx')
    
