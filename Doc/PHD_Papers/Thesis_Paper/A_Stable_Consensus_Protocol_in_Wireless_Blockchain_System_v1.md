# A Stable Consensus protoccol in Wireless Blockchain System

## Introduction

随着无线通信技术和区块链技术的高速发展，许多研究倾向于将区块链技术用于无线应用，如移动边缘计算、智能5G、车联网、物联网等。区块链技术可以在分布式环境下提供可信赖和安全的资源共享服务，受到了学术界和工业界的高度关注。区块链及其关键特性，如去中心化、持久性、匿名性和可审计性，为克服无线网络应用中存在的问题提供了新的方向，特别是当它与智能合约技术相结合时（即自动执行部署在区块链上的不可更改的数字合约）。将区块链技术融入无线网络可以促进资源共享、可信数据交互、安全接入控制与隐私保护、数据溯源、身份认证和信息监控等。

目前，大部分与无线网络相关的区块链研究都是在经典的区块链共识算法的之上提出架构或构建系统。文献[1]，作者提出了区块链的可信移动自组织云架构，并在区块链层设计了一个稳定感知的共识协议提高系统性能。在文献[2]中，作者提出了一种面向未来无线通信的区块链无线接入网架构，并研究了区块链在资源管理和网络接入中的潜在融合应用。文献[3]调研了区块链在智慧城市中的信息通信应用；文献[4]调研了将区块链和机器学习结合应用于移动通信网络系统的一些研究成果，并讨论了潜在问题及挑战。文献[5]利用通过修改无线网络的CSMA/CA协议，设计和部署适用于物联网的区块链PBFT共识算法。

许多的研究工作将区块链简单地套用于无线网络中，实质上无法完全解决其中的信任和安全问题。考虑到无线网络具有节点设备资源有限、节点可移动、网络拓扑动态变化和网络通信质量不稳定等特征，一些关于无线区块链共识算法的研究工作已经展开。文献[6]中，作者利用无线网络的通信特性设计适用于无线网络的区块链共识协议。此外文献[7]作者利用无线通信特性提出信道证明的共识算法，设计了单跳无线区块链网络协议并采用正式通用组合框架分析协议的性能。文献[8]中，作者提出了融合无线通信特性和区块链技术的适用于多跳无线网络的区块链协议。文献[9]利用无线通信协议CSMA/CA的争用机制，提出能够抵御女巫攻击的基于协作的拜占庭共识协议，适用于建立在开放无线网络中实时性要求高的物联网应用。

在本文中，我们设计一个适用于无线网络的基于竞争的区块链协议。根据无线节点生命周期短和区块链存储结构的特征，提出一种基于节点稳定性的类PoS共识算法。在这个共识算法中，拥有更高稳定性的节点将有更大概率获得出块权限，生成区块并且获得系统奖励。这样的设计可以降低共识过程的算力消耗，提高系统共识过程的稳定性和处理交易效率。此外，我们考虑敌手可以干扰节点，但是不能控制所有节点持有总财富的 $50/%$ 的财富。由于满足持久性和活性，因此该协议是安全的。持久性意味着，如果一个诚实节点宣布一个交易是有效的，那么其他诚实节点要么报告相同的结果要么报告错误信息。活性则是诚实节点提出的有效交易最终都会被添加到各诚实节点的区块链上。通过分析共识算法的通信消耗和算力消耗来进一步分析无线区块链共识算法的性能。

我们的主要贡献总结如下：
* 我们提出一种新的基于节点稳定性的适用于无线网络环境的类PoS区块链共识算法。
* 根据无线网络节点的特性和区块链存储结构的特性，我们定义了节点的稳定性。我们提出的共识算法将根据节点的稳定性来确定出块权限。
* 我们详细分析了所提出无线区块链共识算法的通信开销和算力开销，进一步分析无线区块链的性能。
* 最终，我们通过大量的仿真研究验证我们的理论分析。

本文剩余部分组成如下。下一节介绍移动无线自组织网络中最新区块链协议和共识算法最相关的工作。第三节提出我们的模型和假设。第四节详细介绍基于节点稳定性的共识协议。第五节会理论性地分析协议的正确性、活性以及高效性。第六节会给出共识协议相关的仿真结果。最后，在第七节给出相应的结论。

## Related Work

### 区块链共识协议

我们将当前的区块链共识协议可以分为几种：竞争类共识协议和协同类共识协议，在之后将简要介绍。更详细全面的区块链分类的综述可详见[10]。

竞争类共识算法中所有节点通过资源、能力、名誉、权益等证明方式来竞争获取每一轮的出块权限。工作量证明(Proof of Work)在区块链中使用最广泛的竞争类共识算法，节点通过计算资源证明来获得出块权限。众所周知的采用工作量证明作为共识算法的有比特币和以太坊。此外，典型的竞争类共识算法还有Peercoin 项目[11]中的权益证明(Proof of Stake, PoS)、 Parity 项目[12]中的权威证明(Proof of Authority, PoA)、 Burstcoin项目[13]中的空间证明 (Proof of Sapce, PoSpace)、GoChain项目[14]中的信誉证明(Proof of Reputation,PoR)等[15]。竞争类共识算法在每一轮出块节点的选择中，会设置一个竞争成功的标准，最先达到标准的共识节点获取出块权限生成区块，其他诚实的共识节点会认可这个新区块的有效性。竞争类的共识算法通常具有弱一致性，出现分叉的概率会比较高。
协同类共识算法中所有参与共识的节点通过执行局部计算和广播消息与其他节点通信协同生成每一轮的区块并达成共识。这种方法在确保活跃性和安全性的同时，为区块链提供了对拜占庭式故障的鲁棒性。典型的协同类共识算法是Fabric v0.6.0[16]中实现的拜占庭容错算法(Practical Byzantine Fault Tolerant, PBFT)。该共识算法从全网节点中选出出块节点负责创建区块，其他节点通过投票协同对区块达成全网共识。实际拜占庭容错协议无权益抵押或者资源的消耗会降低恶意节点的作恶成本，但是通过节点协作机制可以排除恶意行为对共识的影响。典型的协同类共识算法还有NEO项目[17]中提出DBFT算法、Ripple联盟链[18]项目的RPCA共识算法、Cosmos[19]中所采用的Tendermint共识算法、Algorand共识算法[20]、ELASTICO共识算法[21]、Omniledger共识算法[22]和RipidChain共识算法[23]等。协同类的共识算法通常具有强一致性，出现链分叉的概率比较小。

### 物联网中的区块链

物联网的设备通常是通过无线网络连接的，因此会面临无线网络中存在的安全和信任问题。区块链技术的出现为物联网应用，比如数据管理、访问控制、隐私保护、身份认证等，提供了新的信任和安全体系。文献[24]将区块链的技术和智能设备节点映射技术相结合，实现分布式网络中智能的设备分散自治。文献[25]提出基于雾计算、软件定义网络(SDN)和区块链的分布式云架构，实现安全、高效和低成本的大型数据流的数据管理。文献[26]开发了包含六个组件的架构，用于基于区块链的物联网访问管理。文献[27]在许可的区块链环境中使用零知识证明引入了一种基于区块链的隐私保护身份解决方案——ChainAnchor，为用户提供隐私保护服务。文献[28]将其与监管框架规定联系起来, 提供了区块链的隐私和数据保护方面的解决方案。文献[29]提出了物联
网系统中身份管理系统的要求，并研究了区块链主权身份解决方案，阐述了物联网构建完整身份管理系统的挑战。文献[30]设计了一个非中心化的身份框架——NEXTLEAP，具有使用盲签名的隐
私保护功能，并且使用身份解决方案提供的身份验证服务构建更安全的消息传递应用。

### 无线网络中的共识算法

共识算法是区块链技术的核心，我们的研究与无线网络密切相关，因此我们简要介绍无线网络共识算法的研究。文献[31,32]利用无线信道的干扰特性，提出了一种在无线通信场景中更有效地达成共识的策略。文献[33,34]利用衰落无线信道的干扰特性，提出了实现平均一致性和最大一致性的协议。文献[35]利用MAC层和多径和频率选择性信道的网络模型，为无线传感器网络设计了一种分布式一致性算法。文献[36]研究了概率广播的平均共识问题，探索了无线媒体对共识过程的影响，并扩展了非和保持算法以加速收敛。文献[37]在无线自组织网络中给出了一个抽线的物理层并且直接使用高级广播原语，提出了一个专为资源受限的无线自组织网络设计的异步拜占庭共识协议。


## Models And Assumptions

### 区块链基本定义

在无线区块链系统中，每个节点 $v$ 局部地维护一个通过区块哈希链接形成的区块链 $BC_v$。记 $B_v^i$ 是节点 $v$ 维护的区块链中的第 $i$ 个区块，而 $BC_v^{i+}$ 表示包括第 $i$ 个区块之前的区块链。每个区块中会包含多个交易，记 $Tx_i^j$ 为在区块 $B_v^i$ 中的第 $j$ 个交易，节点维护区块链的最新区块记作 $B_v^{new}$。

### 系统模型

我们考虑是一个由 $N$ 个全连接的随机分布在一个二维地理平面的节点构成的无线网络，即网络中任意两个节点在彼此的通信范围之内。系统是开放的，任意节点都不需要事先的身份授权就加入系统。每个节点配有半双工收发器，可以发送或接收消息，或感知信道，但不能同时发送和接收或发送和感知。记 $d_{ij}$ 是节点 $i,j$ 之间的欧式距离，而 $D_i(R)$ 是以节点 $i$ 为圆心 $R$ 为通信半径的圆形区域，$N_i(R)$ 表示在节点 $i$ 的通信范围中的所有节点。我们假设每个节点拥有唯一的ID，并且知道所有其他节点的身份和公钥。每个节点的传输功率可以被控制以降低干扰对通信的影响。假设节点可以在网络区域中随意移动，并且节点可以随意进入和离开这个区域。

无线网络中节点之间的通信会受到环境和干扰的影响，我们假设消息是在瑞利信道中传输。根据无线通信中小尺度衰落的特性，接收节点处的信噪比可以表示为
$$SNR = \frac{P_i hd_{ij}^{-\alpha}}{\sigma^2}$$
其中 $P_i$ 是节点 $i$ 的发射功率； $h$ 表示瑞利衰落中非负功率增益随机变量，服从指数为 $1$ 的负指数分布；$d_{i,j}$ 是节点 $i$ 到节点 $j$ 的距离；$\alpha$ 是路径损耗分数；$是\sigma^2$ 是干扰噪声功率。设定无线网络的信噪比阈值 $\beta$ 是由节点的硬件设备决定的。我们假设每个节点都能够进行物理载波监听。在一个半径为 $R$ 的圆形网络区域中，发送节点到接收节点的距离 $r$ 的密度函数为 $f(r) = \frac{2r}{R^2}$，节点传输消息平均成功的概率为 
$P_s = \int_0^R P\{SNR >\beta\}f(r)dr = \frac{2\pi\gamma}{N}\int_0^{\sqrt{\frac{N}{\pi\cdot\gamma}}}\exp\{\frac{-N\cdot r^\alpha\cdot \beta}{P_u}\}rd$。

### 敌手模型
给出相应的攻击模型

假设


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
[9] Z. Jiang, Z. Cao, B. Krishnamachari, S. Zhou and Z. Niu, "SENATE: A Permissionless Byzantine Consensus Protocol in Wireless Networks for Real-Time Internet-of-Things Applications," in IEEE Internet of Things Journal, vol. 7, no. 7, pp. 6576-6588, July 2020.
[10] Y. Xiao, N. Zhang, W. Lou, and Y. T. Hou, “A survey of distributed consensus protocols for blockchain networks,” IEEE Commun.Surv. Tutorials, vol. 22, no. 2, pp. 1432–1465, 2020.

[11] Peercoin official website. https://peercoin.net/. Jan. 2019.
[12] Parity official website. https://www.parity.io/. Jan. 2019.
[13] Burstcoin official website. https://www.burst-coin.org/. May. 2019.
[14] Gochain official website. https://gochain.io/. Jan. 2019.
[15] Proof of Reputation: A Reputation-Based Consensus Protocol for Peer-to-Peer Network. https://link.springer.com/content/pdf/10.1007%2F978-3-319-91458-9_41.pdf. Jan. 2019.
[16] Fabric official website. https://get.fabric.io/. Jan. 2019.
[17] NEO offical website. https://neo.org/. Sept. 2019.
[18] Ripple official website. https://ripple.com/. Jan. 2019.
[19] J. Kwon. Tendermint: Consensus without mining.
https://tendermint.com/static/docs/tendermint.pdf (21 August 2021, date last accessed).
[20] Y.Gilad, R. Hemo, S. Micali, et al. Algorand: Scaling Byzantine agreements for cryptocurrencies[C]. In: Proceedings of the 26th Symposium on Operating Systems Principles, Shanghai, China, October 28–31, 2017: 51–68.
[21] L.Luu, V. Narayanan, C. Zheng, et al. A secure sharding protocol for open Blockchains[C]. In: Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security. ACM, 2016: 17–30.
[22] E. Kokoris- Kogias, P. Jovanovic, L. Gasser, et al. OmniLedger: A secure, scale-out, decentralized ledger via sharding[C]. In: Proceedings of 2018 IEEE Symposium on Security and Privacy (SP 2018). IEEE, 2018: 583–598.
[23] M. Zamani, M. Movahedi, M. Raykova. RapidChain: Scaling Blockchain via full sharding[C]. In: Proceed ings of the 2018 ACM SIGSAC Conference on Computer and Communications Security (CCS 2018). Toronto, ON, Canada, October 15–19, 2018: 931–948.

[24] S. Yu, L. Kun, S. Zhou, Y. Guo, J. Zhou and B. Zhang, “A High Performance Blockchain Platform for Intelligent Devices,” In Proc.IEEE International Conference on Hot Information-Centric Networking (HotICN’18), pp.260-261, 2018. 
[25] P. Kumar, M. Chen and J. Park, “A Software Defined Fog Node Based Distributed Blockchain Cloud Architecture for IoT,” IEEE Access, vol.6, pp.115-124, 2018. 
[26] O. Novo, “Blockchain meets iot: An architecture for scalable access management in iot,” IEEE Internet of Things Journal, vol. 5, no. 2,
pp. 1184–1195, 2018.
[27] T. Hardjono, A. Pentland, “Verifiable Anonymous Identities and Access Control in Permissioned Blockchains,” pp. 9, 2016. 
[28] M. Conoscenti, A. Vetro and J. Martin, “Peer to Peer for Privacy 
and Decentralization in the Internet of Things,” In Proc. IEEE/ACM 39th International Conference on Software Engineering Companion (ICSE-C’17), pp.288-290, 2017.
[29] X. Zhu and Y. Badr, “Identity Management Systems for the Internet of Things: A Survey Towards Blockchain Solutions,” Sensors, 
vol.18, no.12, pp.4215-4215, 2018.
[30] H. Halpin, “NEXTLEAP: Decentralizing Identity with Privacy for Secure Messaging,” In Proc.International Conference on Availability,Reliability and Security (ARES’17), 2017. 
[31]M. Zheng, M. Goldenbaum, S. Stańczak and H. Yu, "Fast average consensus in clustered wireless sensor networks by superposition gossiping", Proc. IEEE Wireless Commun. Netw. Conf., pp. 1982-1987, 2012.
[32] M. Goldenbaum, H. Boche and S. Stańczak, "Nomographic gossiping for f-consensus", Proc. 10th Int. Symp. Model. Optimiz. Mobile Ad Hoc Wireless Netw., pp. 130-137, 2012.
[33] F. Molinari, S. Stańczak and J. Raisch, "Exploiting the superposition property of wireless communication for average consensus problems in multi-agent systems", Proc. Eur. Control Conf., pp. 1766-1772, 2018.
[34] F. Molinari, N. Agrawal, S. Stańczak and J. Raisch, "Max-Consensus Over Fading Wireless Channels," in IEEE Transactions on Control of Network Systems, vol. 8, no. 2, pp. 791-802, June 2021.
[35] G. Scutari and S. Barbarossa, “Distributed consensus over wireless sensor networks affected by multipath fading,” IEEE Transactions on Signal Processing, vol. 56, no. 8, pp. 4100–4106, 2008.
[36] T. C. Aysal, A. D. Sarwate, and A. G. Dimakis, “Reaching consensus in wireless networks with probabilistic broadcast,” in 2009 47th Annual Allerton Conference on Communication, Control, and
Computing (Allerton). IEEE, 2009, pp. 732–739.
[37] H. Moniz, N. F. Neves and M. Correia, "Byzantine Fault-Tolerant Consensus in Wireless Ad Hoc Networks," in IEEE Transactions on Mobile Computing, vol. 12, no. 12, pp. 2441-2454, Dec. 2013, doi: 10.1109/TMC.2012.225.

