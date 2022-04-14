# A Stable Consensus protoccol in Wireless Blockchain System

## 1. Introduction

随着无线通信技术和区块链技术的高速发展，许多研究倾向于将区块链技术用于无线应用，如移动边缘计算、智能5G、车联网、物联网等。区块链技术可以在分布式环境下提供可信赖和安全的资源共享服务，受到了学术界和工业界的高度关注。区块链的关键特性，如去中心化、持久性、匿名性和可审计性，为克服无线网络应用中存在的问题提供了新的方向，特别是当它与智能合约技术相结合时（即自动执行部署在区块链上的不可更改的数字合约）。将区块链技术融入无线网络可以促进资源共享、可信数据交互、安全接入控制与隐私保护、数据溯源、身份认证和信息监控等。

目前，无线网络相关的区块链研究有在经典的区块链共识算法的之上提出架构或构建系统。文献[1]，作者提出了区块链的可信移动自组织云架构，并在区块链层设计了一个稳定感知的共识协议提高系统性能。在文献[2]中，作者提出了一种面向未来无线通信的区块链无线接入网架构，并研究了区块链在资源管理和网络接入中的潜在融合应用。文献[3]调研了区块链在智慧城市中的信息通信应用；文献[4]调研了将区块链和机器学习结合应用于移动通信网络系统的一些研究成果，并讨论了潜在问题及挑战。文献[5]通过修改无线网络的CSMA/CA协议，设计和部署适用于物联网的区块链PBFT共识算法。此外，还有一些研究在考虑到无线网络具有节点设备资源有限、节点可移动、网络拓扑动态变化和网络通信质量不稳定等特征，将无线网络的通信特性与区块链协议相结合，提出新的无线区块链协议。文献[6]中，作者利用无线通信特性设计新的无线区块链共识算法。此外，文献[7]中，作者提出基于无线信道证明的区块链共识算法，设计了单跳无线区块链网络协议并采用正式通用组合框架分析协议的性能。文献[8]中，作者利用无线通信构建通信骨架的方式提出了适用于多跳无线网络的区块链协议。文献[9]利用无线通信协议信道争用机制，提出能够抵御女巫攻击的基于协作的拜占庭共识协议，适用于建立在开放无线网络中实时性要求高的物联网应用。这些共识协议中，抽零节点需要承担比较重要的协商作用，如果在共识过程中，首领节点离开或者出现故障时，将无法达成共识，最终导致共识失败。

在本文中，我们设计一个适用于无线网络的稳定的区块链共识协议。根据无线网络节点生命周期短和区块链存储结构的特征，提出一种基于节点稳定性的类PoS共识算法。在这个共识算法中，拥有更高稳定性的节点将有更大概率获得出块权限生成区块。通过节点的稳定度随机选举首领可以降低共识过程中首领选举阶段的算力消耗，同时也能够以较大概率选举出优质节点成为首领，提高系统共识过程的稳定性和处理交易效率。为了提高共识过程的鲁棒性，我们将门限BLS签名技术与区块链共识协议相结合实现首领节点与共识协商过程解耦。只要收集到足够数量的共识结果签名，所有参与共识的节点都可以独立计算共识结果的聚合签名，验证签名成功后发布最终共识结果。不需要通过通信协商达成共识，这可以降低由于节点故障或者链路不稳定导致无法达成共识的风险。在共识协议中首领节点只负责提出区块，不需要与其他参与共识的节点协商对区块达成一致，减少共识协商过程中的二次通信。我们的共识协议是满足持久性和活性，因此该协议是安全的。持久性意味着，如果一个诚实节点宣布一个交易是有效的，那么其他诚实节点要么报告相同的结果要么报告错误信息。活性则是诚实节点提出的有效交易最终都会被添加到各诚实节点的区块链上。通过分析共识算法的通信消耗和算力消耗来进一步分析无线区块链共识算法的性能。

我们的主要贡献总结如下：
* 根据无线网络节点的特性和区块链存储结构的特性，我们定义了节点的稳定性。我们提出的共识算法将根据节点的稳定性来确定出块权限。
* 我们提出一种新的适用于无线网络环境的基于节点稳定性的类PoS区块链共识算法。通过根据节点的稳定度选举出优质的出块节点，降低节点作恶的机会，提高系统的安全性。
* 我们详细分析了所提出无线区块链共识算法的通信开销和算力开销，进一步分析无线区块链的性能。
* 最终，我们通过大量的仿真研究验证我们的理论分析。

本文剩余部分组成如下。下一节介绍区块链共识协议和无线区块链共识协议相关的工作。第三节提出我们的模型和假设。第四节详细介绍基于节点稳定性的共识协议。第五节会理论性地分析协议的正确性、活性以及高效性。第六节会给出共识协议相关的仿真结果。最后，在第七节给出相应的结论。

## 2. Related Work

### 2.1 区块链共识协议

我们将当前的区块链共识协议可以分为：基于资源证明的共识协议和基于协商的共识协议。更详细全面的区块链分类的综述可详见[10]。

基于资源证明的共识协议中参与共识的节点通过资源、能力、名誉、权益等证明方式来竞争获取每一轮的出块权限。根据资源的类型可以分为基于物理资源证明的共识协议和基于虚拟资源证明的共识协议。其中，典型基于物理资源证明的共识算法是工作量证明(Proof of Work)。参与共识的节点通过消耗的计算资源证明来获得出块权限。采用工作量证明作为共识算法的有比特币和以太坊。此外，基于物理资源证明的共识算法还有Burstcoin项目[13]中的空间证明 (Proof of Sapce, PoSpace)，共识参与者通过占用的内存或磁盘空间来竞争出块权限；以及燃烧证明（Proof of Burn），共识参与节点通过烧毁另一种“货币”， 比如比特币，来获得生成区块的权限。物理资源证明共识算法需要通过消耗物理资源来获得生成区块的权限，这个过程会导致大量资源的浪费，对环境并不友好。

虚拟资源证明共识算法不需要消耗实际的资源，而是通过虚拟资源来竞争出块权限。典型的虚拟资源证明的共识算法是Peercoin 项目[11]中的权益证明(Proof of Stake, PoS)，参与共识的节点根据所持有的股份作为选举成为出块节点的权限证明，股份越多的节点，成为出块节点的概率就越大。此外，虚拟资源证明的共识算法有 Parity 项目[12]中的权威证明(Proof of Authority, PoA)，参与共识的节点通过完成一个身份认证过程获得出块权限。；GoChain项目[14]中的信誉证明(Proof of Reputation,PoR)[15]是授权证明的升级，共识参与节点需要拥有足够重要的信誉才能获取出块权限。PoA和PoR在共识过程都需要可信验证节点签名授权，因此总是伴随这一些激励机制和经济惩罚策略。

基于协商共识算法中所有参与共识的节点通过执行局部计算和广播消息与其他节点通信协商对提出的区块达成共识。这种方法可以使得区块链具有很好的活性、安全性和拜占庭攻击抗性。典型的协商共识算法是Fabric v0.6.0[16]中实现的拜占庭容错算法(Practical Byzantine Fault Tolerant, PBFT)。该共识算法从全网节点中选出出块节点负责创建区块，通过与其他节点投票协商对区块达成全网共识。实际拜占庭容错协议无权益抵押或者资源的消耗会降低恶意节点的作恶成本，但是通过节点协作机制可以排除恶意行为对共识的影响。典型的协商共识算法还有NEO项目[17]中提出DBFT算法，授权的共识节点将获取出块权限，并通过投票协商对区块达成共识；Ripple联盟链[18]项目的RPCA共识算法中通过一个信任节点列表对交易和区块投票协商达成一致；Cosmos[19]中所采用的Tendermint共识算法、Algorand共识算法[20]、ELASTICO共识算法[21]、Omniledger共识算法[22]和RipidChain共识算法[23]等都是通过对出块节点生成的区块投票协商达成共识。协商类共识依赖于可信的消息传输模型，消息传输都是端到端的，忽略了一对多的消息传输模型，比如无线网络中的广播操作。因此，协商类的共识算法通常需要可靠的消息传输此模型以及具有较高的通信时间复杂度。比如，拜占庭共识算法的时间复杂度为 $O(n^2)$，当节点数量增加时，共识时延会急剧提升，性能会迅速下降。

### 2.2 无线网络中的共识算法

目前，一些关于共识算法的研究的基于无线信道的。通过利用无线网络的广播操作和无线信道的干扰特性，设计适用于无线网络的共识协议，并且提升共识算法的效率。文献[31,32]利用无线信道的干扰特性，提出了一种在无线通信场景中有效地达成共识的策略。文献[33,34]利用衰落无线信道的干扰特性，提出了实现平均一致性和最大一致性的协议。文献[35]利用多径和频率选择性信道的网络模型，为无线传感器网络设计了一种分布式一致性算法。文献[36]研究了概率广播的平均共识问题，探索了无线媒体对共识过程的影响，并扩展了非和保持算法以加速收敛。文献[37]在无线自组织网络中给出了一个抽象的物理层并且直接使用高级广播原语，提出了一个专为资源受限的无线自组织网络设计的异步拜占庭共识协议。通过利用无线网络的广播操作，可以在较低时间复杂度下实现网络共识。文献[6]中，作者提出了一个基于SINR模型的共识协议，在单跳无线网络中可以在 $O(\log n)$ 时间中达成共识。文献[7]中，作者提出基于无线信道证明的区块链共识算法，设计了单跳无线区块链网络协议，可以在无线网络中高效地对区块达成一致。文献[8]中，作者利用无线通信构建通信骨架的方式提出了适用于多跳无线网络的区块链协议，能够快速地完成数据收集并且对提出的区块达成共识。

### 2.3 门限签名方案

门限签名方案[40]可以帮助共识协议参与方在通信不稳定的无线网络中达成最终共识。参与者利用自己的私钥对共识结果进行签名，通过将不同参与者对共识结果的签名聚合成一个单一的签名，最终利用聚合公钥对共识结果进行验证并达成共识。

BLS签名方案[38]是利用循环群和双线性映射的特性来构造聚合签名，实现多方签名和验证。BLS签名方案中，记 $G_{1}$ 是阶为 $p$ 的循环群，且生成元是 $g_{1}$, $H:\{0, 1\}^{*}\rightarrow G_{1}$ 是一个安全Hash函数，公开参数 $(G_{1}, g_{1}, p, H)$ 是全局信息。记参与者 $i$ 的私钥为  $pri_{key}^{i}$，计算得到公钥 $pub_{key}^{i} = pri_{key}^{i}\times G_{1}$，Hash计算要签名的消息 $MSG$ 的确保消息的完整性 $H(MSG)^{i}$，用私钥签名得到 $sign_{i} = pri_{key}^{i}\times H(MSG)^{i}$。验证者可以通过签名者的公钥验证 $(g_{1}, pub_{key}^{i}, H(MSG), sign_{i})$ 是否有效。

门限BLS签名方案源于BLS签名方案，由于聚合签名的生成与BLS签名方案是一致且最终恢复聚合签名的结果是一个无需交互的计算过程，因此门限BLS签名方案的工作方式是非交互式和分布式的。门限签名方案由密钥生成算法、签名生成算法和验证算法。密钥生成算法使用分布式密钥生成协议[39]向参与者分发相应密钥的方法。签名生成算法包含了一个最终签名生成协议，主要是生成参与者的签名和根据多个参与者的签名计算得到一个完整的签名，最后输出是组合签名的“拉格朗日插值”，签名验证算法使用分布式密钥生成协议生成的组公钥对最终签名结果进行验证。

为了确保在无线共识网络中能达成共识，我们将一个 $t-n$ BLS门限签名方案与共识协议相结合。因此，我们的共识协议使得即使部分参与者对区块共识结果的签名丢失，也能最终达成共识。由于聚合签名可以由任意参与者执行，因此所有参与者都能发布最终共识结果，极大地降低了由于出块节点故障或者链路不稳定导致无法达成共识的风险。出块节点只负责提出区块，不需要与其他参与者协商达成一致，从而极大地减少了共识过程中的通信消耗。


## 3. Models And Assumptions

### 3.1 网络模型

在本文中，我们考虑了一个由 $N$ 个任意部署在通信区域的节点的集合 $V$ 组成的无线网络。在实际场景中，这样的网络可以是构建在一组无人机之间或者车联网之间。所有的网络节点之间是全连接的，即网络中任意一对节点都在彼此的无线通信范围之内。每个节点具有一个半双工发射器可以发送和接收消息或者感知信道，但是不能同时收发消息或者同时发送和感应信道。假设每个节点知道其他节点的ID、位置以及公钥。我们假设每个节点进入之后会分配得到一个密钥对，由分布式密钥生成协议分发给各个节点。

### 3.2 区块链基本定义

在无线区块链系统中，我们假设每个节点局部地维护一个通过区块哈希链接形成的区块链，每个区块中会包含多个交易，我们分别通过 $BC, B, tx$ 记作区块链、区块和交易。交易由一组引用其他交易的输入和输出组成，以及由其发行者生成的签名以证明其有效性。区块的数据结构包括区块头和区块体，区块体主要包括原始的交易信息，区块头则记录区块的基本信息，包括区块ID，父区块Hash、区块Hash、区块最终签名和时间戳等信息。

### 3.3 干扰模型

无线网络中节点之间的通信会受到环境和干扰的影响，我们假设消息是在瑞利信道中传输。根据无线通信中小尺度衰落的特性，接收节点处的信噪比可以表示为
$$SNR = \frac{P hr^{-\alpha}}{\sigma^2}$$
其中 $P$ 是节点的发射功率； $h$ 表示瑞利衰落中非负功率增益随机变量，服从指数为 $1$ 的负指数分布；$r$ 是两节点之间的距离；$\alpha$ 是路径损耗指数；$是\sigma^2$ 是干扰噪声功率。设定无线网络的信噪比阈值 $\beta$ 是由节点的硬件设备决定的。我们假设每个节点都能够进行物理载波监听。在一个半径为 $R$ 的圆形网络区域中，发送节点到接收节点的距离 $r$ 的密度函数为 $f(r) = \frac{2r}{R^2}$，节点传输消息平均成功的概率为 
$P_s = \int_0^R P\{SNR >\beta\}f(r)dr = \frac{2\pi\gamma}{N}\int_0^{\sqrt{\frac{N}{\pi\cdot\gamma}}}\exp\{\frac{-\sigma^2\cdot r^\alpha\cdot \beta}{P}\}rdr,$
当 $\alpha = 2$ 时，节点传输成功的平均概率为 $P_s = \frac{P\cdot \pi\cdot \gamma}{\sigma^2\cdot \beta\cdot N}\cdot(1 - \exp\{-\frac{\sigma^2\cdot \beta\cdot N}{P\cdot \pi\cdot \gamma}\})$。

### 3.4 敌手模型

假设存在敌手可以自由地进出网络，并且最多能够控制网络中不超过 $50\%$ 的金额，敌手的恶意行为如下：
* 敌手节点可以发起女巫攻击，即伪造多个身份在共识过程中获益；
* 假设敌手可以在任意时刻制造噪声干扰其他诚实节点的消息传输；
* 假设敌手可以发起阻塞攻击(Jamming Attack)，在长度为 $T$ 的时间区间内，敌手最多可以发起 $(1-\epsilon)T, 0<\epsilon\leq 1$ 次阻塞攻击，即在 $T$ 轮中敌手最多可以阻塞 $(1-\epsilon)T$ 轮。


在本文中，我们说一个事件 $E$ 有很高概率发生,如果对任意 $c\geq 1$，事件 $E$ 发生的概率为 $1 - \frac{1}{N^{c}}$。

## 4. The Stable Consensus Protocol

在本小节，我们首先介绍稳定共识协议的概览，之后介绍协议的细节。

### 4.1 共识协议概览

在本小节中，我们主要提出稳定共识协议的概述，并且通过描述节点功能更加简洁的表述稳定协议。

稳定共识协议是在无线网络环境下工作的，参与共识的节点通过提交一个女巫攻击抵抗证明，即质押一部分金钱获得在系统中的活动时间，可以加入系统。这笔押金会存放在一个虚拟账户中，任何人不能取出，除非本人通过一个解质押的方式才能取出属于自己的质押金额。这个质押机制可以有效的防止敌手发起女巫攻击。

稳定的无线区块链共识协议是允许数百个节点参与协商一致过程，最终提供稳定的共识过程和较低的共识时延。共识协议是按顺序进行的。在每一轮中，随机选举一个出块节点，随后每个共识节点对区块进行一次投票，其中每个共识节点对于区块Hash的签名被计数为对区块有效的一次投票。如下图所示，我们的共识协议主要包括：
![](Fig_1.png)
* **随机数生成**：节点通过一个分布式随机生成方案根据前一轮确认的区块独立地生成一个随机数 $[0, 1)$ 区间的随机数；
* **出块节点选举**：对当前所有参与共识的节点进行统一排序，根据节点的稳定度构建轮盘。基于构建的轮盘和生成的随机数选举出块节点
* **区块生成**：出块节点将打包交易生成一个区块，之后将区块并广播给网络中地其他共识节点；
* **区块验证**：接收到新区块之后，节点会验证区块的有效性。如果认为区块是有效的，节点将会对区块Hash签名，并将签名广播；
* **区块确认**：节点将确认区块：
  * 节点收集到足够的签名之后，通过一个聚合签名恢复方案将一定数量的区块Hash签名聚合成一个最终签名；
  * 节点即受到一个区块Hash的最终签名。
* **链更新阶段**：当节点确认区块之后，将新区块添加到本地主链上，并开始新的一轮共识。否则

Algorithm 1表示了稳定共识协议每一轮共识所需要执行的流程。每个阶段距离的细节将会在之后的小节中详细介绍。我们解决了出块节点的选举、区块验证和最终确认面临的挑战，确保了系统的安全性。我们的协议确保了即使存在敌手，也能顺利的运行。
![](./consensus.png)

### 4.2 稳定共识协议细节

在这一小节，我们将详细介绍我们的共识算法的设计细节。

#### 4.2.1 门限签名方案

在系统运行共识协议之前，系统通过一种安全的分布式密钥生成算法，为每个参与共识的节点生成和分配密钥和聚合公钥。我们的共识协议采用门限BLS签名方案的三个相关函数：签名生成函数生成部分签名；聚合签名恢复函数通过一定数量的部分签名重构完整的签名；签名验证函数验证每个部分签名和完整签名。每个节点在验证区块成功之后通过密钥对区块Hash签名，生成一个部分签名。其他节点可以通过公钥验证其他节点生成的签名。当节点收集到超过门限的签名数量之后，会聚合生成一个完整签名，所有节点都可以通过聚合公钥对完整签名进行验证。

#### 4.2.2 分布式随机生成

分布式随机数生成协议应该允许共识节点通过在系统中输入相同的输入后最终共识节点的产生唯一的、随机的、可验证的输出。为了满足这些需求，分布式随机生成协议是建立在安全可靠的BLS签名方案之上的，在 $n$ 个共识节点中即使存在 $\lfloor\frac{n}{2}\rfloor$ 个恶意节点也能够正常运行。

当前轮的共识节点接收到区块Hash的完整签名 $sign_{final}^{r}$ 之后，将执行分布式随机数生成协议来产生下一轮的随机数 $Rds^{r+1} \in [0, 1)$。我们将使用当前轮的区块Hash $B_{Hash}^{r}$ 与完整签名 $sign_{final}^{r}$ 结合作为随机输入，最后得到新一轮的随机数:
$$Rds^{r+1} = \frac{Hash(B_{Hash}^{r}||sign_{final}^{r})}{2^{len(Hash(B_{Hash}^{r}||sign_{final}^{r}))}}$$

当绝大多数的共识节点都维护相同的区块链并且都是诚实的时候，门限签名方案的阈值总是能达到。因此，在每一轮中最终总是能够恢复完整签名，这个完整签名可以由任意诚实的共识节点生成，或者有很高概率能够接收到。

此外，分布式随机数生成协议的输出是不可预测且唯一的。虽然区块Hash $B_{Hash}^{r}$ 是一个预先知道的，但是完整签名 $sign_{final}^{r}$ 在聚合产生之前是不可知的，不可以在事先预估得到。即使存在节点首先恢复出完整签名，但是节点是不可能篡改完整签名的。因此，新一轮随机数 $rds^{r+1}$ 的生成是基于相同的、可验证的输入计算的，确保最终输出是随机且唯一的。

分布式随机数生成协议是非交互式的，参与共识的节点不需要通信便能够进入新的一轮共识。一旦节点生成或接收到完整签名 $sign_{final}^{r}$，就会立刻确认区块并将区块添加到本地区块链上。同时，节点可以根据确认的区块Hash $B_{Hash}^{r}$ 和完整签名 $sign_{final}^{r}$ 自主生成新一轮的随机数 $Rds^{r+ 1}$，直接开始新一轮共识进程。

共识协议通过一个激励机制可以提高节点愿意签名区块Hash的积极性。最先聚合生成完整签名的部分签名集合的所有节点将获得部分奖励。这个机制不仅可以激励节点参与签名，更可以激励节点产生完整签名之后尽快将结果广播给其他节点，从而提高共识的效率。

#### 4.2.3 出块节点选举

每个节点在进入系统之后通过分布式密钥生成协议获取自己的密钥对 $<sk_{i}, pk_{i}>$ 和其他共识节点的公钥 $<pk_{1},\cdots, pk_{i-1}, pk_{i+1}, \cdots, pk_{n}>$ 以及聚合公钥 $pks$，用于签名和验证签名。当得到所有共识节点的公钥之后，节点可以通过对所有的共识节点采用基于公钥Hash值进行排序。这种方式可以使得全部参与共识的节点拥有相同的序列。

在稳定区块链共识协议中，主要根据节点的稳定度来选举出块节点。新节点加入系统时，通过保证金质押获得有限的活动时间，活动的时长与交付的保证金成正比。

假设节点 ${\rm Node}_{v}$ 在区块链系统中的<font color=red>剩余活动时间</font>为 $T_{v}$，则所有共识节点的剩余活动时间之和为 $\sum_{v}T_{v}$。定义节点 ${\rm Node}_{v}$ 的 **<font color=red>剩余活动时间比值</font>** 为
$$\rho_{v} = \frac{T_{v}}{\sum_{v}T_{v}}$$

假设在最近的 $K$ 个确认区块中，由节点 ${\rm Node}_{v}$  生成的区块数量为 $N_{v}$。定义节点 ${\rm Node}_{v}$ 的 **<font color=red>共识比值</font>** 为
$$r_{v}=\frac{N_{v}}{K}$$

定义节点 ${\rm Node}_{v}$ 的 **<font color=red>稳定度</font>** 为 
$$S_{v}=\alpha\times \rho_{v}+\beta\times r_{v}\qquad(\alpha+\beta=1,\ \alpha\geq 0,\ \beta\geq 0)$$
其中，$\alpha$ 为剩余活动时间比权重系数，$\beta$ 为共识比权重系数，可根据偏好设置。在系统运行初期，当确认区块数量不足 $K$ 个时，记节点的共识比为 $r_{v}=0$。此时，节点的稳定度主要受节点的剩余活动时间的影响。

在稳定区块链共识协议中，节点 ${\rm Node}_{v}$ 被选为出块节点的概率为
$$p_{v}=\frac{S_v}{\sum_{v}S_v}$$
根据节点的稳定度决定节点被选中的概率，稳定度越高的节点越容易被选中。通过节点的稳定度和统一排序，可以构建一个轮盘。合法的出块节点将会从节点轮盘中选出。共识节点根据轮随机数 $Rds^{r}$ 从构建的轮盘中决定出块节点的索引BPI。记 $S_{i}$ 是节点 $i$（$i=0,\dots,N-1$）的稳定度，所有节点的稳定度之和为 $S =\sum_{i=1}^{N}S_{i}$ ，那么节点 $i$ 被选中的概率为 $p_{i}=\frac{S_{i}}{S}$ 且有 $\sum_{i=1}^{N}p_{i}=1$。为了确定被选中的节点，将区间 $[0, 1)$ 分为连续的多个区间
$$[\sum_{k=1}^{i}p_{k}, \sum_{k=1}^{i+1}p_{k}),\ i=0,\dots,N-1.$$

出块节点的在轮盘中的索引BPI是通过将区块Hash和完整签名作为输入计算得到一个随机值 $Rds^{r}$，根据这个值所在的区间确定的，计算如下：
$$ BPI = \{i | Rds^{r} \in [\sum_{k=1}^{i}p_{k}, \sum_{k=1}^{i+1}p_{k})\}$$

出块节点的选择是基于 $Rds^{r}$，这个数是随机、唯一和可验证的。因此，出块节点的选择也是安全随机的，并且出块节点的确定也是每个节点独立完成，不需要进行任何的消息交互。由于所有共识节点计算BPI的输入的相同的，因此最终计算结果也是唯一。通过出块节点在区块上的签名和出块节点的公钥可以验证出块节点的合法性。

当节点维护的区块链或者剩余活动存在差异时，最终的出块节点的选举并不会出现较大的偏差，即敏感度并不高。

记 $S_{v} = \alpha\times\frac{T_{v}}{\sum_{i \in N}T_{i}} + \beta\times\frac{N_{v}}{K}$，记 $S_{v}' = \alpha\times\frac{T_{v}+ \Delta T_{v}}{\sum_{i \in N}T_{i} + \Delta T_{v}} + \beta\times\frac{N_{v} + \Delta N_{v}}{K}$, 那么 $||S_{v}' - S_{v}|| = ||\alpha\frac{\sum_{i \in N}T_{i}\Delta T_{v} - T_{v}\Delta T_{v}}{\sum_{i \in N}T_{i}(\sum_{i \in N}T_{i}+\Delta T_{v})} + \beta\frac{\Delta N_{v}}{K}||\leq ||\frac{\Delta T_{v} }{\sum_{i \in N}T_{i}+\Delta T_{v}} + \frac{\Delta N_{v}}{K}|| \ll \Omega(1)$

因此，当节点记录的剩余活动时间和共识区块数量存在些许误差时，对于最终稳定性的影响不会太大，节点被选中的概率是对于这两个度量指标的敏感度也不会特别大。因此，诚实节点选中不同出块节点的概率是非常低的。为了尽可能使系统中节点维护相同的区块链，在每次同时开始之前，节点会执行一次区块链同步操作。节点会随机请求几个邻节点的区块链信息，最终同步拥有共同链前缀且有最长有效区块链。

当节点被选中为当前轮的出块节点之后，出块节点将打包交易生成区块，区块分为区块头和区块体。区块体主要是存储的交易元数据，区块头可以用一个元组表示 $(R, Hash_{pre}, inf_{trans}, B_{Hash}, BPI,sign_{final})$，其中 $R$ 是当前的轮数，$Hash_{pre}$ 是前一个区块的Hash，$inf_{trans}$ 是存储在区块体中交易的信息，$BPI$ 是出块节点的索引，$B_{Hash}$ 是区块的Hash。随后，出块节点将通过签名区块Hash和处理区块最终将完整签名 $sign_{final}$ 添加到区块中。

#### 4.2.4 区块验证与确认

我们通过无线网络广播的方式将出块节点生成的区块和区块Hash的部分签名传输给其他共识节点。当节点接收到新的区块消息时会检查区块的有效性和验证出块节点对区块Hash签名。共识节点通过验证以下组件的有效性来验证区块的有效性：
* **父区块哈希** $Hash_{pre}$：新区块的父区块哈希必须与节点维护的当前最新区块链的最后一个区块的哈希相同；
* **交易信息** $inf_{trans}$：验证交易列表的基本信息是否有效；
* **交易**：检查区块中的所有交易是否都是有效的，如果存在无效交易，则认为区块是无效的；
* **部分签名**：验证区块Hash的签名是否有效。验证区块Hash的有效性可以确保区块完整性，验证区块Hash的签名可以确定出块节点的合法性，节点可以通过签名节点的公钥来确定部分签名的有效性。

如果以上条件都满足后，节点验证区块的有效性都成功，会对区块Hash签名并广播部分签名给其他共识节点。当共识节点收集到 $\lceil\frac{n}{2}\rceil$ 个对区块Hash的部分签名时，区块被验证成功。这些部分签名可以聚合恢复成一个完整签名，此时证明区块被确认。

如前所述，节点只需要单向传输部分签名，并不需要其他节点的回复，这极大地减少了节点之间的通信。此外，聚合多个部分签名生成完整签名可以由任意共识节点完成，即区块的确认过程是完全去中心化的、无首领的，这极大地降低了单点故障的概率。

一旦生成或接收到区块Hash的完整签名就可以证明区块被确认，并不需要更多的消息通信。当一个有效的完整签名出现，说明已经有足够多的节点认为这个区块是有效的，这个签名可以通过聚合公钥快速验证。当有一个节点广播了完整签名，所有诚实的节点都会在 $Delta$ 时间内接收到完整签名。因此，完整签名作为区块确认的标志是可行的。由于诚实的节点在一轮中最多只会为一个有效区块的区块Hash签名，最终只有一个区块完成验证和确认过程。这意味着共识协议确保系统在同一轮中不会出现多个区块同时被确认，防止了链分叉的出现。

#### 4.2.5 节点故障时的共识协议操作

在我们的共识协议中，出块节点只承担生成区块的功能，出块节点的恶意行为只能是生成一个无效区块或者不生成区块。为了确保共识协议的持续运行，如果被选中的出块节点出现故障，我们的共识协议将会通过门限签名机制强制更换出块节点。协议中一轮共识进程结束之后，会出现两种输出：输出一个有效的被确认的区块和一个空区块（与一般的区块数据结构相同，但是区块中没有任何交易）。一个有效区块被确认需要满足以下条件：
* 出块节点创建一个有效区块；
* 该有效区块被足够多的共识节点接受并且为其Hash签名。

如果一个合法的出块节点创建一个无效区块，则其他节点会为一个空区块的Hash签名并广播表明当前出块节点的无效行为，最终确定当前轮是无效的。如果出块节点不生成区块或生成的有效区块没有被足够多的共识节点接受并对区块Hash签名，要么出现了网络问题，要么部分共识节点拒绝对区块Hash签名。这种情况，我们设置一个超时机制，所有诚实的共识节点会在一个空区块上签名，最终确认该区块并开始新一轮的共识进程。只有出现超时或者出块节点创建一个无效区块时，共识节点才在一个空区块上签名。我们的协议可以确保为空块或者有效块收集到足够多的区块Hash部分签名，之后将所有的部分签名聚合恢复成一个完整签名，将确认区块的Hash和完整签名作为输入，选出下一轮的出块节点。从而，协议可以确保敌手无法干扰新区块的出块节点的选举过程 ，提高系统的安全性。

#### 4.2.5 受到干扰攻击时协议的操作

在无线网络中，节点发起阻塞攻击（Jamming Attack）时，会阻塞其他节点传输消息。可能会导致其他节点即使对有效区块Hash签名也无法成功广播部分签名。

根据时间窗口动态调整节点收集签名的超时时间，确保节点能够在敌手发起阻塞攻击时也达成共识。我们的共识协议中，每个节点根据感应信道的情况维护一个敌手时间窗口估计 $T$。每个节点会根据共识过程中信道的情况，动态调整 $T$ 的大小，当 $T$ 达到某一阈值时需要更改超时的阈值。延长节点接受消息的时间，最终确保存阻塞攻击时共识节点也能够对有效区块达成共识，降低敌手发起干扰攻击共识过程的影响。

### 4.3 奖惩机制

为了提高节点愿意参与共识的积极性，出块节点在区块被确认之后会获得来自系统的区块奖励。为了提高节点愿区块签名的积极性，在区块被确认之后，我们为提供签名的节点发放签名奖励。

记组合最终签名的签名集合为 $signs = \{sig_{1}, sig{2}, \cdots, sig_{m}\}$， 每个签名对应的时间戳分别为 $tss = \{ts_{1}, ts_{2}, \cdots, ts_{m}\}$。针对可能存在节点接收到多个最终签名是由不同签名组成，签名奖金将发放给组合最终签名的签名集合中平均时间戳最小的节点集合。假设系统存在两个组合最终签名的签名集合 $signs_1 = \{sig_{11}, sig{12}, \cdots, sig_{1m_{1}}\}, signs_2 = \{sig_{21}, sig{22}, \cdots, sig_{2m_{2}}\}$， 每个签名的时间戳分别对应为 $tss_1 = \{ts_{11}, ts_{12}, \cdots, ts_{1m_{1}}\}, tss_2 = \{ts_{21}, ts_{22}, \cdots, ts_{2m_{2}}\}$。两个签名集合中平均时间戳分别为 $AVG_1 = \frac{\sum_{i = 1}^{m_1} ts_i}{m_1}，AVG_2 = \frac{\sum_{i = 1}^{m_2} ts_i}{m_2}$。如果 $AVG_1 < AVG_2$，则签名奖励将会被均分给 $signs_1$ 的所有节点。这种奖励机制，不仅会提高节点签名的积极性，还能提高区块签名的效率，进一步提高系统的性能。

此外，协议中设置了惩罚机制降低理性节点作恶的机会。一旦发现合法出块节点生成无效区块导致在当前轮最终确认空区块来判定节点的恶意行为。针对这类出块节点，我们将会选择减少节点在系统中的活动时间作为惩罚。这个惩罚措施会降低节点的稳定度，进而会降低节点被选作出块节点的概率，最终降低节点生成区块获得奖励。因此，理性的出块节点为了确保自己的收益，会减少生成无线区块的情况，从而提高系统的安全性和效率。

## 5. 协议分析

在本小节，我们主要分析系统的安全性和性能。通过分析系统的安全性来证明我们的协议能够为无线区块链系统提供持续性和活性，通过对系统达成共识的开销分析系统的性能，可以证明我们的协议的高效性和适用于无线区块链网络环境。

### 5.1 安全性分析

区块链的共识算法需要确保确保所有的共识节点对系统中的交易历史达成共识。当系统中绝大多数节点是诚实的，我们的协议可以保证持续性和活性。

为了确保安全性，稳定共识协议需要至少 $\lceil\frac{n+1}{2}\rceil$ 个节点来满足门限签名的需求。门限签名机制的输出是不可伪造和鲁棒的，这个机制具有两个重要的性质：
* 唯一性：门限签名机制中任意超过 $\lceil\frac{n+1}{2}\rceil$ 个部分签名恢复的完整签名都是相同的。
* 可验证性：最终恢复的完整签名可以被持有聚合公钥的任意节点验证。聚合公钥是在节点加入系统的时候由网络的密钥生成协议创建和分配的。

#### 5.1.1 持续性分析

我们的共识协议并以依赖出块节点确保安全性。恶意的节点可能会提出一个冲突区块来对共识发起攻击。由于在每一轮中，诚实节点只会对认可的首领节点生成的有效区块的区块Hash签名确认一次。因此，在一轮共识结束后，要么确认一个有效区块，要么确认一个空块，并且所有的诚实节点将会有相同的操作。我们的共识协议满足持续性：

* **定理一（持续性）**：所有诚实的节点将维护相同的区块链，即诚实节点 ${\rm Node}_{v}$ 声明交易 $tx$ 在区块链第 $i$ 个区块的第 $j$ 个位置上, 则最终所有诚实节点的区块链的第 $i$ 个区块的第 $j$ 个位置的交易一定是 $tx$。
**证明**：要证明持续性，我们需要证明任意两个诚实的节点维护的区块链相同。采用反证法证明，假设 $tx_{u}\in BC_{u}, tx_{v}\in BC_{v}$ 分别是诚实节点 ${rm Node}_{u}, {rm Node}_{v}$ 维护的区块链上相同位置的交易，且 $tx_{u}\neq tx_{v}$。那么会有两种情况出现：
  * $tx_{u}, tx_{v}$ 在同一轮中分别被添加到节点${rm Node}_{u}, {rm Node}_{v}$ 的本地区块链 $BC_{u}, BC_{v}$ 上。这表明首领节点在同一轮中生成并确认了两个不同的区块，这违反了我们协议中的门限签名机制的唯一性，因此与假设相矛盾。
  * $tx_{u}, tx_{v}$ 在不同的轮被添加到两个节点的区块链上。假设 $tx_{u}, tx_{v}$ 分别在 $r_{m}, r_{n}(m < n)$ 轮中被添加到两个节点的区块链 $BC_{u}, BC_{v}$。根据我们的协议，在 $r_{m}$ 轮中添加 $tx_{u}$ 到区块链上的节点至少有 $\lceil\frac{n+1}{2}\rceil$ 个，这些节点认可交易 $tx_{u}$ 是在 $r_{u}$ 轮首次被添加到的区块链的第 $i$ 个区块中第 $j$ 个交易。由于在一轮中不会最终确认两个不同的区块，因此添加交易 $tx_{u}$ 的节点在 $r_{m}$ 轮中有相同的区块链视图，即这些节点维护的区块链中的第 $i$ 个区块中第 $j$ 个交易 $tx_{i}^{j}$ 是相同的。我们假设 $tx_{v} \neq tx_{u}$，且 $r_{m} < r_{n}$。当节点 $v$ 在 $r_{m}$ 之前故障了并且在 $r_{n}$ 的时候恢复，此时节点将会同步区块链的最新信息。那么将会有至少 $\lceil\frac{n+1}{2}\rceil$ 个节点在第 $r_{n}$ 轮的时候认可区块链的第 $i$ 个区块的第 $j$ 个交易是 $tx_{v}$。由于之前在 $r_{m}$ 轮中也至少有 $\lceil\frac{n+1}{2}\rceil$ 个节点认可区块链在第 $i$ 个区块的第 $j$ 个交易是 $tx_{u}$。此时，网络大小为 $n > \lceil\frac{n+1}{2}\rceil + \lceil \frac{n+1}{2}\rceil = \lceil n+ 1 \rceil$，矛盾了。因此 $tx_{u} = tx_{v}$，与假设 $tx_{u} \neq tx_{v}$ 相矛盾。
因此得出结论，在每一轮中，即使存在矛盾区块，所有的诚实节点将会确认相同的有效区块。最终，所有的诚实节点对于区块链历史应该有相同的视图，即所有诚实的节点将维护相同的区块链。

#### 5.1.2 活性分析

对于活性，当至少 $\lceil\frac{n+1}{2}\rceil$ 个诚实节点能够对有效区块或者空块签名，并且最终只要有一个节点聚合足够的部分签名形成完整签名，就能够完成共识过程。

* **定理二（活性）**：当诚实节点数量超过 $\lceil\frac{n+1}{2}\rceil$ 时，即使系统中存在 $\lfloor\frac{n}{2}\rfloor$ 个故障节点，诚实节点也能够完成共识并获得新一轮的随机源。
**证明**：
  * 出块节点故障：由于我们的共识协议并不依赖出块节点来确保安全性，因此也不依赖出块节点的正确性来确保活性。如果出块节点出现故障未创建有效区块或者创建一个无效区块，诚实的共识节点在超时未收到有效区块或者验证区块无效之后，会对一个空块的区块Hash签名，最终收集到至少 $\lceil\frac{n+1}{2}\rceil$ 个部分签名的节点会生成完整签名，完成当前轮的共识过程并获得新一轮的随机源——完整签名。
  * 系统中存在 $\lfloor\frac{n}{2}\rfloor$ 个非出块节点故障：由于出块节点未发生故障，因此会生成一个有效的区块。其他 $n - \lfloor\frac{n}{2}\rfloor \geq \lceil\frac{n+1}{2}\rceil$ 个诚实的节点在验证区块成功后，会生成有效区块Hash的部分签名并广播给其他节点，故障节点会拒绝为区块Hash签名。但是由于诚实节点的数量超过安全阈值，因此会有至少 $\lceil\frac{n+1}{2}\rceil$ 个节点会生成有效部分签名。诚实节点会收集到足够的部分签名生成有效区块Hash的完整签名并广播。因此最终会完成当前轮的共识过程并获得新一轮的随机源。当由于敌手发起网络阻塞攻击导致最终诚实节点没有生成有效区块Hash的最终签名时，最终所有诚实的节点会因为超时而确认一个空区块。并开始新一轮的共识过程并获得下一轮的随机源。
即使节点故障，我们的协议也能够完成一轮共识过程，并获得下一轮的随机源。因此，我们的共识协议是能够确保活性的。

#### 5.1.3 女巫攻击分析

我们的协议能够比较好的防止理性的节点发起女巫攻击。假设攻击者被选中成为出块节点的概率为 $p_{A}$，其余 $m$ 个节点的概率分别为 $\{p_1, p_2, \cdots, p_m\}$。若攻击者发起女巫攻击，则攻击者控制的节点被选中的概率的期望 $\frac{1}{n}\sum_{k = 1}^n k\cdot p_k, (\sum_{k = 1}^n p_k = p_{A})$。此时有 $\frac{1}{n}\sum_{k = 1}^n k\cdot p_k < p_A$。
**证明**：令 $p_k = \frac{p_A}{n}$，则有 $\frac{1}{n}\sum_{k = 1}^n k\cdot p_k = \frac{1}{n}\sum_{k = 1}^n k\cdot \frac{p_A}{n} = p_A\sum_{k=1}^n\frac{k}{n^2} = p_A\frac{\sum_{k=1}^n k}{n^2}$。当 $n > 1$ 是有 $\sum_{k = 1}^n < n^2$ ，因此 $p_A\frac{\sum_{k=1}^n k}{n^2} < p_A, n>1$。最终得出结论 $\frac{1}{n}\sum_{k = 1}^n k\cdot p_k < p_A, n > 1$。因此，我们的协议中，攻击者发起女巫攻击时，成为出块节点的概率会降低。攻击者的伪造节点越多，则成为出块节点的概率将会越低。通常理性的节点不会愿意伪造多个节点降低成为出块节点的概率，因此我们的协议能够较好的抵抗女巫攻击。

#### 5.1.4 阻塞攻击

我们的协议能够较好的抵抗节点发起阻塞攻击影响共识过程。假设节点在 $T$ 轮通信中最多能够发起 $(1 - \epsilon)T$ 轮阻塞攻击。在共识节点开始新一轮的共识过程时，节点会根据检测信道的情况来动态调整收集部分签名的超时阈值。

当没有敌手发起阻塞攻击时，假设每个节点成功传输消息的概率为 $p$，可以在 $K$ 轮中以较高的概率传输部分签名成功。计算 $1 - (1 - p)^{K} \geq 1 - \frac{1}{N^{2}}$，从而就有 $1 - (1 - p)^{K} \geq 1 - e^{-pK} \geq 1 - \frac{1}{N^{2}}$，可知共识节点在 $\frac{2}{p}\log n$ 轮中有很高的概率可以传输部分签名成功。因此，在 $\lceil\frac{n+1}{2}\rceil \frac{2}{p}\log n$ 轮后，共识节点有很高的概率可以生成一个完整签名，最终确认区块。

当敌手发起阻塞攻击时，诚实节点能够成功传输的轮数为 $\frac{2\epsilon}{p}\log n$，成功生成完整签名的轮数为 $\lceil\frac{n+1}{2}\rceil \frac{2\epsilon}{p}\log n$。敌手发起阻塞攻击会使得诚实节点的部分签名不能成功传输，最终导致系统无法在超时阈值之内接收到足够的部分签名而无法完成共识。我们的协议通过根据节点对于敌手攻击窗口的估计来动态调整超时机制的阈值，降低阻塞攻击对于共识过程的影响。

### 5.2 性能分析

在协议的共识过程中，只有在出块节点生成有效区块，并有节点接收到至少 $t = \lceil\frac{N+1}{2}\rceil$ 个区块Hash的部分签名时，才会生成完整签名确认有效区块。节点接收到至少 $t$ 个区块Hash的部分签名的概率为 $P_{rs} = \sum_{k = t}^{N-1}C_{N-1}^{k}P_{s}^{k}(1 - P_{s})^{N-1-k}$，共识协议生成有效区块的概率为 
$$P_{valid} = P\{L \geq t\} = \sum_{L=t}^{N-1}C_{N-1}^L P_{rs}^L(1 - P_{rs})^{N-1-L}$$
其中 $L$ 为成功接收到 $t$ 以上个区块签名份额节点的数量，当 $L\geq t$ 时说明系统中大部分节点都能将有效区块添加到本地区块链上。因此，生成空块的的概率为 
$$P_{null} = 1 - P_{valid}.$$

#### 5.2.1 算力开销分析

在我们的共识协议中，主要的算力开销来自共识过程中出块节点的选择过程的计算，生成和验证区块时的交易Hash计算、区块Hash计算，确认区块时生成和验证区块Hash签名的计算，以及生成和验证完整签名时的计算。

记协议中每个节点的算力为 $r$，令区块中交易的打包时间为 $T_{c}$，区块哈希和签名的计算时间都为 $T_{s}$。
* 生成一个空块的哈希次数为 $NrT_{s} + (N-1)NrT_{s} + NrT_{s} = (N+1)NrT_{s} \approx O(N^2rT_{s})$；
* 生成一个有效区块的哈希次数为 $NrT_{s} + Nr(T_{s}+T_{c}) + (N-1)NrT_{s} + NrT_{s} = Nr(T_{s}+T_{c}) + (N+1)NrT_{s} \approx O(N^{2}r(T_{s}+T_{c})$。

假设在生成一个有效区块之前已经生成过 $m$ 次空块，当生成空块的概率 $0\leq P_{null} < 1$时，生成一个有效区块所需的哈希次数为
$H_{Stable} = \sum_{m=0}^{\infty}P_{null}^mP_{valid}(m\cdot(N+1)NrT_{s} + Nr(T_{s}+T_{c}) + (N+1)NrT_{s})$。最终计算得到生成一个有效区块的平均哈希次数为
$$H_{Stable} = \left\{
      \begin{aligned}
      & \frac{(N+1)NrT_{s}}{1 - P_{null}} + Nr(T_{s}+T_{c}), \text{if } P_{null}\neq 1, \\
      & \infty, \text{ if } P_{null} = 1.
      \end{aligned}
      \right.$$

#### 5.2.2 通信开销分析

在我们的共识协议中生成一个有效区块主要的时间包括打包生成和验证区块（毫秒级）、广播区块（秒级）；生成和验证部分签名（毫秒级）、广播部分签名（秒级）、生成和验证完整签名（毫秒级）、广播完整签名（秒级）。

记节点广播一次的时延为 $T_{b}$ ，打包有效区块的交易时间为 $T_{c}$，生成区块Hash和签名的时间为 $T_{s}$。
* 生成一个有效区块的时间为 $T_{1} = 2T_{c} + 4T_{s} + 3T_{b}$；
* 生成一个空块的时间为 $T_{2} = 3T_b + 4T_s$。

假设生成有效区块的通信次数为 $C_{normal}$；生成空块的通信次数为 $C_{null}$。假设生成一个有效区块之前连续 $m$ 次生成空块。
  $$C_{Stable} = \left\{
      \begin{aligned}
      & \sum_{m=0}^\infty P_{null}^m\cdot P_{valid}\cdot (mC_{null} + C_{normal}), \text{if } P_{null}\neq 1, \\
      & \infty, \text{ if } P_{null} = 1.
      \end{aligned}
      \right.$$
  * **生成有效区块**：假设交易到达速率为 $\lambda$，协议在 $T_{1}$ 时间内生成一个有效区块，则交易到达数量为 $\lambda T_{1}$。生成一个有效区块的通信次数为 $C_{normal} = \lambda T_{1}(N-1) + (N-1) + （N-1) + (N-1) = (N-1)(\lambda T_{1} + 3)$；
  * **生成空块**：出块节点在 $T_1$ 时间内生成一个区块但是确认失败。所有节点会在 $T_{2}$ 时间内生成一个空块，并最终确认该空块。这段时间内的交易到达数为 $\lambda T_{2}$，增加的通信数是 $\lambda T_{2}(N-1) + (N-1) + (N-1) + (N-1) = (N-1)(\lambda T_{2} + 3)$。生成空块的通信数量为 $C_{null} = C_{normal} +(N-1)(\lambda T_{2} + 3) = (N-1)[\lambda(T_1 + T_2) + 6]$。
最后计算得到在我们的协议中平均通信数量为
  $$C_{Stable} = \left\{
      \begin{aligned}
      & \frac{P_{null}\cdot(N-1)\cdot(\lambda T_{2} + 3)}{1 - P_{null}} + \frac{(N-1)\cdot(\lambda T_{1} + 3)}{1 - P_{null}}, \text{if } P_{null}\neq 1, \\
      & \infty, \text{ if } P_{null} = 1.
      \end{aligned}
      \right.$$

#### 5.2.3 节点活动时间分析

每个节点在注册进入系统时，通过支付金钱来获取在系统中的活动时间。支付的金钱将通过购买基础设施或者做一些投资来获取盈利。因此，关于活动时间的价格可以根据价格在一段时间内的波动现象和规律来对活动时间的价格进行预测定价。

节点可以通过增加金额来延长活动时间，也可以重新注册新的节点来获得活动时间。记 $N$ 为共识节点集合，$T_{i}$ 是节点 $i\in N$ 的活动时间，用户增加活动时间有两种方式：一种是通过充值金钱延长节点 $i$ 的活动时间；一种是通过注册新节点延长用户的活动时间。
* 第一种情况时用户的稳定度概率计算如下：
  * 节点的活动时间比为 $\rho_{i} = \frac{T_{i} + \Delta T_{i}}{\sum_{j\in N}T_j + \Delta T_{i}} $
  * 节点的共识比 $r_i = \frac{N_{i} + \Delta N_i}{K}$
  * 节点的稳定度为 $w_{i} = \alpha \rho_{i} + \beta r_{i} = \alpha \frac{T_{i} + \Delta T_{i}}{\sum_{j\in N}T_j + \Delta T_{i}} + \beta \frac{N_{i} + \Delta N_i}{K}$
  * 节点被选中的概率为 $p_{i} = \frac{w_{i}}{\sum_{j\in N} w_{j} + \alpha \Delta \frac{\Delta T_{i}}{\sum_{j\in N}T_j + \Delta T_{i}} + \beta \frac{\Delta N_i}{K}}$
* 第二种情况时用户稳定度概率计算如下：
  * 用户所有节点的活动时间比为 $\rho_{i}' = \frac{T_{i}}{\sum_{j\in N}T_j + \Delta T_{i}} + \frac{\Delta T_{i}}{\sum_{j\in N}T_j + \Delta T_{i}} = \rho_{i}'' + \Delta \rho_{i}$
  * 节点的共识比 $r_{i}'= \frac{N_{i}}{K} +  \frac{\Delta N_i}{K} = r_{i}'' + \Delta r_{i}$
  * 两个节点的稳定度分别为：$w_i'' = \alpha \frac{T_{i}}{\sum_{j\in N}T_j + \Delta T_{i}} + \beta \frac{N_{i}}{K} = \alpha \rho_{i}'' + \beta r_{i}'', \Delta w_{i} = \alpha \frac{\Delta T_{i}}{\sum_{j\in N}T_j + \Delta T_{i}} + \beta \frac{\Delta N_i}{K} =\alpha \Delta\rho_{i} + \beta \Delta r_{i}$
  * 两个节点的被选中的概率分别为 $p_{i}'' = \frac{w_{i}''}{\sum_{j\in N} w_{j} + \alpha \Delta \frac{\Delta T_{i}}{\sum_{j\in N}T_j + \Delta T_{i}} + \beta \frac{\Delta N_i}{K}}, \Delta p_{i} = \frac{\Delta w_{i}}{\sum_{j\in N} w_{j} + \alpha \Delta \frac{\Delta T_{i}}{\sum_{j\in N}T_j + \Delta T_{i}} + \beta \frac{\Delta N_i}{K}}$。

通过计算可知 $p_{i} = \frac{\alpha \frac{T_{i} + \Delta T_{i}}{\sum_{j\in N}T_j + \Delta T_{i}} + \beta \frac{N_{i} + \Delta N_i}{K}}{\sum_{j\in N} w_{j} + \alpha \Delta \frac{\Delta T_{i}}{\sum_{j\in N}T_j + \Delta T_{i}} + \beta \frac{\Delta N_i}{K}} = \frac{\alpha \frac{T_{i}}{\sum_{j\in N}T_j + \Delta T_{i}} + \beta \frac{N_{i}}{K}}{\sum_{j\in N} w_{j} + \alpha \Delta \frac{\Delta T_{i}}{\sum_{j\in N}T_j + \Delta T_{i}} + \beta \frac{\Delta N_i}{K}}  + \frac{\alpha \frac{\Delta T_{i}}{\sum_{j\in N}T_j + \Delta T_{i}} + \beta \frac{\Delta N_i}{K}}{\sum_{j\in N} w_{j} + \alpha \Delta \frac{\Delta T_{i}}{\sum_{j\in N}T_j + \Delta T_{i}} + \beta \frac{\Delta N_i}{K}} = \alpha\rho_{i}'' + \beta r_{i}'' + \alpha \Delta\rho_{i} + \beta \Delta r_{i}  = p_{i}''$。因此，不管是直接注资延长节点的活动时间还是注册新节点增加活动时间，最终用户控制的节点被选中成为出块节点的概率是相等的。


## 仿真验证

在这一节中，我们仿真研究变量参数是如何影响稳定协议的性能。我们区块共识的平均吞吐量和时延来分析协议的正确性和高效性。

影响性能主要因素包括网络大小、网络密度和信噪比模型。我们采用的信噪比参数分别是 $\alpha = 2, \beta = 3, $（待补充）。此外，节点是均匀分布且女巫节点默认为 $0\%$。

为了估计协议的性能，我们主要采用两个指标：吞吐量和共识时延。共识时延是指完成一轮共识所需的时间。换句话说，也是完成添加一个新区块到区块链所需的时间。这个指标主要是受到节点的数量和节点的密度的影响。对于吞吐量，我们固定区块大小之后，可以根据共识时延计算得到 $$Throughput = \frac{\text{number of transactions}}{\text{consensus latency}}$$

吞吐量的单位是每秒交易数(TPS)。

我们的实验都是在(电脑的基本参数指标)。


由于协议的活性是由网络大小决定的，



## 结论

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

[38] D. Boneh, B. Lynn, and H. Shacham, "Short signatures from the Weil pairing[C]". International Conference on the Theory and Application of Cryptology and Information Security. Springer, Berlin, Heidelberg, 2001:514-532.
[39] R. Gennaro, S. Jarecki, H. Krawczyk, and T. Rabin. "Secure distributed key generation for discrete-log based cryptosystems," in Proc.
Int. Conf. Theory Appl. Cryptograph. Techn., vol. 1592, Aug. 2010,pp. 295–310.
[40] A. Boldyreva. "Threshold signatures, multisignatures and blind signatures
based on the gap-Diffie-Hellman-group signature scheme," in Proc. 6th Int. Workshop Theory Pract. Public Key Cryptogr., 2003, pp. 31–46.
