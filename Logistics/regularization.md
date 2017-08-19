# 正则化(regularization）
## 1.正则性（regularity）
正则性衡量了函数光滑的程度，正则性越高，函数越光滑。（光滑衡量了函数的可导性，如果一个函数是光滑函数，则该函数无穷可导，即任意n阶可导）。
## 2.过拟合

![image](http://www.datalearner.com/resources/blog_images/d5095e9f-bf4e-454b-a1ed-92557a013299.png)

从左到右分别是欠拟合（underfitting，也称High-bias）、合适的拟合和过拟合（overfitting，也称High variance）三种情况。

解决过拟合的两种方法：

- 尽量减少选取变量的数量。我们可以人工检查每一个变量，确定哪些变量更为重要，保留那些更为重要的特征变量。自然，最好的做法还是采取某种约束可以自动选择重要的特征变量，自动舍弃不需要的特征变量。

- 正则化。采用正则化方法会自动削弱不重要的特征变量，自动从许多的特征变量中“提取”重要的特征变量，减小特征变量的数量级

## 3.正则化
### 3.1引例

![image](http://www.datalearner.com/resources/blog_images/6a01bed3-190f-4418-85ec-10e92d14bbd5.png)

上面的λ||θ||^2便是正则化项，只不过这里用的是L2范数。

### 3.2正则化项的类型概要介绍
正则化项可以是零范数、一范数、二范数、迹范数、Frobenius范数和核范数等。下面来具体看一下L0、L1、L2三种：
- L0范数是指向量中非0的元素的个数。
- L1范数是指向量中各个元素绝对值之和。
- L2范数是指向量各元素的平方和然后求平方根。

L0和L1都是参数是稀疏的。L0范数希望W的大部分元素都是0。但是，L0范数很难优化求解（NP难问题）。

L1范数是L0范数的最优凸近似，如果在研究建模时，如果隐特征中大多数与最终结果没多大关系的话，在训练模型时希望这些特征的权重尽可能为0的话，也就是想要使得整个矩阵变得稀疏的话，一般采取L1范数来正则化。

L2范数在研究建模中是为了防止过拟合的，不断地进行权值衰减，也就是使参数矩阵的每个元素都很小，趋近于0，但不会像L1范数那样等于0。

L1和L2范数下降速度比较：

![image](http://img.blog.csdn.net/20160813232632087?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

对于L1和L2规则化的代价函数来说，我们可以写成以下形式：

![image](http://img.blog.csdn.net/20160813232806943?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

L1和L2范数约束空间：

![image](http://img.blog.csdn.net/20160813232854725?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

L1范数在二维平面是一个矩形，L2范数在二维空间是一个圆；

可以看到，L1-ball 与L2-ball 的不同就在于L1在和每个坐标轴相交的地方都有“角”出现，而目标函数的等高线大部分时候第一次都会与L1-ball在角的地方相交。注意到在角的位置就会产生稀疏性，例如图中的相交点就有w1=0，而更高维的时候（想象一下三维的L1-ball 是什么样的？）除了角点以外，还有很多边的轮廓也是既有很大的概率成为第一次相交的地方，又会产生稀疏性。

相比之下，L2-ball 就没有这样的性质，因为第一次相交的地方不太可能出现在任意坐标轴上，因此不太可能产生稀疏性。这就从直观上来解释了为什么L1-regularization 能产生稀疏性，而L2-regularization 不行的原因了。

因此，L1会趋向于产生少量的特征，而其他的特征都是0，而L2会选择更多的特征，这些特征的权重系数都会接近于0。

       
所以，综合这三种范数的特点来看的话：如果在建模时，特征数较多，而很多特征又与结果没有直接关系的话，想要参数矩阵变得稀疏的的话，就选择L1范数；如果在进行矩阵分解时，设定特征数量后，希望每个特征都能有一定的权重的话，那么就选择L2范数。L1是让绝对值最小，L2是让平方最小，由此可知，L1的下降速度很快，L2范数在优化迭代时的下降是平缓稳定的，逐渐收敛到0附近。
### 3.3正则化的本质
> 约束（限制）要优化的参数

正则化其实和“带约束的目标函数”是等价的，二者可以互相转换。关于这一点，以引例为案例，给出公式进行解释：

![image](http://img.blog.csdn.net/20140927172820098?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvd3NqOTk4Njg5YWE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

通过熟悉的**拉格朗日乘子法**，可以变为如下形式：

![image](http://img.blog.csdn.net/20140927173332395?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvd3NqOTk4Njg5YWE=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

这两个等价公式说明了，正则化的本质就是，给优化参数一定约束，所以，正则化与加限制约束，只是变换了一个样子而已。
### 3.4正则化详解
#### 3.4.1 L2 regularization（权重衰减）

-  L2正则化就是在代价函数后面加上一个正则化项：

![image](http://i.imgur.com/9WnBBu1.jpg)

C0代表原始的代价函数，后面那一项就是L2正则化项（所有参数w的平方的和，除以训练集的样本大小n。λ就是正则项系数，权衡正则项与C0项的比重。另外还有一个系数1/2，1/2经常会看到，主要是为了后面求导的结果方便，后面那一项求导会产生一个2，与1/2相乘刚好凑整）

- L2正则化项是怎么避免overfitting的呢？我们推导一下看看，先求导：

![image](http://i.imgur.com/mebEC90.jpg)
    
可以发现L2正则化项对b的更新没有影响，但是对于w的更新有影响:

![image](http://i.imgur.com/qM83geg.jpg)

在不使用L2正则化时，求导结果中w前系数为1，现在w前面系数为 1−ηλ/n ，因为η、λ、n都是正的，所以 1−ηλ/n小于1，它的效果是减小w，这也就是权重衰减（weight decay）的由来。当然考虑到后面的导数项，w最终的值可能增大也可能减小。

- 到目前为止，我们只是解释了L2正则化项有让w“变小”的效果，但是还没解释为什么w“变小”可以防止overfitting？

    一个所谓“显而易见”的解释就是：更小的权值w，从某种意义上说，表示网络的复杂度更低，对数据的拟合刚刚好（这个法则也叫做奥卡姆剃刀），而在实际应用中，也验证了这一点，L2正则化的效果往往好于未经正则化的效果。当然，对于很多人（包括我）来说，这个解释似乎不那么显而易见，所以这里添加一个稍微数学一点的解释（引自知乎）：
    
    过拟合的时候，拟合函数的系数往往非常大，为什么？如下图所示，过拟合，就是拟合函数需要顾忌每一个点，最终形成的拟合函数波动很大。在某些很小的区间里，函数值的变化很剧烈。这就意味着函数在某些小区间里的导数值（绝对值）非常大，由于自变量值可大可小，所以只有系数足够大，才能保证导数值很大。

![image](http://i.imgur.com/RsR5cOK.png)

而正则化是通过约束参数的范数使其不要太大，所以可以在一定程度上减少过拟合情况
#### 3.4.2 L1 regularization、数据集扩增、dropout
[L1 regularization、数据集扩增、dropout](http://blog.csdn.net/u012162613/article/details/44261657)
### 3.5正则化的作用
### 3.5.1 防止过拟合；
### 3.5.2正则化项的引入其实是利用了先验知识
体现了人对问题的解的认知程度或者对解的估计；例如正则化最小二乘问题如下：
### 3.5.3 解决条件数（condition number）

条件数（condition number）不好的情况下矩阵求逆很困难的问题。
> 条件数：如果方阵A是非奇异（A的行列式不等于0，正定矩阵一定是非奇异的）的，那么A的condition number定义为：

![image](http://img.blog.csdn.net/20160813183849334?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

![image](http://img.blog.csdn.net/20160813185637967?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQv/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/Center)

在样本数小于参数个数的情况下，样本矩阵很可能是不可逆的（条件数很大），而引入正则化项将会解决这个问题。
### 3.5.4正则化项的引入平衡了偏差（bias)与方差(variance)理论
[关于偏差和方差参考误差理论](http://blog.csdn.NET/linkin1005/article/details/42563229)
### 3.5.5产生了稀疏性
[稀疏性](http://www.cnblogs.com/Rosanna/p/3946596.html)