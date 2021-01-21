import numpy as np

def createData():
    x1 = np.array([[1,1,1,1,1,1]])
    x2 = np.array([[-1,-1,-1,-1,-1,-1]])
    x3 = np.array([[1,-1,-1,1,1,1 ]])
    x4 = np.array([[1,1,-1,-1,-1,-1]])
    x = np.concatenate((x1.T,x2.T,x3.T,x4.T),axis = 1)
    
    y1 = np.array([[1,1,1]])
    y2 = np.array([[-1,-1,-1]])
    y3 = np.array([[-1,1,1]])
    y4 = np.array([[1,-1,1]])
    y = np.concatenate((y1.T,y2.T,y3.T,y4.T),axis = 1)
    
    return x,y

def testInput(weight,data):
    for i in range(len(data.T)):
        res = weight.T @ data.T[i]
        res[res >= 0] = 1
        res[res < 0] = -1
        print("Y for input ",i," : ")
        print(res.reshape(3,1))
        print()

def testTarget(weight,data):
    for i in range(len(data.T)):
        res = weight @ data.T[i]
        res[res > 0] = 1
        res[res <= 0] = -1
        print("X for output ",i," : ")
        print(res.reshape(6,1))
        print()

x,y = createData()
weight = x @ y.T
print("The weight matrix is : ")
print(weight)

testInput(weight,x)

testTarget(weight,y)