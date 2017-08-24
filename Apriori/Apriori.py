__metaclass__=type
class Apriori:
    def __init__(self,number,sopport):
        self.items=[]           #存储输入的原始数据
        self.item_set={}        #存储组成数据的元素
        self.pSet=[]            #元素的总体
        self.pMask=[]           #生成子集时的二进制字符串
        self.number=number      #数据的条数
        self.sopport=sopport    #支持度的阈值
        self.subsets=[]         #多项集
        self.result=[]          #频繁多项集
        for i in range(number):
            self.items.append([])

    def items_print(self):
        print"输入的数据为:\n"
        for i in range(self.number):
            lenght=len(self.items[i])
            for j in range(lenght):
                print self.items[i][j],
            print "\n"

    def items_input(self):
        print"数据以字母'c'结束"
        for i in range(self.number):
            print"请输入数据"+str(i+1)
            while 1:
                ch=raw_input();
                if ch!='c' and ch!='C':
                    if self.item_set.has_key(ch):
                        self.item_set[ch]=self.item_set.get(ch)+1
                    else:
                        self.item_set[ch]=1
                    self.items[i].append(ch)
                else:
                    break

    def __result_output(self,n):
        for i in range(n):
            print"频繁"+str(i+1)+"项集："
            for j in range(len(self.result[i])):
                print self.subsets[i][(self.result[i][j])]

    def __pretreatment(self):
        #对数据进行预处理
        temp=len(self.item_set)
        for i in range(temp):
            item=self.item_set.popitem()
            if item[1]>=(self.number*self.sopport):
                self.pSet.append(item[0])
                self.pMask.append(0)

    def __calurate(self,frequency,nlen):
        #通过阈值筛选符合条件的频繁多项集
        for i in range(nlen-1):
            while not(len(frequency[i])==0):
                temp=frequency[i].popitem()
                if not(temp[1]<self.number*self.sopport):
                    self.result[i].append(temp[0])

    def __frequency_store(self,s,mark,frequency):
        #计算各个集合的频率
        for i in range(self.number):
            for j in range(len(s)):
                if (s[j] in self.items[i]):
                    if j==len(s)-1:
                        flag=mark[j][-1]
                        if flag in frequency[j]:
                            frequency[j][flag]=frequency[j].get(flag)+1
                        else:
                            frequency[j][flag]=1
                else:
                    break
                                

    def solve(self):
        self.__pretreatment();
        nlen=len(self.pSet)
        subset=[]               #存储生成子集
        mark=[]                 #子集与频率联系的中介
        frequency=[]            #存储子集的频率
        for i in range(nlen-1):
            self.result.append([])
            self.subsets.append([])
            frequency.append({})
            mark.append([])
            mark[i].append(0)
        while True:
            #生成子集，并对生成的子集计算频率
            k=nlen
            while k>=1:
                if self.pMask[k-1]==1:
                    k-=1
                else:
                    break
            if k>=1:
                subset=[]
                for i in range(nlen):
                    if self.pMask[i]==1:
                        subset.append(self.pSet[i])
                nl=len(subset)
                if nl!=0:
                    self.subsets[nl-1].append(subset)
                    self.__frequency_store(subset,mark,frequency)
                    temp=mark[len(subset)-1][-1]
                    temp=temp+1
                    mark[len(subset)-1].append(temp)
                self.pMask[k-1]=1
                for i in range(k,nlen):
                    self.pMask[i]=0
            else:
                break
        self.__calurate(frequency,nlen)
        self.__result_output(nlen-1)



a=int(raw_input("请输入数据的条数:"))
b=float(raw_input("请输入支持度阈值:"))
apr=Apriori(a,b)
apr.items_input()
apr.items_print()
apr.solve()
