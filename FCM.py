import csv
import random as rand
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import copy
from mpl_toolkits.mplot3d import Axes3D
from kneed import KneeLocator


figure(figsize=(8, 6), dpi=80)


rand.seed(time.time())
tradeoff=0.3

class datapoint:
    def __init__(self,data,cluster):
        self.data=data
        self.cluster=cluster

def plotter(color,ax,data,gradient=1.0):
    z=''
    h=''
    x=''
    y=''

    if(len(data[0])==2):
     x = [data[i][0] for i in range(len(data))]
     y = [data[i][1] for i in range(len(data))]
    elif (len(data[0])>=3):
     x = [data[i][0] for i in range(len(data))]
     y = [data[i][1] for i in range(len(data))]
     z = [data[i][2] for i in range(len(data))]

    if z=='':
        plt.plot(x, y, color, alpha=gradient)
        ax.view_init(azim=0, elev=90)
    elif h=='':
        print()
        #Axes3D.scatter(ax,x,y,z,gradient*color)
        ax.plot (x, y, z, color,alpha=gradient)




def randomPoint(clusters,max,data):
    centers=[]
    for i in range(clusters):
        centers.append([rand.random()% max for j in range(len(data[0]))])
    return np.array(centers)



def kneeFinder(data,tradeoff,mode=0):

    i=0
    finished=[0 for k in range(len(data))]
    if mode==0:
     for i in range(0,len(data)-1):

         baseSlope=data[i+1]-data[i]

         for j in range(i+1,len(data)-1):
             currentSlope=(data[j+1]-data[j])
             gap=tradeoff*abs(baseSlope)

             if currentSlope-baseSlope>gap:
                 print()
                 break
             else:
                 baseSlope=currentSlope
                 finished[i]+=1
                 print()
     print()
     return np.argmax(np.array(finished))
    else:
        knee=None
        sensetivity=[1,2 ,3,4, 5,6, 10, 100, 200, 400]
        t = np.arange(0, len(data), 1)
        for i in range(len(data),-1,-1):
            kn = KneeLocator(t, np.array(data), curve='convex', direction='decreasing', S=sensetivity[i])
            knee = kn.knee
            if knee!=None:
                break
        return knee



def clusterIdentifier(Uik,data):

    datapoints=[]
    for i in range(len(data)):
        datapoints.append(datapoint(data[i],0))

    tempUik=np.transpose(Uik)
    print()

    for j in range(len(tempUik)):
         print()
         index=np.argmax(tempUik[j])+1
         print()
         datapoints[j].cluster=index
    return datapoints


def clusterPlotter(ax,Uik,data,crisp):
    datapoints = clusterIdentifier(Uik, data)

    if crisp:
     for i in range(len(datapoints)):
         print()
         plotter(colors[datapoints[i].cluster], ax, [[datapoints[i].data[k] for k in range(len(datapoints[i].data))]])
    else:
        for i in range(len(datapoints)):
            for j in range(len(Uik)):
                print()
                plotter(colors[j+1], ax ,[[datapoints[i].data[k] for k in range(len(datapoints[i].data))]],round(Uik[j][i],4))
                print()

def phaseCalculator(data,centers,m):
    debugNumber=0
    Uik=np.zeros((len(centers),len(data)))
    print()
    for i in range(len(centers)):
        for k in range(len(data)):
         constant=np.linalg.norm(data[k]-centers[i])
         print()
         tempArr=[]
         if Uik[i][k]==0:
            try:
             tempArr=[np.linalg.norm(data[k]-centers[l])for l in range(len(centers))]
             print()
             tempArr=np.divide(1,tempArr)
             print()
             tempArr = np.multiply(tempArr,constant)
             print()
             tempArr = np.power(tempArr,2/(m-1))
             print()
             tempArr=np.sum(tempArr)
             print()
             Uik[i][k]=np.divide(1,tempArr)
             print()
             debugNumber+=1
            except Exception as e:
                print("Oops!", e.__class__, "occurred.")
                print()
                for l in range(len(tempArr)):
                    if tempArr[i]==0:Uik[l][k]=1
    return Uik

def centerUpdater(data,centers,m,Uik):
    debugNumber=0
    tempArr=[]
    for i in range(len(centers)):
     tempArr2=[np.multiply(np.power(Uik[i][k],m),data[k]) for k in range(0,len(data))]
     print()
     sum=np.array([0.0 for i in range(len(centers[0]))])
     for j in range(len(tempArr2)):
         sum+=tempArr2[j]
     print()
     tempArr2=sum
     tempArr3=[np.power(Uik[i][k],m) for k in range(0,len(data))]
     tempArr3=np.sum(tempArr3)
     print()
     tempArr.append(tempArr2/tempArr3)
     print()
     debugNumber+=1
    return tempArr

def cost(data,centers,m,Uik):
    tempArr = []
    for j in range(len(data)):
        tempArr2=[]
        for i in range(len(centers)):
            tempArr2.append(np.power(Uik[i][j],m)*np.power(np.linalg.norm(data[j]-centers[i]),2))

        tempArr2=np.sum(tempArr2)
        tempArr.append(tempArr2)
    tempArr=np.sum(tempArr)
    return tempArr

def dataProcessor(data):
    tempData=[]

    max = float(data[0][0])
    for i in range(len(data) - 1):
        temp = []
        for j in range(len(data[0])):
            tempFloat = float(data[i][j])
            if abs(tempFloat) > max: max = tempFloat
            temp.append(tempFloat)
        tempData.append(temp)
    tempData.append(max)
    return tempData



fileName="data3.csv"
csv_file = open(fileName)
sv_file = open(fileName)
read_tsv = csv.reader(csv_file, delimiter=",")
data = list(read_tsv)
print()
data=dataProcessor(data)
max=data[len(data)-1]
data=data[0:len(data)-2]
print()
crisp=int(input("1 for crisp and 0 for not crisp "))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plotter("bd",ax,data)
plt.show()
plt.close(fig)
print()
data=np.array(data)
print()
csv_file.close()
colors={1:"bd",2:"gd",3:"md",4:"kd",5:"cd",6:"yd"}
print()
m=float(input("please enter m"))
costs=[]
centers=[]

for clusters in range(1,7):
 centers=randomPoint(clusters,max+1,data)
 print()
 Uik=[]
 debugNumber=0
 for i in range(100):
     Uik=phaseCalculator(data,centers,m)
     print()
     debugNumber+=1
     centers=centerUpdater(data,centers,m,Uik)
     print()


 fig = plt.figure()
 ax = fig.add_subplot(111, projection='3d')
 clusterPlotter(ax,Uik,data,crisp)
 costs.append(cost(data,centers,m,Uik))
 print()
 print("centers are")
 print(centers)
 plotter("rd",ax,centers)
 plt.show()
 plt.close(fig)

 print()





print("costs are")
print(costs)
t=np.arange(0,len(costs),1)
plt.plot(t,costs)
plt.show()
X = np.array(list(zip(t, costs))).reshape(len(t), 2)
knee=kneeFinder(costs,tradeoff,1)
print("appropriate cluster number is")
print(knee+1)
