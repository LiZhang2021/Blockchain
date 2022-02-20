# 无线网络中中的区块链共识算法研究

由于具有去中心化、不可篡改、可追溯、共同维护以及开放透明的特点，区块链在各个领域都有了广泛的应用。但是目前的区块链系统在能耗和稳定性方面并不太适用于设备资源资源有限、节点具有移动性的无线网络。区块链系统的性能很大程度上取决于所采用的共识算法。目前主流的区块链共识算法主要有基于PoW共识算法, 基于PoS共识算法, 基于PBFT共识算法。其中基于PoW的共识算法耗能非常高，不适用于计算能力有限的无线网络环境。基于PoS的共识算法依赖于代币不适用于高动态性的无线网络。而基于PBFT的共识算法存在主节点故障问题和巨大的网络资源开销问题。因此，在这些

## 引言
### 研究背景

### 研究现状
### 研究内容
### 论文结构

## 区块链技术原理
### 区块链体系架构
#### 区块结构
#### 交易结构
#### 存储结构
##### 单链结构
##### DAG结构
### 哈希算法
### 数字签名算法
### 共识算法
#### 适用于单链的共识算法
#### 适用于DAG链的共识算法
#### 适用于两种存储结构的共识算法

## 无线网络中DAG区块链双花攻击分析
### 问题分析
#### 双花问题
#### 诚实交易广播
#### 欺诈交易广播
#### 交易确认
### 双花攻击策略
#### 一般攻击策略
#### 提前攻击策略
#### 自适应攻击策略
### 双花攻击成功概率计算
#### 随机模型
#### 一般攻击成功概率
#### 提前攻击成功概率
#### 自适应攻击成功概率
### 仿真测试
#### 网络负载测试
#### 确认区块（交易）数量测试
#### 等待区块（交易）数量测试
### 本章小结

## 无线网络中基于节点稳定度的单链共识算法
### 问题分析
#### 网络结构
#### 区块结构
#### 共识节点选取
#### 故障节点处理
#### 区块广播
### 算法思想
根据节点的稳定度，只有达到一定稳定度的节点能够打包交易，生成区块，并广播。最终谁最先广播谁就能够获得奖励。
### 算法设计
#### 稳定度排序机制
#### 共识节点选取
#### 权重系数
节点关联度、节点回退窗口大小、节点剩余电量、节点之前参与共识比值
### 算法性能分析
#### 安全性
#### 活性
### 性能测试
#### 交易吞吐量
#### 交易确认延时

## 无线网络中基于分片的单链委员会共识算法
### 问题分析
#### 网络结构
#### 区块结构
#### 共识节点选取
#### 故障节点处理
#### 区块广播
### 算法思想
### 算法设计
根据节点的坐标，将节点分到不同区域。随后根据节点的稳定度选出每一片区域的主节点。这些主节点通过通信达成共识（PBFT算法），并将共识的结果广播到所属的区域的节点。从而确保全局共识。
#### 网络分片机制
#### 委员会节点选取
#### 权重系数
节点关联度、节点回退窗口大小、节点剩余电量、节点之前参与共识比值
### 算法性能分析
#### 安全性
#### 活性
### 性能测试
#### 交易吞吐量
#### 交易确认延时

## 无线网络中基于节点稳定度的DAG链共识算法
### 问题分析
#### 网络结构
#### 单元结构
#### 见证节点选取
#### 单元广播
#### 父亲单元选择
### 算法思想
### 算法设计
#### 最优父亲单元选择机制
#### 稳定度排序机制
#### 见证节点选取机制
#### 权重系数
节点关联度、节点回退窗口大小、节点剩余电量、节点之前参与共识比值
#### 主链选择机制
### 算法性能分析
#### 安全性
#### 活性
### 性能测试
#### 交易吞吐量
#### 交易确认延时

## 无线网络中基于信誉的DAG链共识算法
### 问题分析
#### 网络结构
#### 单元结构
#### 单元广播
#### 见证节点的选取
#### 父亲单元的选取
### 算法思想
通过选择最优父亲单元可以沿着一个方向增长链。随后根据节点的信誉选出固定数量的见证者，每个交易都有一个见证者列表。相邻交易的见证者列表应该是相容的（差别不大）根据见证列表中节点的单元对于非见证列表单元的支持率来决定单元的是否稳定，从而确定一条主链，最终在DAG链上建立一个全序，防止双花。
### 算法设计
#### 父亲单元选择机制
#### 信誉排序机制
#### 见证节点选取
#### 权重系数
（节点之前参与共识的比例，节点的关联性，节点的特征向量中心性）
### 算法性能分析
#### 安全性
#### 活性
### 性能测试
#### 交易吞吐量
#### 交易确认延时

## 总结与展望
