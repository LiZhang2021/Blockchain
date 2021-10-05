# Blockchain

本代码仓库（repository）用于存放与区块链论文相关的问题。

## 仓库结构

根据讨论问题，分别建立相应的文件夹（讨论区）。文件夹结构如下(文章列表的编号与笔记列表的编号一一对应)：

* Blockchain/some_topic/README.md
* Blockchain/some_topic/Papers/README.md  （文章列表）
* Blockchain/some_topic/Papers/1.文章---
* Blockchain/some_topic/Papers/2.文章---
* Blockchain/some_topic/Papers/3.文章---
* Blockchain/some_topic/Notes/README.md  （笔记列表）
* Blockchain/some_topic/Notes/1.md  （1.文章--- 对应笔记）
* Blockchain/some_topic/Notes/2.md  （2.文章--- 对应笔记）
* Blockchain/some_topic/Notes/3.md  （3.文章--- 对应笔记）

文章结构示例如下:

* Blockchain/Blockchain_in_Wireless_Networks/README.md
* Blockchain/Blockchain_in_Wireless_Networks/Papers/README.md
* Blockchain/Blockchain_in_Wireless_Networks/Papers/1. BLOWN -- A Blockchain Protocol for Wireless Networks under Adversarial SINR(M.Xu&etal, 2021).pdf
* Blockchain/Blockchain_in_Wireless_Networks/Papers/2. Concordia -- A Streamlined Consensus Protocol for Blockchain Networks(C.Santiago&etal, 2021).pdf
* Blockchain/Blockchain_in_Wireless_Networks/Papers/3. How Does CSMA-CA Affect the Performance and Security in Wireless Blockchain Networks(B.Cao&etal, 2020).pdf
* Blockchain/Blockchain_in_Wireless_Networks/Notes/README.md
* Blockchain/Blockchain_in_Wireless_Networks/Nodes/1.md
* Blockchain/Blockchain_in_Wireless_Networks/Notes/2.md
* Blockchain/Blockchain_in_Wireless_Networks/Notes/3.md


## 论文标识

在论文中

| 标识 | 含义 |
| ----------- | ----------- |
| <font style="background: red">红色荧光</font> | 系统模型的假设 |
| <font style="background: blue">蓝色荧光</font> | 定义 |
| <font style="background: yellow">黄色荧光</font> | 文章的创新点 |
| <font style="background: green">绿色荧光</font> | 文章中某些重要定理 |
| <font color=Red>红色下划线</font> | 文章中写的比较好的英文 |
| <font color=Green>绿色下划线</font> | 文章中仿真结果和结论 |

详细实例见 Blockchain/Example.pdf

## 日志 LOG

### 2021/10/05

#### 进展
1. 完成了Blockchain/Double_Spending_Attacks/Notes/4.md笔记的重新编辑，并回答之前提出的相关问题；
   *本文提出了一种自适应双花攻击，计算最优双花攻击决策以及通过发起自适应双花攻击奖励的期望的理论界。本文中将双花攻击过程看作是一个随机过程，通过最大化攻击者收益作为目标函数，以攻击决策作为随机变量，通过采用随机动态规划求的该优化问题的最优解，即在收益最大化时，攻击者的最优决策。因此，攻击者根据收益来做出决策是否继续攻击而实现了一个自适应的双花攻击。
   最终分析得出结论：1）该自适应双花攻击受到确认区块数量的影响极大，当确认区块数量越大时，获得的奖励越低，从而系统也就越安全；2）自适应双花攻击也受到攻击者控制系统的哈希算力影响，当攻击者控制的哈希算力越大时，所获得的奖励越高，从而攻击越容易成功，即系统越不安全。因此，本文通过基于随机动态规划算法来计算得到攻击策略的决策矩阵可以使得攻击者根据收益的大小来决定是否发起攻击。从而来来评估系统的安全性。
2. 完成了一个小时练习毛笔字的任务；
3. 今天并没有完成阅读Blockchain/Blockchain_in_Wireless_Networks/Papers/9.pdf，并在文章中用相应的颜色标记重点内容。


#### 计划
1. 8：30 ~ 12：00 am 完成阅读Blockchain/Blockchain_in_Wireless_Networks/Papers/9.pdf，并在文章中用相应的颜色标记重点内容；
2. 13:30 ~19:30 pm 完成Blockchain/Double_Spending_Attacks/Notes/5.md笔记的重新编辑，并回答之前提出的相关问题；
3. 20 ：30 ~ 21：00 练习一篇毛笔字；
4. 21 ：00 ~ 22：30 完成当日日志的记录。

### 2021/10/03~04

#### 进展
1. 完成部分Blockchain/Blockchain_in_Wireless_Networks/Papers/8.pdf文章的笔记的整理。
   * 这篇文章提出了多接口的PBFT系统，通过在PBFT算法的基础上加上带宽预约协议。通过带宽预约协议选出请求提出的节点（主节点），随后该节点通过原子广播执行PBFT算法过程，最终将记录/交易依据序列号排序插入到排序节点（共识节点）的内存池中。当内存池中记录/交易的数量达到某一阈值后，共识节点将会根据选择规则选出主节点。之后，该节点将一定数量的记录/交易打包成区块，并通过PBFT协议达成共识。最后将达成共识的区块连接到各自节点的区块链上，同时也将最终结果返回给代理。
   * 随后，本文作者通过建模分析该系统的性能，主要分析了带宽预约协议对于系统性能的影响。通过增加系统总负载，分析了排序节点数量以及节点的区域覆盖率对于系统性能的影响。在讨论系统的型嗯那个时，平均系统响应时间、共识节点的通信时间以及系统的容量作为衡量系统性能的重要指标。最终得出结论：1）增加共识节点的数量会提升每个节点的有效负载，从而提升系统的容量；2）但是提升共识节点的数量也会提升媒体之间争用的机会从而使得带宽预约协议运行时间变长；3）提升节点之间的物理距离将会提升用于插入记录到分布式账本中所需要的时间，从而使得插入相同数量的记录/交易将花费更长的时间，降低系统的性能。
   * 本文中只重点分析了记录/交易插入过程的系统性能，根据最终结果可知，该系统的扩展性不太好，因为随着共识节点数量的增加，会使得系统处理速度降低，尽管节点的增加会提升系统的容量，但是这个提升也是有限的。那么当节点数量上百上千的时候，也许系统处理速度将会明显降低。此外，该协议中共识节点数量好像一开始就固定了的，并没有考虑新公式节点加入系统设计。那么，共识节点是静态的，会使得当节点出现故障时，或者当故障节点书来给你超过系统能够容忍的最大阈值时，系统将出现故障，并且无法恢复。因此，将系统中共识委员会设置成为动态的更能确保系统的安全性和活性。此外，针对代理请求插入的记录/交易的有效性也需要验证，否则会出现错误交易被确认到区块中，这将对该系统造成毁灭性的打击。最后，关于区块的生成和确认过程，区块远远大于交易的大小，这使得区块的共识过程将花费大量的时间，只采用本文中对于记录/交易插入过程的性能来分析系统的性能可能还不太够。因此，为了提升系统性能，最好是将交易插入过程和区块生成过程解耦，使得这两个过程能够并行进行，从而提升系统总体性能。
2. 这两天由于朋友相约，进展非常缓慢，有些计划好的工作也没有完成。接下来基本没有假期了，就在学校好好的学习啦。


#### 计划
1. 完成全部Blockchain/Double_Spending_Attacks/Notes/4.md笔记的重新编辑，并回答之前提出的相关问题；
2. 阅读Blockchain/Blockchain_in_Wireless_Networks/Papers/9.pdf，并在文章中用相应的颜色标记重点内容；
3. 中午午饭之后，练习一篇毛笔字。

### 2021/10/02

#### 进展
1. 跟哥哥商讨完了文件命名规则，完成了Blockchain仓库所有pdf文件依据新的命名规则进行重命名。
2. 完成部分Blockchain/Blockchain_in_Wireless_Networks/Papers/8.pdf文章的笔记的整理。更加清晰的了解物联网应用区块链技术时面临的有限资源设备的限制，无线网络传输存在信道争用问题，以及节点共识安全性和扩展性问题。


#### 计划
1. 完成全部Blockchain/Blockchain_in_Wireless_Networks/Papers/8.pdf文章的笔记编辑；
2. 完成日记的写作；
3. 练习一篇毛笔字。

### 2021/10/01

#### 进展
1. 完成了Blockchain/Double-Spending_Attacks/Notes/3.md的重新编辑，回答之前提出的问题，并添加文章中的核心理论分析； 
2. 将Blockchain仓库中双花攻击文件和无线区块链文件中的文章依据新的命名规则进行重命名。
3. 完成部分Blockchain/Blockchain_in_Wireless_Networks/Papers/8.pdf文章的笔记编辑

#### 计划
1. 讨论并确定命名规则；
2. 完成Blockchain/Blockchain_in_Wireless_Networks/Papers/8.pdf文章的笔记编辑

### 2021/9/30

#### 进展
1. 编辑了部分Double-Spending_Attacks/Notes/3.md 
2. 重新梳理了Double-Spending_Attacks/Papers/3.pdf
3. 今天并没有完成昨天的计划，因此需要在明天追赶上来

#### 计划
1. 在上午完成Blockchain/Double-Spending_Attacks/Notes/3.md的重新编辑，回答之前提出的问题，并添加文章中的核心理论分析；
2. 在下午和晚上完成将Blockchain/Blockchain_in_Wireless_Networks/Papers/8.pdf文章的笔记编辑。
3. 完成对Blockchain仓库中关于双花攻击和无线区块链中文章依据新的命名规则进行重命名。

### 2021/9/29

#### 进展
1. 完成Blockchain/Double-Spending_Attacks/Notes/2.md的重新编辑，回答了之前提出的问题，并添加了文章中的核心理论分析； 
2. 将Blockchain/Blockchain_in_Wireless_Networks/Papers/8.pdf看完了，并在文章中做了相应的标记。

#### 计划
1. 计划在30号完成Blockchain/Blockchain_in_Wireless_Networks/Notes/8.md的编辑，整理文章的脉络，提出问题并解答提出的问题。
2. 对于Blockchain/Double-Spending_Attacks/Notes/3.md进行重新编辑，并添加理论分析以及补充回答问题讨论中的相关问题。

### 2021/9/28

#### 进展
1. 完成Blockchain/Double_Spengding_Attacks/Notes/1.md的编辑； 
2. 开始精读Blockchain/Blockchain_in_Wireless_Networks/Papers/8.pdf，并且做相应的标记。

#### 计划
1. 完成Blockchain/Blockchain_in_Wireless_Networks/Papers/8.pdf论文的标记，并写关于这篇文章的笔记；
2. 对Blockchain/Double_Spengding_Attacks/Notes/2.md中的理论推导进行重新梳理；

### 2021/9/27

#### 进展
1. 完成Blockchain_in_Wireless_Network/Notes/7.md的编写
2. 对于Double-Spending_Attack/Notes/1.md添加了关于双花攻击成功的概率的计算以及成功攻击后奖励的期望计算

#### 计划
1. 明天完成Double-Spending_Attack/Notes/1.md中问题讨论部分加入交易费用后的计算，将计算过程重新完整的写下来；
2. 开始看文章Blockchain_in_Wireless_Network/Paper/8，并将文章中的内容按照规则进行标记

### 2021/9/26

#### 进展
1. 将Blockchain_in_Wireless_Network文件中的 Papers 加了三篇新的文章，Notes文件夹也添加了三个； 
2. 读完了Blockchain_in_Wireless_Network/Papers/7. Comparison of single and multiple entry point PBFT for IoT blockchain Systems(J.Misic&etal, 2020).pdf那篇文章，在文章中做完了标记。

#### 计划
1. 明天完成Blockchain_in_Wireless_Network/Notes/7.md文章的编写；
2. 针对Double_Spengding_Attack/Notes/1.md中的问题进行解答，并对文章中的公式进行推导，并将过程加入到对应笔记中。


### 2021/9/25

#### 进展
1. 进展1 
2. 进展2

#### 计划
1. 计划1
2. 计划2


### 2021/9/24

#### 进展
1. 进展1 
2. 进展2

#### 计划
1. 计划1
2. 计划2