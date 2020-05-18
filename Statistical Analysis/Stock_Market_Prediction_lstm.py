#Importing the essential libraries
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

#Collecting data from yahoofinancials by giving appropiate time interval 
df1=YahooFinancials('RELIANCE.NS')
stat=df1.get_historical_price_data('2019-05-15','2020-05-15','daily')
#store a closing price in 2-D array 'prc'
i=0
prc=[]
for date in stat['RELIANCE.NS']['prices']:
    if i==0:
        i+=1
        continue
    prc.append([date['close']])
    i+=1

#Data preprocessing:If data for particular day is missing then it is replaced by avg of previous and next day values
for j in range(1,len(prc)-1):
    if prc[j][0]==None or prc[j][0]<10:
        if prc[j+1][0]=='nan' or prc[j+1][0]<10:
            prc[j][0]=prc[j-1][0]
        else:
            prc[j][0]=(prc[j-1][0]+prc[j+1][0])//2

#Store last 30 days data in prc1
prc1=prc[len(prc)-30:]

#Conversion of closing price data into feature range(0,1)
sc=MinMaxScaler()
X_scaled=sc.fit_transform(prc)
x_train=[]
y_train=[]

#Storing last 30 days data in x_train for each day in time interval
for i in range(30,len(prc)):
    x_train.append(X_scaled[i-30:i,0])
    y_train.append(X_scaled[i,0])

#As LSTM used 3d input,conversion of x_train into that dimensions
x_train=np.array(x_train)
y_train=np.array(y_train)
x_train=x_train.reshape(x_train.shape[0],x_train.shape[1],1)

#Adding LSTM and Dropout layers to the model
regressor=Sequential()
regressor.add(LSTM(units=50,return_sequences=True,input_shape=(x_train.shape[1],1)))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=50,return_sequences=True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=50,return_sequences=True))
regressor.add(Dropout(0.2))
regressor.add(LSTM(units=50))
regressor.add(Dropout(0.2))
regressor.add(Dense(units=1))

#Fitting the training data into model
regressor.compile(optimizer='adam',loss='mean_squared_error')
regressor.fit(x_train,y_train,epochs=100,batch_size=32)

#Scaling the test data and converting it into required dimensions
validator=np.array(prc1)
validator=validator.reshape(-1,1)
validator=sc.transform(validator)
x_test=[]
for i in range(30,31):
    x_test.append(validator[i-30:i,0])
x_test=np.array(x_test)
x_test=x_test.reshape(x_test.shape[0],x_test.shape[1],1)

#Predicting value of next day closing price
predictions=regressor.predict(x_test)
predictions=sc.inverse_transform(predictions)
print(predictions)


