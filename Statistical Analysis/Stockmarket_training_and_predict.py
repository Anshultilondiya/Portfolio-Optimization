#!/usr/bin/env python
# coding: utf-8

# In[7]:


#Importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import keras
from yahoofinancials import YahooFinancials
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.models import Model
from keras.layers import Input
from keras.layers.merge import concatenate


# In[8]:


#Required functions
# Takes financial data from Yahoo Finance
def getdata_stock(companyname,start,end):
    df1=YahooFinancials(companyname)
    stat=df1.get_historical_price_data(start,end,'daily')
    return stat
# return array corresponding to particular value e.g high,low,closing,open etc 
def particular_data(companyname,parameter,stat):
    i=0
    prc=[]
    for date in stat[companyname]['prices']:
        if i==0:
            i+=1
            continue
        prc.append([date[parameter]])
        i+=1
    return prc
# fill missing data with average of two days
def removing_none(prc):
    for j in range(1,len(prc)-1):
        if prc[j][0]==None or prc[j][0]<=5:
            if prc[j+1][0]==None:
                prc[j][0]=prc[j-1][0]
            else:
                prc[j][0]=(prc[j-1][0]+prc[j+1][0])/2
    return prc
#scalled the data for model
def scaling(arr,frange):
    sc=MinMaxScaler(feature_range=frange)
    arr=sc.fit_transform(arr)
    return arr


# In[20]:


def Statistical_training(company,start_date,end_date):
    company=company 
    stat=getdata_stock(company,start_date,end_date)
    # get the arrays corresponding to each data
    close=removing_none(particular_data(company,'close',stat))
    volume=removing_none(particular_data(company,'volume',stat))
    high=removing_none(particular_data(company,'high',stat))
    low=removing_none(particular_data(company,'low',stat))
    #scalling the data
    close=scaling(close,(0,1))
    volume=scaling(volume,(0,1))
    high=scaling(high,(0,1))
    low=scaling(low,(0,1))
    #Taking last 50 days data for each y_train
    x_train1=[]
    x_train2=[]
    x_train3=[]
    x_train4=[]
    y_train=[]
    for i in range(50,len(close)):
        x_train1.append(close[i-50:i,0])
        y_train.append(close[i,0])
    for i in range(50,len(volume)):
        x_train2.append(volume[i-50:i,0])
    for i in range(50,len(high)):
        x_train3.append(high[i-50:i,0])
    for i in range(50,len(low)):
        x_train4.append(low[i-50:i,0])
    #converting into required shape for model
    x_train1=np.array(x_train1)
    x_train2=np.array(x_train2)
    x_train3=np.array(x_train3)
    x_train4=np.array(x_train4)
    x_train1=x_train1.reshape(x_train1.shape[0],x_train1.shape[1],1)
    x_train2=x_train2.reshape(x_train2.shape[0],x_train2.shape[1],1)
    x_train3=x_train3.reshape(x_train3.shape[0],x_train3.shape[1],1)
    x_train4=x_train4.reshape(x_train4.shape[0],x_train4.shape[1],1)
    #creating model
    input1=Input(shape=(x_train1.shape[1],1))
    hidden1=LSTM(units=100,return_sequences=True,activation='relu')(input1)
    hidden2=Dropout(0.1)(hidden1)
    hidden3=LSTM(units=50,return_sequences=True,activation='relu')(hidden2)
    hidden4=Dropout(0.1)(hidden3)
    hidden5=LSTM(units=32,return_sequences=True,activation='relu')(hidden4)
    hidden6=Dropout(0.1)(hidden5)
    hidden7=LSTM(units=16,activation='relu')(hidden6)

    input2=Input(shape=(x_train2.shape[1],1))
    hidden1a=LSTM(units=100,return_sequences=True,activation='relu')(input2)
    hidden2a=Dropout(0.1)(hidden1a)
    hidden3a=LSTM(units=50,return_sequences=True,activation='relu')(hidden2a)
    hidden4a=Dropout(0.1)(hidden3a)
    hidden5a=LSTM(units=32,return_sequences=True,activation='relu')(hidden4a)
    hidden6a=Dropout(0.1)(hidden5a)
    hidden7a=LSTM(units=16,activation='relu')(hidden6a)

    input3=Input(shape=(x_train3.shape[1],1))
    hidden1b=LSTM(units=100,return_sequences=True,activation='relu')(input3)
    hidden2b=Dropout(0.1)(hidden1b)
    hidden3b=LSTM(units=50,return_sequences=True,activation='relu')(hidden2b)
    hidden4b=Dropout(0.1)(hidden3b)
    hidden5b=LSTM(units=32,return_sequences=True,activation='relu')(hidden4b)
    hidden6b=Dropout(0.1)(hidden5b)
    hidden7b=LSTM(units=16,activation='relu')(hidden6b)

    input4=Input(shape=(x_train4.shape[1],1))
    hidden1c=LSTM(units=100,return_sequences=True,activation='relu')(input4)
    hidden2c=Dropout(0.1)(hidden1c)
    hidden3c=LSTM(units=50,return_sequences=True,activation='relu')(hidden2c)
    hidden4c=Dropout(0.1)(hidden3c)
    hidden5c=LSTM(units=32,return_sequences=True,activation='relu')(hidden4c)
    hidden6c=Dropout(0.1)(hidden5c)
    hidden7c=LSTM(units=16,activation='relu')(hidden6c)

    merge=concatenate([hidden7 ,hidden7a, hidden7b, hidden7c])
    layer1=Dense(units=50,activation='relu')(merge)
    layer2=Dropout(0.1)(layer1)
    layer3=Dense(units=50,activation='relu')(layer2)
    layer4=Dropout(0.1)(layer3)
    layer5=Dense(units=50,activation='relu')(layer4)
    layer6=Dropout(0.1)(layer5)
    layer7=Dense(units=50,activation='relu')(layer6)
    layer8=Dropout(0.1)(layer7)
    layer9=Dense(units=50,activation='relu')(layer8)
    output=Dense(units=1,activation='sigmoid')(layer9)
    model=Model(inputs=[input1,input2,input3,input4],outputs=output)
    #complie and fit model
    model.compile(optimizer='adam',loss='mse')
    model.fit([x_train1,x_train2,x_train3,x_train4],y_train,epochs=50,batch_size=32)
    return model


# In[21]:


model=Statistical_training('TCS.NS','2013-01-01','2020-01-01')


# In[35]:


def Predict(company,today_date,model):
    model=model
    today_date1=today_date.split('-')
    start_date= str(int(today_date1[0])-1)+'-'+today_date1[1]+'-'+today_date1[2]
    end_date=today_date
    stat1=getdata_stock(company,start_date,end_date)
    close1=removing_none(particular_data(company,'close',stat1))
    volume1=removing_none(particular_data(company,'volume',stat1))
    high1=removing_none(particular_data(company,'high',stat1))
    low1=removing_none(particular_data(company,'low',stat1))
    #scalling the data
    sc1=MinMaxScaler((0,1))
    close1=sc1.fit_transform(close1)
    volume1=scaling(volume1,(0,1))
    high1=scaling(high1,(0,1))
    low1=scaling(low1,(0,1))
    #Taking last 50 days data for each y_test
    x_test1=[]
    x_test2=[]
    x_test3=[]
    x_test4=[]
    x_test1.append(close1[len(close1)-50:len(close1),0])
    x_test2.append(volume1[len(volume1)-50:len(volume1),0])
    x_test3.append(high1[len(high1)-50:len(high1),0])
    x_test4.append(low1[len(low1)-50:len(low1),0])
    #converting into required shape for model
    x_test1=np.array(x_test1)
    x_test2=np.array(x_test2)
    x_test3=np.array(x_test3)
    x_test4=np.array(x_test4)
    x_test1=x_test1.reshape(x_test1.shape[0],x_test1.shape[1],1)
    x_test2=x_test2.reshape(x_test2.shape[0],x_test2.shape[1],1)
    x_test3=x_test3.reshape(x_test3.shape[0],x_test3.shape[1],1)
    x_test4=x_test4.reshape(x_test4.shape[0],x_test4.shape[1],1)
    predictions=model.predict([x_test1,x_test2,x_test3,x_test4])
    predictions1=sc1.inverse_transform(predictions)    
    print('The Next Day closing price of'+'  '+ company+' is'+'  '+str(predictions1[0][0]))


# In[36]:


Predict('TCS.NS','2020-06-23',model)


# In[ ]:




