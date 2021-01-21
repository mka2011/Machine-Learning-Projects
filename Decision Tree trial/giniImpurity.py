
import numpy as np
import pandas as pd
import math

"""Function to find all unique slopes"""
def getUniq(data,attr):
    a = list()    
    for i in data[attr]:
        a.append(i)    
    return(set(a))

"""helper Function to calculate entropy"""
def hValue(indivVal):
    total = indivVal[0]
    totalPos = indivVal[1]
    totalNeg = indivVal[2]
    hval1 = 0
    if totalPos != 0:
        hval1 = -(totalPos/total * math.log2(totalPos/total))
    
    if totalNeg != 0:
        hval1 += -(totalNeg/total * math.log2(totalNeg/total))
    
    return hval1

"""Calculating frequency of all slopes along with their positive and negative values"""
def getInfoVals(data,uniqueVals,attr):
    infoGainTemp = dict()
    for i in uniqueVals:
        temp = data[data[attr] == i]
        totalPos = len(temp[temp["heart disease"] == 1])
        totalNeg = len(temp[temp["heart disease"] == 0])
        infoGainTemp[i] = [totalPos+totalNeg,totalPos,totalNeg]
    
    infoGain = dict()
    for i in uniqueVals:
        hval = hValue(infoGainTemp[i])
        infoGain[i] = infoGainTemp[i][0]/data.shape[0]
        
    return infoGain,infoGainTemp

"""Function to calculate entropy for all unique slopes"""
def calcEntropy(infoGainVals,infoGainTemp,size):
    entropy = 0
    
    for i in infoGainVals.keys() :
        entropy += (infoGainTemp[i][0]/size) * infoGainVals[i]
    return entropy

"""Calculates gain"""
def calcGain(globalEntropy,cumEntropy):
    return globalEntropy - cumEntropy

"""Calculates global entropy"""
def calcGlobal(dataset):
    pos = len(dataset[dataset["heart disease"] == 1])
    neg = len(dataset[dataset["heart disease"] == 0])
    return hValue([dataset.shape[0],pos,neg])

"""Input dataset"""
dataset = pd.read_csv("cleveland.csv").iloc[:,[10,13]]
dataset.columns = ["slope","heart disease"]

"""Calculate gain,individual as well as cumulative entropy and global entropy"""
uniqueVals = getUniq(dataset,"slope")
infoGainVals,infoGainTemp = getInfoVals(dataset,uniqueVals,"slope")
cumEntropy = calcEntropy(infoGainVals,infoGainTemp,dataset.shape[0])
globalEntropy = calcGlobal(dataset)
gain = calcGain(globalEntropy,cumEntropy)

"""Prints all the values"""
for i in uniqueVals:
    print("The slope ",i," has an entropy of : ",infoGainVals[i])

print("The cumulative entropy is : ",cumEntropy,"\nThe global entropy is : ",globalEntropy,"\nThe gain is :",gain)
    
    