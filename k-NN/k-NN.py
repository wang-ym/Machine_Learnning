from numpy import *
import operator
from matplotlib.cbook import distances_along_curve
from audioop import reverse
import matplotlib
import matplotlib.pyplot as plt
from lib2to3.btm_utils import MinNode
from platform import _release_filename
from dircache import listdir

def creatDataSet():
    group=array([[1.0,1.1],[1.0,1.0],[0.0,0.0],[0,0.1]])
    lebels=['A','A','B','B']
    return group,lebels
def classfy0(inX,dataSet,labels,k):
    dataSetSize=dataSet.shape[0]
    diffMat=tile(inX,(dataSetSize,1))-dataSet
    sqMat=diffMat**2
    sqDistances=sqMat.sum(axis=1)
    diatance=sqDistances**0.5
    sortedMatDis=diatance.argsort()
    classCount={}
    for i in range(k):
        voteLable=labels[sortedMatDis[i]]
        classCount[voteLable]=classCount.get(voteLable,0)+1
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    love_dictionary={'largeDoses':3, 'smallDoses':2, 'didntLike':1}
    fr=open(filename)
    allLines=fr.readlines()
    linNum=len(allLines)
    newMat=zeros((linNum,3))
    index=0
    labels=[]
    for line in allLines:
        line=line.strip()
        Formline=line.split('\t')
        newMat[index,:]=Formline[0:3]
        if(Formline[-1].isdigit()):
            labels.append(int(Formline[-1]))
        else:
            labels.append(love_dictionary.get(Formline[-1]))
        index+=1
    return newMat,labels

def autoNorm(dataSet):
    minN=dataSet.min(0)
    maxN=dataSet.max(0)
    range=maxN-minN
    dataSetSize=dataSet.shape[0]
    noMat=zeros((dataSetSize,3))
    normaDataSet=dataSet-tile(minN,(dataSetSize,1))
    normaDataSet=normaDataSet/tile(range,(dataSetSize,1))
    return normaDataSet,range,minN
    
def plotDraw(datingDataMat,datingLabels):
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter(datingDataMat[:,0],datingDataMat[:,1],15*array(datingLabels),array(datingLabels))
    plt.show()    

def datingClassTest():
    hoRatio=0.10
    datingDataMat,datingLabels=file2matrix('datingTestSet.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    m=normMat.shape[0]
    numTestVecs=int(m*hoRatio)
    errorCount=0.0
    for i in range(numTestVecs):
        classifierResult=classfy0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifer came back with:%d,the real answer id :%d"%(classifierResult,datingLabels[i])
        if(classifierResult!=datingLabels[i]):
            errorCount+=1.0
    print "the rate id :%f"%(errorCount/float(numTestVecs))    

def img2Vector(filename):
    returnVect=zeros((1,1024))
    fr=open(filename)
    for i in range(32):
        linStr=fr.readline()
        for j in range(32):
            returnVect[0,32*i+j]=int(linStr[j])
    return returnVect


def handwritingClassTest():
    hwLabels=[]
    trainingFileList=listdir('trainingDigits')
    m=len(trainingFileList)
    trainingMat=zeros((m,1024))
    for i in range(m):
        fileNameStr=trainingFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:]=img2Vector('trainingDigits/%s'%fileNameStr)
    testFileList=listdir('testDigits')
    errorCount=0.0
    mTest=len(testFileList)
    for i in range(mTest):
        fileNameStr=testFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        vectorUnderTest=img2Vector('testDigits/%s'%fileNameStr)
        classifierResult=classfy0(vectorUnderTest,trainingMat,hwLabels,3)
        print "the classifier came back with :%d,the real answer is :%d"%(classifierResult,classNumStr)
        if(classifierResult!=classNumStr):
            errorCount+=1
    print "\nthe total number of errors is: %d" % errorCount
    print"\n the total error rate is :%f"%(errorCount/float(mTest))

handwritingClassTest()
#datingClassTest()