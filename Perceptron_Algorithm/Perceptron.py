#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 18:36:10 2020

@author: manavagrawal
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""For getting training set"""
def getTrainVal(gate):
    x = np.array([[1,0,0],[1,0,1],[1,1,0],[1,1,1]])
    y = np.array([])
    
    if gate == "AND" :
        y = np.append(y,[0,0,0,1])
    
    elif gate == "OR" :
        y = np.append(y,[0,1,1,1])
    
    elif gate == "NAND" :
        y = np.append(y,[1,1,1,0])
    
    else :
        y = np.append(y,[1,0,0,0])
    
    return x,y

def sigmoid(val):
    val = np.array(val)
    return 1 / (1 + np.exp(-val))

"""ANN function, returns weights and list of change in weight per iteration"""
def getWeight(x,y):
    weight = np.random.rand(3)
    weight2 = np.random.rand(3)
    cost = list()
    epochs = 1000
    
    for i in range(epochs):
        index = np.random.randint(0,3)
        changeInWeight_temp = (y[index] - sigmoid(x[index] @ weight.T))
        cost.append(changeInWeight_temp)
        changeInWeight = (changeInWeight_temp * x[index])
        weight = weight + changeInWeight
        
        changeInWeightBatch = 0.1*((y - sigmoid(x @ weight2.T)) @ x)
        weight2 = weight2 + changeInWeightBatch
        
    return weight2,cost
    
"""returns predicted output against test set"""
def predict(weight,x_train):
    pred = weight @ x_train.T
    for i in range(len(pred)):
        if pred[i] <= 0:
            pred[i] = 0
        else:
            pred[i] = 1
            
    return pred

"""Calculates accuracy against test set ouptut"""
def calcAccuracy(y_pred,y_test):
    acc = 0
    
    for i in range(len(y_pred)):
        if y_pred[i] == y_test[i]:
            acc += 1
            
    return (acc/len(y_pred) * 100)

"""For plotting multiple graphs"""
fig, axs = plt.subplots(4, 1, figsize=(15, 12))
e1 = 1000

"""Running prediction algorithm for AND gate"""
x_train, y_train = getTrainVal("AND")
weight,cost = getWeight(x_train,y_train)
y_pred = predict(weight, x_train)
print("The accuracy is : ",calcAccuracy(y_pred,y_train),"%") 
axs[0].plot(range(e1),cost)
axs[0].set_ylim([-1, 1])
axs[0].set_xlabel("Epochs")
axs[0].set_ylabel("Change in Weight")

"""Running prediction algorithm for NAND gate"""
x_train2, y_train2 = getTrainVal("NAND")
weight2, cost2 = getWeight(x_train2, y_train2)
y_pred2 = predict(weight2, x_train2)
print("The accuracy is : ",calcAccuracy(y_pred2,y_train2),"%") 
axs[1].plot(range(e1),cost2)
axs[1].set_ylim([-1, 1])
axs[1].set_xlabel("Epochs")
axs[1].set_ylabel("Change in Weight")

"""Running prediction algorithm for OR gate"""
x_train3, y_train3 = getTrainVal("OR")
weight3, cost3 = getWeight(x_train3, y_train3)
y_pred3 = predict(weight3, x_train3)
print("The accuracy is : ",calcAccuracy(y_pred3,y_train3),"%") 
axs[2].plot(range(e1),cost3)
axs[2].set_ylim([-1, 1])
axs[2].set_xlabel("Epochs")
axs[2].set_ylabel("Change in Weight")

"""Running prediction algorithm for NOR gate"""
x_train4, y_train4 = getTrainVal("NOR")
weight4, cost4 = getWeight(x_train4, y_train4)
y_pred4 = predict(weight4, x_train4)
print("The accuracy is : ",calcAccuracy(y_pred4,y_train4),"%") 
axs[3].plot(range(e1),cost4)
axs[3].set_ylim([-1, 1])
axs[3].set_xlabel("Epochs")
axs[3].set_ylabel("Change in Weight")




