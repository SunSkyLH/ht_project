# 航天器多维度时间序列数据融合挖掘方法研究


## 开发环境
1.单系统数据融合挖掘研究：Python + PyQT5 + SQLServer

2.多系统数据融合挖掘研究：Python + Vue + Flask


## 单系统数据挖掘融合研究
1.建立模板：采用改进的K-means聚类方法，对训练数据的每一维参数分别进行聚类，计算簇内所有点到簇中心点之间的距离，选取距离簇中心点最近的点，作为该参数的模板数据。最终，计算出所有系统参数的模板数据，并存入本地数据库。

2.异常检测：使用分段匹配和动态时间弯曲距离衡量不同序列之间的相似程度。将试验数据与模板数据分段进行匹配，通过改进的DTW求出每一段相似度，若低于所设定的阈值，则可认为待检数据的这段序列出现了异常。

项目系统基于Python语言编写，使用PyQT5编写软件界面，使用SQLServer数据库存储实验数据。


## 多系统数据融合挖掘研究
航天器的各个器件之间存在着极其复杂的耦合关系。这导致卫星的许多遥测参数间存在大量的相关性。

1.针对多参数关联下的异常检测问题，提出了一种无监督学习方法Transformer变分自编码器异常检测模型。该模型使用Transformer的自注意力机制捕获序列之间的关联关系。通过具有特殊残差结构的变分自编码器综合考虑提取到的特征信息，对数据进行重构，利用重构误差进行有效的异常检测。

2.针对故障传播路径识别问题，提出了一种基于Copula熵的传递熵值估计方法(Copula-TE)用于生成遥测变量之间的因果关系网络。该方法可以解决传统传递熵方法计算复杂度较高且含有大量间接因果边的问题。

项目系统采用B/S架构，前端基于Vue框架编写软件界面，后端使用Flask框架处理浏览期请求。


## 联系
由于多系统数据挖掘融合挖掘研究部分，笔者后续将继续进行相关科研研究，核心算法部分还未完全开源。

若有问题，请联系：

- [Github@codingXiaxw](https://github.com/SunSkyLH)


