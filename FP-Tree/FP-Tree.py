class treeNode:
    #FP树的节点的结构
    def __init__(self,name, num, parent):
        self.name=name
        self.count=num
        self.parent=parent
        self.children={}
        self.nodeLink=None#存储下一个相似的节点
    def inc(self, number):
        #增加节点的处出现次数
        self.count+=number

class FPTree():
    def __init__(self,number,support):
        self.number=number
        self.support=support#阈值
        self.items=[]#存储数据集合
        self.freqItems=[]#存储最终结果
        for i in range(self.number):
            self.items.append([])

    def __items_input(self):
        print"数据以数字'9'结束"
        for i in range(self.number):
            print"请输入数据"+str(i+1)
            while 1:
                ch=raw_input();
                if ch!='9' and ch!=9:
                    self.items[i].append(ch)
                else:
                    break    

    def __createTree(self,dataSet):
        #创建头指针表
        headerTable={}
        for items in dataSet:
            for item in items:
                headerTable[item]=headerTable.get(item, 0)+1
        #移除低于阈值的元素
        for k in headerTable.keys():
            if headerTable[k]<self.number*self.support:
                del(headerTable[k])
        freqItemSet=set(headerTable.keys())
        if len(freqItemSet)==0:
            return None, None
        #存放相似元素项
        for k in headerTable:
            headerTable[k]=[headerTable[k], None]
        tree = treeNode('Null Set', 1, None)
        #创建FP树
        for items,count in dataSet.items():
            temp={}
            for item in items:
                if item in freqItemSet:
                    temp[item]=headerTable[item][0]
            if len(temp) > 0:
                sortedItems=[v[0] for v in sorted(temp.items(), key=lambda p: p[1], reverse=True)]
                self.__updateTree(sortedItems,tree,headerTable,count)
        return tree,headerTable

    def __updateTree(self,items,tree,headerTable,count):
        #将节点添加到树种
        if items[0] in tree.children:
            tree.children[items[0]].inc(count)
        else:
            tree.children[items[0]]=treeNode(items[0],count,tree)
            if headerTable[items[0]][1]==None:
                headerTable[items[0]][1]=tree.children[items[0]]
            else:
                self.__updateHeader(headerTable[items[0]][1],tree.children[items[0]])           
        if len(items)>1:
            self.__updateTree(items[1::],tree.children[items[0]],headerTable,count)    
        
    def __updateHeader(self,aNode,bNode):
        while (aNode.nodeLink!=None):
            aNode=aNode.nodeLink
        aNode.nodeLink=bNode  

    def __createInitSet(self):
        retDict={}
        for trans in self.items:
            retDict[frozenset(trans)]=1
        return retDict

    def __findPrefixPath(self,basePat,treeNode):
        #寻找元素的条件基
        condPats = {}
        while treeNode != None:
            prefixPath = []     
            self.__ascendTree(treeNode, prefixPath)
            if len(prefixPath) > 1:
                condPats[frozenset(prefixPath[1:])] = treeNode.count
            treeNode = treeNode.nodeLink
        return condPats

    def __ascendTree(self,leafNode, prefixPath):
        if leafNode.parent != None:
            prefixPath.append(leafNode.name)
            self.__ascendTree(leafNode.parent, prefixPath)    
        
    def __mineTree(self,tree,headerTable,preFix,freqItemList):
        #迭代挖掘FP树
        bigL = [v[0] for v in sorted(headerTable.items(),key = lambda p:p[1])]
        for basePat in bigL:
            newFreqSet = preFix.copy()
            newFreqSet.add(basePat)
            freqItemList.append(newFreqSet)
            condPattBases =self.__findPrefixPath(basePat, headerTable[basePat][1])
            myConTree,myHead =self.__createTree(condPattBases)
            if myHead != None:
                self.__mineTree(myConTree, myHead,newFreqSet, freqItemList)
    def __resuDisplay(self):
        for i in self.freqItems:
            print i
    def solve(self):
        self.__items_input()
        dic=self.__createInitSet()
        myFPtree, myHeaderTab=self.__createTree(dic)
        self.__mineTree(myFPtree, myHeaderTab,  set([]),self.freqItems)
        self.__resuDisplay()

a=int(raw_input("请输入数据的条数："))
b=float(raw_input("请输入阈值："))
pf=FPTree(a,b)
pf.solve()
