#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 21:101:33 2023

@author: muthyala.7
"""

import FeatureSpaceConstruction
import SISSO_REGRESSOR_TORCH
import torch
import numpy as np 
import pandas as pd 
import time
import os 
from sklearn.model_selection import train_test_split

'''
###########################################################################################

Commented the file saving because the data is already collected with nice distribution, if want to benchmark then use the 
read the file and perform sisso

###############################################################################################
'''





'''
########################################################################################################

#CaseStudy - 1

#######################################################################################################
'''
x = [np.random.uniform(0,2,size=100) for i in range(5)]
df = pd.DataFrame()
for i in range(len(x)):
  variable = 'x'+str(i+1)
  df[variable] = x[i]
operators = ['+','/']
y = 10*((df.iloc[:,0])/(df.iloc[:,1]*(df.iloc[:,2]+df.iloc[:,3]))) + 3 + 0.01*np.random.normal(0,1,100)
df.insert(0,'Target',y)
train, test = train_test_split(df,test_size=0.9,random_state=18)
train = train.reset_index(drop=True)
test = test.reset_index(drop=True)
start = time.time()
fc = FeatureSpaceConstruction.feature_space_construction(operators,train,3,'cpu')
x,y,names= fc.feature_space()
print('Time taken to create feature space: ',time.time()-start,'seconds')

sr = SISSO_REGRESSOR_TORCH.SISSORegressor(x, y, names,1,20,'L0','cpu')
rmse,equation = sr.SISSO()
#sr = SISSORegressor.SISSO_Regressor(x,y,names,1,20,'cpu','L0')
#rmse, equation = sr.SISSO()
print('SISSO Completed',time.time()-start,'\n')
print(equation)
print('\n')

'''
os.chdir('/home/muthyala.7/TorchSisso/Case_Studies/1/')
df.to_csv('original.csv')
train.to_csv('train.csv')
test.to_csv('test.csv')
train.insert(0,'Index',train.index)
train.to_csv('train.dat',sep='\t',index=False)
test.to_csv('predict.dat',sep=' ')'''
'''
###############################################################################################

#CaseStudy -2 
###############################################################################################
'''
x = [np.random.uniform(0,2,size=100) for i in range(5)]
df = pd.DataFrame()
for i in range(len(x)):
  variable = 'x'+str(i+1)
  df[variable] = x[i]
y1 = 3*np.sqrt(df.iloc[:,1]) + 2.10*np.sin(df.iloc[:,2]) + 2.10 + 0.010*np.random.normal(0,1,100)
df.insert(0,'Target',y1)
operators = ['sqrt','sin']
train, test = train_test_split(df,test_size=0.9,random_state=18)
train = train.reset_index(drop=True)
test = test.reset_index(drop=True)
start_c = time.time()
FC = FeatureSpaceConstruction.feature_space_construction(operators, train,3,'cpu')
x,y,names= FC.feature_space()
print('Time taken to create feature space: ',time.time()-start_c,'seconds')
start = time.time()
sr = SISSO_REGRESSOR_TORCH.SISSORegressor(x,y,names,2,10,'L0','cpu')
rmse,equation = sr.SISSO()
print(time.time()-start)
print("SISSO Completed: ",time.time()-start_c,'\n')
print(equation,'\n')
import os 
'''
os.chdir('/home/muthyala.7/TorchSisso/Case_Studies/2/')
df.to_csv('original.csv')
train.to_csv('train.csv')
test.to_csv('test.csv')
train.insert(0,'Index',train.index)
train.to_csv('train.dat',sep='\t',index=False)
test.to_csv('predict.dat',sep=' ')
'''

'''
##########################################################################################################

#CaseStudy-3

#########################################################################################################
'''
x = [np.random.uniform(0,2,size=100) for i in range(4)]
df = pd.DataFrame()
for i in range(len(x)):
  variable = 'x'+str(i+1)
  df[variable] = x[i]
y2 = 3*(np.exp(df.iloc[:,3])/(df.iloc[:,2]+np.exp(df.iloc[:,1]))) + 0.01*np.random.normal(0,1,100)
df.insert(0,'Target',y2)
train, test = train_test_split(df,test_size=0.9,random_state=18)
train = train.reset_index(drop=True)
test = test.reset_index(drop=True)
operators = ['/','+','exp']
start_c = time.time()
FC = FeatureSpaceConstruction.feature_space_construction(operators, train,4,'cpu')
x,y,names= FC.feature_space()
print('Time taken to create feature space: ',time.time()-start_c,'seconds')
start = time.time()
sr = SISSO_REGRESSOR_TORCH.SISSORegressor(x,y,names,1,20,'cpu')
rmse, equation = sr.SISSO()

print("SISSO Completed: ",time.time()-start_c,'\n')
'''
os.chdir('/home/muthyala.7/TorchSisso/Case_Studies/3/')
df.to_csv('original.csv')
train.to_csv('train.csv')
test.to_csv('test.csv')
train.insert(0,'Index',train.index)
train.to_csv('train.dat',sep='\t',index=False)
test.to_csv('predict.dat',sep=' ')
'''


'''
##############################################################################################################

#CaseStudy 4

##############################################################################################################

'''
df = pd.read_csv('/home/muthyala.7/Downloads/NOMAD_TEST_FILE.csv')

operators = ['+','-','*','/']
start_c = time.time()
FC = FeatureSpaceConstruction.feature_space_construction(operators, df,3,'cpu')
x,y,names= FC.feature_space()
print('Time taken to create feature space: ',time.time()-start_c,'seconds')

sr = SISSO_REGRESSOR_TORCH.SISSORegressor(x,y,names,3,20,'L0','cpu')
rmse, equation = sr.SISSO()

print("SISSO Completed: ",time.time()-start_c,'\n')
print(equation,'\n')

'''
##########################################################################################################

#CaseStudy-5

#########################################################################################################
'''
x = [np.random.uniform(0,2,size=100) for i in range(10)]
df = pd.DataFrame()
for i in range(len(x)):
  variable = 'x'+str(i+1)
  df[variable] = x[i]
y2 = 3*df.iloc[:,0]**3 + 2*df.iloc[:,1]**2 - 3.5*(df.iloc[:,2]) - 2 + 0.01*np.random.normal(0,1,size=100)
df.insert(0,'Target',y2)
train, test = train_test_split(df,test_size=0.9,random_state=18)
train = train.reset_index(drop=True)
test = test.reset_index(drop=True)
operators = ['^3','^2']
start_c = time.time()
FC = FeatureSpaceConstruction.feature_space_construction(operators, train,3,'cpu')
x,y,names= FC.feature_space()
print('Time taken to create feature space: ',time.time()-start_c,'seconds')
sr = SISSO_REGRESSOR_TORCH.SISSORegressor(x,y,names,3,5,'L0','cpu')
rmse, equation =sr.SISSO()
#sr = SISSORegressor.SISSO_Regressor(x,y,names,3,5,'cpu')
#rmse, equation = sr.SISSO()
print("SISSO Completed: ",time.time()-start_c,'\n')
print(equation)
#os.mkdir('/home/muthyala.7/TorchSisso/Case_Studies/4')
'''
os.chdir('/home/muthyala.7/TorchSisso/Case_Studies/4/')
df.to_csv('original.csv')
train.to_csv('train.csv')
test.to_csv('test.csv')
train.insert(0,'Index',train.index)
train.to_csv('train.dat',sep='\t',index=False)
test.to_csv('predict.dat',sep=' ')

'''





