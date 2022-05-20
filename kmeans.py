import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def get_data():
    data = pd.read_csv("data.csv")
    return data

def get_centroids(data):
    c1 = int(np.random.rand(1).tolist()[0]*data.iloc[:,0].count())
    c2 = int(np.random.rand(1).tolist()[0]*data.iloc[:,0].count())
    if(c1 == c2):
        c2 = int(np.random.rand(1).tolist()[0]*data.iloc[:,0].count())
    centroid1 = [data.iloc[c1,0],data.iloc[c1,1]]
    centroid2 = [data.iloc[c2,0],data.iloc[c2,1]]
    return centroid1, centroid2

def calc_dist(data, centroid1, centroid2):
    a1=[];a2=[]
    data = data.copy()
    for i in range(len(data)):
        newdata1 = np.sqrt(abs(centroid1[0] - data.iloc[i,0])**2 + (abs(centroid1[1] - data.iloc[i,1]))**2)
        newdata2 = np.sqrt(abs(centroid2[0] - data.iloc[i,0])**2 + (abs(centroid2[1] - data.iloc[i,1]))**2)
        a1.append(newdata1)
        a2.append(newdata2)
    data.insert(2, "distance1", a1)
    data.insert(3, "distance2", a2)
    return data

def min_dist(data):
    m=[];n=[]
    for i in range(len(data)):
        if data.iloc[i,2]<data.iloc[i,3]:
            m.append(data.iloc[i,2])
            n.append(1)
        else:
            m.append(data.iloc[i,3])
            n.append(2)
    data.insert(4, "min", m)
    data.insert(5, "NewCluster", n)
    return data

def plotting(centroid1, centroid2, data):
    if(len(data.columns) > 5):
        plt.scatter(data.iloc[:,0], data.iloc[:,1], c=data.iloc[:,5])
    else:
        plt.scatter(data.iloc[:,0], data.iloc[:,1])
    plt.scatter(centroid1[0], centroid1[1], color="red")
    plt.scatter(centroid2[0], centroid2[1], color="red")
    plt.show()

def new_centroids(m, n, data):
    count1=0;count2=0
    centroid1 = [0,0]
    centroid2 = [0,0]
    for i in range(len(data)):
        if data.iloc[i,5] == 1:
            centroid1[0] += data.iloc[i,0]
            centroid1[1] += data.iloc[i,1]
            count1 += 1
        else:
            centroid2[0] += data.iloc[i,0]
            centroid2[1] += data.iloc[i,1]
            count2 += 1
    centroid1[0] = centroid1[0]/count1
    centroid1[1] = centroid1[1]/count1
    centroid2[0] = centroid2[0]/count2
    centroid2[1] = centroid2[1]/count2
    return centroid1, centroid2

def main():
    data = get_data()
    centroid1, centroid2 = get_centroids(data)
    plotting(centroid1, centroid2, data)
    while True:        
        oldCentroid1 = centroid1; oldCentroid2 = centroid2
        data = calc_dist(data, centroid1, centroid2)
        newData = min_dist(data)
        print("Plotting Inermediate Results")
        centroid1, centroid2 = new_centroids(newData.iloc[:,4].sum(), newData.iloc[:,5].sum(), newData)
        if(centroid1 == oldCentroid1 and centroid2 == oldCentroid2):
            print("Plotting Final Results")
            plotting(centroid1, centroid2, newData)
            print("Minimum Error", sum(data.iloc[:,4]))
            break
        plotting(centroid1, centroid2, newData)
        data.drop(columns=["distance1", "distance2", "min", "NewCluster"], inplace=True)
main() 