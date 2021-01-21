import numpy as np
import pandas as pd

"""Function to Split dataset into test and train"""
def split(data,trainSize):
    return data[:trainSize], data[trainSize:]

"""Getting frequency of ages less than and greater than any distinct age"""
def getFreq(train,listVal):
    freqGreat = dict()
    freqLess = dict()
    for i in listVal:
        if i not in freqGreat:
            temp = train[train['age'] >= i]
            frequency = len(temp)
            trueVals = len(temp[temp["heart disease"] == 1])
            falseVals = len(temp[temp["heart disease"] == 0])
            freqGreat[i] = [frequency,trueVals,falseVals]
            
            temp2 = train[train['age'] < i]
            frequency2 = len(temp2)
            trueVals2 = len(temp2[temp2["heart disease"] == 1])
            falseVals2 = len(temp2[temp2["heart disease"] == 0])
            freqLess[i] = [frequency2,trueVals2,falseVals2]
            
    return freqGreat, freqLess

"""Calculating gini weights for every distinct age"""
def calcGiniWeights(freqGreat,freqLess):
    giniWeights = dict()
    
    for i in freqGreat.keys() :
        calcPos = 0 
        calcNeg = 0

        if freqGreat[i][0] != 0:
            calcPos = 1 - ((freqGreat[i][1]/freqGreat[i][0])**2 + (freqGreat[i][2]/freqGreat[i][0])**2)
        
        if freqLess[i][0] != 0:
            calcNeg = 1 - ((freqLess[i][1]/freqLess[i][0])**2 + (freqLess[i][2]/freqLess[i][0])**2)
        
        giniWeights[i] = [calcPos,calcNeg]
    
    return giniWeights

"""Calcultating gini values depending on their weights for all ages"""
def calcGiniVals(freqGreat,freqLess,giniWeights):
    giniVals = dict()
    
    for i in freqGreat.keys():
        posTotal = freqGreat[i][0]
        negTotal = freqLess[i][0]
        total = posTotal + negTotal
        giniVals[i] = (posTotal/total) * giniWeights[i][0] + (negTotal/total) * giniWeights[i][1]
    
    return giniVals

"""Finding all distinct ages in our training set"""
def getList(data):
    listVal = list()
    for i in range(data.shape[0]-1):
        listVal.append((data.iloc[i,0]+data.iloc[i+1,0])/2)
    return sorted(set(listVal))

"""Function to predict on test set"""
def pred(test,bestAge):
    y_pred = list()
    test = np.asarray(test)
    for i in range(test.shape[0]):
        if test[i] < bestAge:
            y_pred.append(0)
        else:
            y_pred.append(1)
    return y_pred

"""Function that calculates accuracy of our predictions"""
def calcAcc(y_pred,y_test):
    count = 0
    y_test = np.asarray(y_test)
    for i in range(y_test.shape[0]):
        if y_pred[i] == y_test[i]:
            count += 1
    return count/y_test.shape[0]

"""Importing dataset"""
dataset = pd.read_csv("cleveland.csv").iloc[:,[0,13]]
dataset.columns = ["age","heart disease"]
trainSize = int(0.7*dataset.shape[0])+1
testSize = dataset.shape[0] - trainSize
train,test = split(dataset,trainSize)
train = train.sort_values(by = ['age'])

"""Computing gini scores"""
giniCompValsList = getList(train)
freqGreat, freqLess = getFreq(dataset,giniCompValsList)
giniWeights = calcGiniWeights(freqGreat,freqLess)
giniVals = calcGiniVals(freqGreat, freqLess, giniWeights)
bestAge = min(giniVals,key = giniVals.get)

"""Prediction and calculation of accuracy"""
y_test = test.iloc[:,1]
test = test.iloc[:,0]
y_pred = pred(test,bestAge)
print("The gini score is : ",giniVals[bestAge]," and the best age for classification is : ",bestAge)
print("The accuracy of Model is : ",calcAcc(y_pred,y_test)*100,"%")
    
