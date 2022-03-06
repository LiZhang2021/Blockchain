# A Stable Consensus protoccol in Wireless Blockchain System

## Introduction

随着无线通信技术和区块链技术的高速发展，许多研究倾向于将区块链技术用于无线应用，如移动边缘计算、智能5G、车联网、物联网等。区块链技术可以在分布式环境下提供可信赖和安全的资源共享服务，受到了学术界和工业界的高度关注。区块链及其关键特性，如去中心化、持久性、匿名性和可审计性，为克服无线网络应用中存在的问题提供了新的方向，特别是当它与智能合约技术相结合时（即自动执行部署在区块链上的不可更改的数字合约）。将区块链技术融入无线网络可以促进资源共享、可信数据交互、安全接入控制与隐私保护、数据溯源、身份认证和信息监控等。

目前，大部分与无线网络相关的区块链研究都是在经典的区块链共识算法的之上提出架构或构建系统。文献[1]，作者提出了区块链的可信移动自组织云架构，并在区块链层设计了一个稳定感知的共识协议提高系统性能。在文献[2]中，作者提出了一种面向未来无线通信的区块链无线接入网架构，并研究了区块链在资源管理和网络接入中的潜在融合应用。文献[3]调研了区块链在智慧城市中的信息通信应用；文献[4]调研了将区块链和机器学习结合应用于移动通信网络系统的一些研究成果，并讨论了潜在问题及挑战。文献[5]利用通过修改无线网络的CSMA/CA协议，设计和部署适用于物联网的区块链PBFT共识算法。

许多的研究工作将区块链简单地套用于无线网络中，实质上无法完全解决其中的信任和安全问题。考虑到无线网络具有节点设备资源有限、节点可移动、网络拓扑动态变化和网络通信质量不稳定等特征，一些关于无线区块链共识算法的研究工作已经展开。文献[6,9]中，作者利用无线网络的通信特性设计适用于无线网络的区块链共识协议。此外文献[7]作者利用无线通信特性提出信道证明的共识算法，设计了单跳无线区块链网络协议并采用正式通用组合框架分析协议的性能。文献[8]中，作者提出了融合无线通信特性和区块链技术的适用于多跳无线网络的区块链协议。文献[9SENATOR]利用无线通信协议CSMA/CA的争用机制，提出能够抵御女巫攻击的基于协作的拜占庭共识协议，适用于建立在开放无线网络中实时性要求高的物联网应用。

在本文中，我们设计一个适用于无线网络的基于竞争的区块链协议。根据无线节点生命周期短和区块链存储结构的特征，提出一种基于节点稳定性的类PoS共识算法。在这个共识算法中，拥有更高稳定性的节点将有更大概率获得出块权限，生成区块并且获得系统奖励。这样的设计可以降低共识过程的算力消耗，提高系统共识过程的稳定性和处理交易效率。此外，我们考虑敌手可以干扰节点，但是不能控制所有节点持有总财富的 $50/%$ 的财富。由于满足持久性和活性，因此该协议是安全的。持久性意味着，如果一个诚实节点宣布一个交易是有效的，那么其他诚实节点要么报告相同的结果要么报告错误信息。活性则是诚实节点提出的有效交易最终都会被添加到各诚实节点的区块链上。通过分析共识算法的通信消耗和算力消耗来进一步分析无线区块链共识算法的性能。

我们的主要贡献总结如下：
* 我们提出一种新的基于节点稳定性的适用于无线网络环境的类PoS区块链共识算法。
* 根据无线网络节点的特性和区块链存储结构的特性，我们定义了节点的稳定性。我们提出的共识算法将根据节点的稳定性来确定出块权限。
* 我们详细分析了所提出无线区块链共识算法的通信开销和算力开销，进一步分析无线区块链的性能。
* 最终，我们通过大量的仿真研究验证我们的理论分析。

本文剩余部分组成如下。下一节介绍移动无线自组织网络中最新区块链协议和共识算法最相关的工作。第三节提出我们的模型和假设。第四节详细介绍基于节点稳定性的共识协议。第五节会理论性地分析协议的正确性、活性以及高效性。第六节会给出共识协议相关的仿真结果。最后，在第七节给出相应的结论。

## Related Work

### 区块链共识协议

我们当前区块链共识协议可以分为几种：基于工作量证明的共识协议、基于权益证明的共识协议、混合分布式一致性协议的共识协议以及其他的共识算法。

基于工作量证明的区块链共识算法中，参与共识的节点通过展示他们的计算算力的消耗来竞争出块权限。工作量证明最早由C.Dwork和M.Naor[18]在1992年提出，用来解决垃圾邮件问题.该机制要求邮件在被发送之前必须找到某个数学难题的答案来证明发送者确实执行了一定量的工作。A.Back在1997年提出，并在2002年正式发表的Hashcash [19]通过寻找哈希函数原像实现工作量证明。在1999年，M.Jakobsso[20]正式提出了工作量证明的概念。这些工作都为比特币的共识机制奠定了坚实的基础。以太坊可以提供一个图灵完备的以太坊虚拟机并且采用改进的工作量证明共识算法——Ethash。此外，采用基于工作量证明共识算法的区块链协议的有Bitcoin-NG、Fruitchain等。

基于权益证明的的共识算法中参与节点根据拥有资产的比例来决定成为下一个出块者的概率。因此，这类共识算法依赖参与节点的初始代币。由S.King和S.Nadal[28]提出的点点币首次引入了权益证明共识算法，根据参与节点持有代币的币龄来选择生成新区块的节点。V.Buterin等人[33]提出的Casper FFG是用于以太坊的基于PoS共识算法。区块产生仍然依靠以太坊的Ethash工作量证明算法，每隔50个区块出现一个检查点，验证者通过权益证明共识算法对检查点完成最终确定，确保系统的安全性。A.Kiayias等人[35]提出了一种新的基于权益证明的共识算法Ouroboros，根据参与节点持有的股权来随机选举出块节点。P.Daian等人[38]提出的Snow White是基于权益证明的可重配置共识算法。该协议提出了一种保证安全的腐败延迟机制，确保节点离线、候选者节点选择机制被敌手偏置和腐蚀时系统的安全性。

基于委员会的混合共识协议是将经典分布式一致性算法与当前的区块链共识算法相结合，即采用PoW或PoS的方式选举特定的委员会，在委员会内部运行经典分布式共识算法生成区块。根据委员会的数量可以分为单一委员会混合共识协议和多委员会混合共识协议。典型的采用单一委员会混合共识协议的区块链有PeerCensus、Byzcoin、Solida、Algrand等；采用多委员会混合共识机制的区块链协议有ELATICO、Omniledger、Chainspace、RapidChain等。

除了以上三种区块链共识算法的分类以外，许多研究者提出一些其他区块链共识算法。针对工作量证明共识算法耗能大的问题，一些替代的共识算法被提出，比如Proof of space、proof of storage(proof of capacity）、Proof of elapsed time。考虑到权益证明共识算法需要持有股份的特点，提出基于节点信用的Proof of reputation。为了降低区块链节点间同步沟通的成本，Ripple采用的RPCA算法利用验证节点的可信任节点名单对交易投票
和对区块进行投票最终达成一致。

### 物联网中的区块链



### 无线网络中的区块链协议

目前，大部分与无线网络相关的区块链研究都是在经典的区块链共识算法的之上提出架构或构建系统。例如，在车联网上建立具有区块链安全性的通信架构[引用几篇车联网区块链相关的文章]。在边缘云上构建区块链系统确保安全、公平、高效地实现资源分配[引用几篇边缘计算区块链相关的文章]。在其他物联网领域中对区块链地研究也是提出新的架构系统。比如，[ChainSplitter]

有一些区块链研究是根据无线网络广播特性提出可以在具有一定时间复杂度的区块链系统中达成共识。例如，BLOWN [] 和 wChain [] 分别被提议为单跳和多跳无线区块链协议。此外，[Consensus in wireless blockchain system] 中提出了一种基于 SINR 模型的共识协议，在单跳无线网络中可以在 O(log n) 时间步内获得共识。然而，以前的工作只考虑达成一次共识。但是，区块链系统中的共识需要通过参与节点重复获得。只讨论共识协议的单次共识的效率对于无线网络的区块链共识算法的研究可能会稍显不足。

### 移动无线自组织网络的区块链协议

## Models And Assumptions

问题定义

给出相应的网络模型

给出相应的攻击模型


## The Stable Consensus Protocol
介绍共识协议的框架：
首领选举阶段、
区块提出阶段、
区块验证阶段、
链更新阶段、
区块链系统中共识算法的性质







## Protocol Analysis

分析共识协议的正确性、高效性和安全性


## Simulation Result
测试不同区块大小时，固定网络大小时，区块确认时延
测试吞吐量

## Conclusion

得出结论


## References

[1] Z. Jiao, B. Zhang, L. Zhang, M. Liu, W. Gong and C. Li. A Blockchain-Based Computing Architecture for Mobile Ad Hoc Cloud, in IEEE Network, vol. 34, no. 4, pp. 140-149, July/August 2020.
[2] X. Ling, J. Wang and T. Bouchoucha et al. Blockchain radio access network (B-RAN): Towards decentralized secure radio access paradigm. IEEE Access 2019; 7: 9714–23.
[3] J. Xie, H. Tang and T. Huanget al. A survey of blockchain technology applied to smart cities: Research issues and challenges. IEEE Commun Surv Tutorials 2019; 21: 2794–830.
[4] Y. Liu, F.R. Yu and X. Li et al. Blockchain and machine learning for communications and networking systems. IEEE Commun Surv Tutorials 2020; 22: 1392–431.
[5] J. Mišić, V. B. Mišić, X. Chang and H. Qushtom, "Adapting PBFT for Use With Blockchain-Enabled IoT Systems," in IEEE Transactions on Vehicular Technology, vol. 70, no. 1, pp. 33-48, Jan. 2021
[6] Q. Xu, Y. Zou, D. Yu, M. Xu, S. Shen, F. Li. Consensus in Wireless Blockchain System, in WASA, 2020.
[7]	M. Xu, F. Zhao, Y. Zou, C. Liu, X. Cheng, F. Dressler. BLOWN:A Blockchain Protocol for Single-Hop Wireless Networks under Adversarial SINR, in CoRR abs/2103.08361, 2021.
[8] M. Xu, C. Liu, Y. Zou, F. Zhao, J. Yu and X. Cheng, "wChain: A Fast Fault-Tolerant Blockchain Protocol for Multihop Wireless Networks," in IEEE Transactions on Wireless Communications, vol. 20, no. 10, pp. 6915-6926, Oct. 2021, doi: 10.1109/TWC.2021.3078639.
[9] Y. Zou, M. Xu, J. Yu, F. Zhao and X. Cheng, "A Fast Consensus for Permissioned Wireless Blockchains," in IEEE Internet of Things Journal, doi: 10.1109/JIOT.2021.3124022.


