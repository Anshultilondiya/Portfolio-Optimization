CompanyName = 'TCS'
TodaysDate = '2020-07-25'

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import keras
from yahoofinancials import YahooFinancials
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

out = ''
i = 0
while TodaysDate[i] != '-':
    out = out + TodaysDate[i]
    i = i+1
out = str(int(out) - 1)
out = out +'-'
for i in range(5,len(TodaysDate)):
    out = out + TodaysDate[i]
  
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
    
company = CompanyName + '.NS'
stat=getdata_stock(company,out,TodaysDate)

close=removing_none(particular_data(company,'close',stat))
volume=removing_none(particular_data(company,'volume',stat))
high=removing_none(particular_data(company,'high',stat))
low=removing_none(particular_data(company,'low',stat))

sc1 = MinMaxScaler((0,1))
sc2 = MinMaxScaler((0,1))
sc3 = MinMaxScaler((0,1))
sc4 = MinMaxScaler((0,1))
close = sc1.fit_transform(close)
volume = sc2.fit_transform(volume)
high = sc3.fit_transform(high)
low = sc4.fit_transform(low)

x_test1 = []
x_test2 = []
x_test3 = []
x_test4 = []
y_test1 = []
y_test2 = []
y_test3 = []
y_test4 = []

for i in range(len(close)-1,len(close)):
    x_test1.append(close[i-50:i,0])
    y_test1.append(close[i,0])
for i in range(len(volume)-1,len(volume)):
    x_test2.append(volume[i-50:i,0])
    y_test2.append(volume[i,0])
for i in range(len(high)-1,len(high)):
    x_test3.append(high[i-50:i,0])
    y_test3.append(high[i,0])
for i in range(len(low)-1,len(low)):
    x_test4.append(low[i-50:i,0])
    y_test4.append(low[i,0])
    
x_test1=np.array(x_test1)
x_test2=np.array(x_test2)
x_test3=np.array(x_test3)
x_test4=np.array(x_test4)
y_test1 = np.array(y_test1)
y_test2 = np.array(y_test2)
y_test3 = np.array(y_test3)
y_test4 = np.array(y_test4)
x_test1=x_test1.reshape(x_test1.shape[0],x_test1.shape[1],1)
x_test2=x_test2.reshape(x_test2.shape[0],x_test2.shape[1],1)
x_test3=x_test3.reshape(x_test3.shape[0],x_test3.shape[1],1)
x_test4=x_test4.reshape(x_test4.shape[0],x_test4.shape[1],1)

Close = []
Volume = []
High = []
Low = []

for i in range(len(close)-50,len(close)):
    Close.append([close[i,0]])
    Volume.append([volume[i,0]])
    High.append([high[i,0]])
    Low.append([low[i,0]])
    
ClosedPriceFile = CompanyName + 'ClosedPrice.h5'
VolumeFile = CompanyName + 'Volume.h5'
HighFile = CompanyName + 'High.h5'
LowFile = CompanyName + 'Low.h5'

modelForClosedPrice = load_model(ClosedPriceFile)

modelForVolume = load_model(VolumeFile)

modelForHigh = load_model(HighFile)

modelForLow = load_model(LowFile)

predictedClose = []
predictedVolume = []
predictedHigh = []
predictedLow = []

count = 0
while count<10:
    prediction1 = modelForClosedPrice.predict([x_test1,x_test2,x_test3,x_test4])
    predictedClose.append(sc1.inverse_transform(prediction1))
    prediction2 = modelForVolume.predict([x_test1,x_test2,x_test3,x_test4])
    predictedVolume.append(sc2.inverse_transform(prediction2))
    prediction3 = modelForHigh.predict([x_test1,x_test2,x_test3,x_test4])
    predictedHigh.append(sc3.inverse_transform(prediction3))
    prediction4 = modelForLow.predict([x_test1,x_test2,x_test3,x_test4])
    predictedLow.append(sc4.inverse_transform(prediction4))
    
    x_test1 = []
    x_test2 = []
    x_test3 = []
    x_test4 = []
    
    Close.append([prediction1])
    Volume.append([prediction2])
    High.append([prediction3])
    Low.append([prediction4])
    
    for i in range(len(Close)-50,len(Close)):
        x_test1.append([Close[i]])
        x_test2.append([Volume[i]])
        x_test3.append([High[i]])
        x_test4.append([Low[i]])
         

    x_test1 = np.array(x_test1)
    x_test1=x_test1.reshape(x_test1.shape[1],x_test1.shape[0],1)
    
    x_test2 = np.array(x_test2)
    x_test2=x_test2.reshape(x_test2.shape[1],x_test2.shape[0],1)

    
    x_test3 = np.array(x_test3)
    x_test3=x_test3.reshape(x_test3.shape[1],x_test3.shape[0],1)

    x_test4= np.array(x_test4)
    x_test4 =x_test4.reshape(x_test4.shape[1],x_test4.shape[0],1)
    
    count = count+1
    
 for i in range(0,10):
    print('Day' + str(i+1))
    print('ClosingPrice', end= '  :  ')
    print(predictedClose[i][0][0])
    print('Volume', end = '  :  ')
    print(predictedVolume[i][0][0])
    print('High', end = '  :  ')
    print(predictedHigh[i][0][0])
    print('Low', end = '  :  ')
    print(predictedLow[i][0][0])
    print()
