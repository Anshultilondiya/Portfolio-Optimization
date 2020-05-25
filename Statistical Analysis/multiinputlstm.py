#!/usr/bin/env python
# coding: utf-8

# In[62]:


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


# In[63]:


df1=YahooFinancials('RELIANCE.NS')
stat=df1.get_historical_price_data('2014-05-15','2019-05-15','daily')
stat


# In[64]:


i=0
prc=[]
for date in stat['RELIANCE.NS']['prices']:
    if i==0:
        i+=1
        continue
    prc.append([date['close']])
    i+=1
i=0
vlm=[]
for date in stat['RELIANCE.NS']['prices']:
    if i==0:
        i+=1
        continue
    vlm.append([date['volume']])
    i+=1
i=0
typ=[]
for date in stat['RELIANCE.NS']['prices']:
    if i==0:
        i+=1
        continue
    typ.append([date['high'],date['low'],date['close']])
    i+=1


# In[65]:


for j in range(1,len(prc)-1):
    if prc[j][0]==None:
        if prc[j+1][0]==None:
            prc[j][0]=prc[j-1][0]
        else:
            prc[j][0]=(prc[j-1][0]+prc[j+1][0])/2
for j in range(1,len(vlm)-1):
    if vlm[j][0]==None:
        if vlm[j+1][0]==None:
            vlm[j][0]=vlm[j-1][0]
        else:
            vlm[j][0]=(vlm[j-1][0]+vlm[j+1][0])/2
for i in range(1,len(typ)-1):
    for j in range(0,len(typ[0])):
        if typ[i][j]==None:
            if typ[i+1][j]==None:
                typ[i][j]=typ[i-1][j]
            else:
                typ[i][j]=(typ[i-1][j]+typ[i+1][j])/2


# In[66]:


closing_chg=[]
for i in range(1,len(prc)):
    closing_chg.append([prc[i][0]-prc[i-1][0]])
closing_chg


# In[67]:


typ1=[]
for i in range(0,len(typ)):
    typ1.append(sum(typ[i])*vlm[i][0])


# In[68]:


typ2=[]
for j in range(1,len(typ1)):
    typ2.append(typ1[j]-typ1[j-1])


# In[69]:


mf=[]
for i in range(60,len(typ2)):
    pf=0
    nf=0
    for j in range(i-14,i):
        if typ2[j]>=0:
            pf=pf+typ2[j]
        else:
            nf=nf+typ2[j]
    mf1=100-(100/(1+(pf/nf)))
    mf.append([mf1])


# In[70]:


sc=MinMaxScaler()
X_scaled=sc.fit_transform(closing_chg)


# In[71]:


st=MinMaxScaler(feature_range=(0,1))
Mf_scaled=st.fit_transform(mf)


# In[72]:


x_train1=[]
x_train2=[]
y_train=[]
for i in range(60,len(closing_chg)):
    x_train1.append(X_scaled[i-60:i,0])
    x_train2.append(Mf_scaled[i-60][0])
    y_train.append(X_scaled[i][0])
x_train1=np.array(x_train1)
x_train2=np.array(x_train2)
x_train1=x_train1.reshape(x_train1.shape[0],x_train1.shape[1],1)
x_train2=x_train2.reshape(x_train2.shape[0],1,1)
y_train=np.array(y_train)


# In[73]:


x_train2.shape


# In[74]:


input1=Input(shape=(x_train1.shape[1],1))
hidden1=LSTM(units=50,return_sequences=True,dropout=0.2,activation='relu')(input1)
hidden2=LSTM(units=50,return_sequences=True,dropout=0.2,activation='relu')(hidden1)
hidden3=LSTM(units=50,return_sequences=True,dropout=0.2,activation='relu')(hidden2)
hidden4=LSTM(units=50,dropout=0.2,activation='relu')(hidden3)
input2=Input(shape=(x_train2.shape[1],1))
hiddena1=LSTM(units=50,return_sequences=True,dropout=0.2,activation='relu')(input2)
hiddena2=LSTM(units=50,return_sequences=True,dropout=0.2,activation='relu')(hiddena1)
hiddena3=LSTM(units=50,return_sequences=True,dropout=0.2,activation='relu')(hiddena2)
hiddena4=LSTM(units=50,dropout=0.2,activation='relu')(hiddena3)
merge=concatenate([hidden4 ,hiddena4])
layer1=Dense(units=10,activation='relu')(merge)
layer2=Dense(units=10,activation='relu')(layer1)
output=Dense(units=1,activation='sigmoid')(layer2)
model=Model(inputs=[input1,input2],outputs=output)


# In[105]:


model.compile(optimizer='rmsprop',loss='mse')
model.fit([x_train1,x_train2],y_train,epochs=100,batch_size=32)


# In[94]:


stat1=df1.get_historical_price_data('2019-06-15','2020-05-15','daily')
i=0
prc1=[]
for date in stat1['RELIANCE.NS']['prices']:
    if i==0:
        i+=1
        continue
    prc1.append([date['close']])
    i+=1
i=0
vlm1=[]
for date in stat1['RELIANCE.NS']['prices']:
    if i==0:
        i+=1
        continue
    vlm1.append([date['volume']])
    i+=1
i=0
typa=[]
for date in stat1['RELIANCE.NS']['prices']:
    if i==0:
        i+=1
        continue
    typa.append([date['high'],date['low'],date['close']])
    i+=1


# In[95]:


for j in range(1,len(prc1)-1):
    if prc1[j][0]==None:
        if prc1[j+1][0]==None:
            prc1[j][0]=prc1[j-1][0]
        else:
            prc1[j][0]=(prc1[j-1][0]+prc1[j+1][0])/2
for j in range(1,len(vlm1)-1):
    if vlm1[j][0]==None:
        if vlm1[j+1][0]==None:
            vlm1[j][0]=vlm1[j-1][0]
        else:
            vlm1[j][0]=(vlm1[j-1][0]+vlm1[j+1][0])/2
for i in range(1,len(typa)-1):
    for j in range(0,len(typa[0])):
        if typa[i][j]==None:
            if typa[i+1][j]==None:
                typa[i][j]=typa[i-1][j]
            else:
                typa[i][j]=(typa[i-1][j]+typa[i+1][j])/2


# In[96]:


closing_chg1=[]
for i in range(1,len(prc1)):
    closing_chg1.append([prc1[i][0]-prc1[i-1][0]])
typa1=[]
for i in range(0,len(typa)):
    typa1.append(sum(typa[i])*vlm1[i][0])
typa2=[]
for j in range(1,len(typa1)):
    typa2.append(typa1[j]-typa1[j-1])
mfa=[]
for i in range(60,len(typa2)):
    pf=0
    nf=0
    for j in range(i-14,i):
        if typa2[j]>=0:
            pf=pf+typa2[j]
        else:
            nf=nf+typa2[j]
    mf1=100-(100/(1+(pf/nf)))
    mfa.append([mf1])


# In[104]:


validator=sc.transform(closing_chg1)
x_test1=[]
x_test2=[]
Mf_scaled2=st.fit_transform(mfa)
for i in range(60,len(validator)):
    x_test1.append(validator[i-60:i,0])
    x_test2.append(Mf_scaled2[i-60][0])
x_test1=np.array(x_test1)
x_test2=np.array(x_test2)
x_test1=x_test1.reshape(x_test1.shape[0],x_test1.shape[1],1)
x_test2=x_test2.reshape(x_test2.shape[0],1,1)
predictions=model.predict([x_test1,x_test2])
predictions1=sc.inverse_transform(predictions)
predictions1


# In[101]:


preds1=[]
preds=[]
count=0
for i in range(60,len(closing_chg1)):
    if closing_chg1[i][0]>=0:
        preds1.append([1])
    else:
        preds1.append([0])
for i in range(0,len(predictions)):
    if predictions[i][0]>=0:
        preds.append([1])
    else:
        preds.append([0])
    prev=predictions[i][0]
for k in range(0,len(preds1)):
    if preds[k]==preds1[k]:
        count=count+1
print((count/len(preds1))*100)


# In[99]:


print(validator[60:])


# In[100]:


print(preds)


# In[102]:


print(preds1)


# In[103]:


plt.plot(closing_chg1[60:],color='green')
plt.plot(predictions1,color='blue')
plt.show()


# In[ ]:




