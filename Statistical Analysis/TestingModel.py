CompanyName = 'TCS'

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

def getdata_stock(companyname,start,end):
    df1=YahooFinancials(companyname)
    stat=df1.get_historical_price_data(start,end,'daily')
    return stat
    
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
    
def removing_none(prc):
    for j in range(1,len(prc)-1):
        if prc[j][0]==None or prc[j][0]<=5:
            if prc[j+1][0]==None:
                prc[j][0]=prc[j-1][0]
            else:
                prc[j][0]=(prc[j-1][0]+prc[j+1][0])/2
    return prc
  
def scaling(arr,frange):
    sc=MinMaxScaler(feature_range=frange)
    arr=sc.fit_transform(arr)
    return arr
    
 def CreatingModel(x_train1,x_train2,x_train3,x_train4,y_train):
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
    model =Model(inputs=[input1,input2,input3,input4],outputs=output)
    model.compile(optimizer='adam',loss='mse')
    model.fit([x_train1,x_train2,x_train3,x_train4],y_train,epochs=100,batch_size=32)
    
    return model
    
company = CompanyName + '.NS' 
stat=getdata_stock(company,'2013-01-1','2019-12-31')

close=removing_none(particular_data(company,'close',stat))
volume=removing_none(particular_data(company,'volume',stat))
high=removing_none(particular_data(company,'high',stat))
low=removing_none(particular_data(company,'low',stat))

close=scaling(close,(0,1))
volume=scaling(volume,(0,1))
high=scaling(high,(0,1))
low=scaling(low,(0,1))

x_train1 = []
x_train2 = []
x_train3 = []
x_train4 = []
y_train1 = []
y_train2 = []
y_train3 = []
y_train4 = []

for i in range(50,len(close)):
    x_train1.append(close[i-50:i,0])
    y_train1.append(close[i,0])
for i in range(50,len(volume)):
    x_train2.append(volume[i-50:i,0])
    y_train2.append(volume[i,0])
for i in range(50,len(high)):
    x_train3.append(high[i-50:i,0])
    y_train3.append(high[i,0])
for i in range(50,len(low)):
    x_train4.append(low[i-50:i,0])
    y_train4.append(low[i,0])
    
x_train1=np.array(x_train1)
x_train2=np.array(x_train2)
x_train3=np.array(x_train3)
x_train4=np.array(x_train4)
y_train1 = np.array(y_train1)
y_train2 = np.array(y_train2)
y_train3 = np.array(y_train3)
y_train4 = np.array(y_train4)
x_train1=x_train1.reshape(x_train1.shape[0],x_train1.shape[1],1)
x_train2=x_train2.reshape(x_train2.shape[0],x_train2.shape[1],1)
x_train3=x_train3.reshape(x_train3.shape[0],x_train3.shape[1],1)
x_train4=x_train4.reshape(x_train4.shape[0],x_train4.shape[1],1)

ClosedPriceFile = ComapnyName + 'ClosedPrice.h5'
VolumeFile = ComapnyName + 'Volume.h5'
HighFile = CompanyName + 'High.h5'
LowFile = CompanyName + 'Low.h5'

modelForClosedPrice = CreatingModel(x_train1,x_train2,x_train3,x_train4,y_train1)

modelForClosedPrice.save(ClosedPriceFile)
print('model saved')

modelForVolume = CreatingModel(x_train1,x_train2,x_train3,x_train4,y_train2)

modelForVolume.save(VolumeFile)
print('model saved')

modelForHigh = CreatingModel(x_train1,x_train2,x_train3,x_train4,y_train3)

modelForHigh.save(HighFile)
print('model saved')

modelForLow = CreatingModel(x_train1,x_train2,x_train3,x_train4,y_train4)

modelForLow.save(LowFile)
print('model saved')
