from math import log
import operator
def calcShannonEnt(dataSet):
    entriesNum=len(dataSet)
    classLabels={}
    for key in dataSet:
        classLabel=key[-1]
        if classLabel in classLabels.keys():
            classLabels[classLabel]+=1
        else:
            classLabels[classLabel]=1
    calc=0.0
    for key in classLabels:
        calc-=classLabels[key]/float(entriesNum)*log(classLabels[key]/float(entriesNum),2)
    return calc
def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    #change to discrete values
    return dataSet, labels
def splitDataSet(dataSet,axis,value):
    result=[]
    for feature in dataSet:
        if feature[axis]==value:
            temp=feature[:axis]
            temp.extend(feature[axis+1:])
            result.append(temp)
    return result 
def chooseBestFeature(dataSet):
    featuresNum=len(dataSet[0])-1
    baseEntropy=calcShannonEnt(dataSet)
    bestInfoGain=0.0
    bestFeature=-1
    for i in range(featuresNum):
        values=[example[i]for example in dataSet]
        uniqValues=set(values)
        newEntroy=0.0
        for value in uniqValues:
            temp=splitDataSet(dataSet,i,value)
            prob=len(temp)/float(len(dataSet))
            newEntroy+=prob*calcShannonEnt(temp)
        infoGain=baseEntropy-newEntroy
        if infoGain>bestInfoGain:
            bestInfoGain=infoGain
            bestFeature=i
    return bestFeature
def majorityCnt(classList):
    classCount={}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]
def createTree(dataSet,labels):
    classList=[example[-1]for example in dataSet]
    if classList.count(classList[0])==len(classList):
        return classList[0]
    if len(dataSet[0])==1:
        return majorityCnt(classList)
    bestFeat=chooseBestFeature(dataSet)
    bestFetLabel=labels[bestFeat]
    myTree={bestFetLabel:{}}
    del(labels[bestFeat])
    featValues=[example[bestFeat]for example in dataSet]
    uniqueValues=set(featValues)
    for value in uniqueValues:
        subLabels=labels[:]
        myTree[bestFetLabel][value]=createTree(splitDataSet(dataSet, bestFeat, value), subLabels)  
    return myTree  


a,b=createDataSet()
print a
print b 
c=calcShannonEnt(a)
print c  
print chooseBestFeature(a)
print createTree(a,b)      