# 无线网络中的区块链

无线网络中资源有限的设备不能使用消耗物理资源的工作量证明作为系统共识机制。因此，如何在无线区块系统上尽可能节约资源的达成一致是无线区块链系统急需解决的问题。

## 无线网络中的区块链协议

在设计无线区块链协议时，主要从系统模型、协议架构，协议分析以及仿真试验这几个方面入手。我们将分别总结在区块链中这几个部分的特点。

### 系统模型

在设计无线网络区块链协议时，重点要考虑网络模型、干扰模型以及攻击者模型。

#### 网络模型

首先需要定义区块链系统中网络模型的构建，并且定义每个节点的基本设置参数。
* 系统是由 $n$ 个节点组成，节点集合记作 $V = { V_1, \cdots, V_n}$；
* 节点通过发送信号进行通信，每个节点 $V_i$ 都是半双工收发器；
* 记 $d(u,v)$ 是节点 $u$ 和 $v$ 的欧式距离，以及 $DR(v)$ 是以 $v$ 为中心，以 $R$ 为半径的圆盘, 记 $NR(v)$ 为在 $DR(v)$ 中包括节点 $v$ 在内的节点的集合。
* 假设每个节点都知道其他节点的身份、位置以及公钥；
* 假设每个节点都可以生成密钥对并且可以访问安全EUF-CMA 数字签名方案；
* 根据适用的场景决定节点节点能否自由的加入或者离开网络（许可网络、开放网络）。

在构建网络模型时，主要是考虑节点的连接方式、节点的通信方式、节点的组成等都需要重点考虑。最重要的是节点在协议中拥有的功能（这将在后面的协议架构中讨论）。
#### 干扰模型
采用信号发射的方式传递消息的无线网络也需要考虑信号发射过程中必然存在干扰，因此需要考虑无线网络中的信道干扰模型。
* 信道传输的干扰模型主要采用信号干扰噪声模型 $SINR = \frac{\mathcal{S}}{(\mathcal{I}+\mathcal{N})} \geq \beta$，其中 $\mathcal{S} = P\cdot d(u,v)^{-\alpha}$ 是节点 $v$ 从节点 $u$ 处接收信号功率，而 $P$ 是均匀信号发射功率；
* 在节点 $v$ 处的干扰为 $\mathcal{I} = \sum_{w\in W\setminus{u}} P\cdot d(w,v)^{-\alpha}$，其中 $W$ 是在当前轮中传输的节点的集合；
* 记环境噪声为 $\mathcal{N}$，路径损耗指数为 $\alpha\in(2,6]$，阈值 $\beta > 1$ 取决于硬件。为了捕获细粒度噪声，定义 $\mathcal{N} = \mathcal{ADV}(v)$ 是由环境和敌手生成的组合噪声。
* 信号干扰噪声模型的假设：
  * 每个节点都使用先沟通的噪声阈值 $\theta$ 并且任意两节点之间的距离的界为 $R_0 = (\frac{P}{\beta\theta})^{\frac{1}{\alpha}}$； 
  * 每个节点都可以执行物理载波监听。若节点 $v$至少有一个邻居 $u$ 广播消息，那么 $v$ 要么接收消息，要么感应到信道忙碌。
   $$ v=\left\{
    \begin{aligned}
    \text{ sense idle channel} &  & \text{if } \mathcal{I+N} < \theta, \\
    \text{ receive a message}  &  & \text{if }  \mathcal{I+N} > \theta \text{ and }  SINR \geq \beta,\\
     \text{ sense busy channel}  &  & \text{if }  \mathcal{I+N} > \theta \text{ and } SINR < \beta.
    \end{aligned}
  \right.$$  

#### 攻击者模型
对于无线网络中，部分节点可能会被攻击者控制作恶使得系统最终崩溃。因此在讨论区块链系统的故障容忍性时，需要预先定义节点可能的故障行为。通常节点会出现两种故障：节点崩溃故障和节点拜占庭故障。
* **节点崩溃故障：** 在节点崩溃之前的所有消息都是正确的，一旦节点崩溃将不在进行任何工作（不在发送或者接收任何消息）；
* **节点拜占庭故障：** 节点可能发送错误消息阻止系统共识的达成，或者阻止干扰其他节点的消息传输，或者创建假身份误导其他节点。

通常为了防止系统一开始被攻击者控制，会限制攻击者的能力：
* 攻击者最多可以控制少于全网 $50\%$ 的网络资源（算力或者节点）；
* 攻击者可以发起阻塞攻击，但是为了确保无线网络中诚实节点拥有通信机会，攻击者不能阻塞所有所有轮中的通信（至少要给诚实节点留下通信的轮）。

### 协议架构

在设计区块链协议时，主要考虑系统中节点的功能、共识机制、区块（交易）验证机制、检查点机制等。其中最为重要的的部分是节点功能以及区块链系统的共识机制。

#### 节点功能函数

无线网络区块链协议的最基本构成就是节点。节点都承担了交易生成、消息发送和接收、生成区块等基本功能。为了确保系统的正常运行，需要对节点的检点函数给出相应的定义。
* 节点生成普通消息 $m$ ：
* 节点生成交易消息 $m_T$ ：
* 节点生成区块消息 $m_B$ ：
* 节点打包交易生成区块：
* 节点添加区块到区块链：
* 交易的数据结构：
* 区块的数据结构：
* 节点的数据结构：
* 消息的数据结构：

#### 共识机制

##### 区块链的共识分类
区块链系统根据容忍的故障类型可以分为拜占庭容错共识算法和非拜占庭容错共识算法，根据区块的确定性程度可以分为非确定性共识算法和确定性共识算法，根据区块链的能耗可以分为资源证明（物理资源和虚拟资源）共识算法和消息传输共识算法。而根据共识节点数量则可以分为首领选择共识算法和委员会决议共识算法。下面我们根据共识节点的数量来讨论分析无线网络中区块链的共识算法。

* **基于首领选择的共识机制**
基于首领选择的共识算法的核心是首领选择，工作流程如下：
  * 一个任期的开始选出一个系统公认的首领；
  * 首领收集交易打包生成区块并广播出去；
  * 其他节点接收到区块后，验证其有效性并链接到局部链上，开始新一轮任期选出新的首领。

  首领选择的机制是区块链系统的核心，需要满足随机性、公认性以及公平性。主要的首领选择机制如下：
  * 随机机制选举首领：设置一个随机函数，上一轮区块的结果作为随机种子输入到随机函数中选出新一轮任期的首领；
  * 轮换机制选举首领：根据已知的节点ID，设置一个轮换函数，每个任期依次指定一个节点作为首领；
  * 竞争机制选举首领：节点通过竞争的方式成为首领，所有节点在一个任期中抢占信道的快慢、工作量证明计算的快慢以及资源的大小等方式选举出首领。

  选出的首领的正确性与合法性是可以由系统中其他节点验证的，如果不合法则系统将不会承认该节点为首领。一旦首领选出并确定后，其他诚实节点必须承认接收该节点生成的有效区块，并链接到本地局部链上。最终，系统的所有节点在区块链上达成全局一致。

* **基于委员会的共识机制**
  基于委员会的共识算法主的核心是委员会成员的选择以及共识达成的机制：
  * 选取委员会成员，并选出当前任期内的区块提案者；
  * 委员会成员通过通信对提出的区块达成一致，并将结果广播；
  * 根据最后的结果，系统中所有节点将接收到的区块链接到局部链上，并开始新一轮操作。 

  委员会分为静态委员会和动态委员会：
  * **静态委员会：** 在系统开始运行时就选定固定的委员会成员，并且将一直不发生变化；
  * **动态委员会：** 每一个委员会都只能工作固定时长，一旦任期结束就会进行部分或全部更换。

  静态委员会机制比较高效节省资源，但是中心化程度过高，并且容易受到腐蚀攻击；动态委员会机制会额外的资源和通信开销，但是安全性高，且成员更换有利于节点的安全性（不容易被腐蚀和攻击）。

##### 实例

在这几篇无线网络区块链共识协议中，[BLOWN协议](./Notes/1.md)采用的是竞争首领选择机制的共识算法，利用无线信道特性，选出节点作为首领。在确认首领之后，收集交易并打包成区块，发送给其他跟随者节点达成全局一致。而[wChain协议](Notes/6.md)则利用无线网络节点距离和最大独立集来构造一个多跳网络通信架构——Spanner，从而选出首领，并利用这个通信架构收集交易，最终首领将交易打包成区块，并将区块作为提案，通过消息通信所有节点最终对于提案达成一致。最后所有节点接受该区块，并链接到局部链上，达成全局一致。[SENATE协议](Notes/5.md)则采用的是委员会机制，通过双重选择的方式确定最终委员会的成员：首先通过随机抽签的方式选出候选人，其次再根据节点的分布特性利用K聚类算法选出最终委员会成员。之后委员会成员提出提案达成委员会共识后，将结果广播给所有节点，接收到结果的节点将结果添加到本地账本中。

### 协议分析
分析协议时主要从协议的性能和安全性方面入手。区块链的性能分析则是研究区块链协议的交易吞吐量和交易确认延时。区块链协议的安全性分析主要是讨论区块链协议的一致性、活性以及抗攻击性。针对无线区块链系统通信协议的特点，根据协议的设计架构进行具体分析。

#### 安全性
区块链协议的安全性主要是从考虑区块链中数据的一致性、系统的活性以及系统的抗攻击性。
* **一致性：** 所有诚实节点维护相同的区块链（当一个节点返回一个请求的结果时，其他诚实节点也会返回相同的结果）；
* **活性：** 所有的诚实节点最终都会确认一个区块。

对于区块链系统要确保一致性需要保证系统中绝大部分节点都是诚实的，确保最终共识结果掌控在诚实节点中，使得系统的区块链是全局一致的。此外，也要确保区块链系统能够一直运行下去。系统中只要生成了区块，在有限时间内该区块要么达成共识被链接到各诚实节点的区块链上，要么不被所有诚实节点接受，最终被拒绝。针对不同的网络模型，一致性的实现将会有差异：
* 无许可网络：对于开放网络，节点无法获知系统中节点的总数量。因此节点无法通过绝大多数节点的认可来确认区块的有效性。每个节点都维护自己的局部账本，但这类区块链系统中所有的节点都遵循统一的区块链确认原则（最长链原则或最大权重原则），进而确保区块链系统最终只维护一条统一的区块链。这类网络下的区块链系统的共识算法通常是改了才行共识。由于每个节点都是维护自己的局部账本，因此区块链容易出现分叉，极易受到双花攻击；
* 许可网络：针对于许可网络，节点可以知道系统中节点的总数量。因此，系统中的节点可以对于区块达成统一的共识，使得系统中所有节点都是维护一个区块链。这类网络设计的区块链共识算法通常是确定性共识算法，区块链不会出现分叉，可以很好的避免双花攻击。



#### 性能

在研究区块链的安全性满足后，会分析区块链协议的性能。在完美通信的假设下，对于链式结构的区块链协议的性能主要考虑该区块链的交易吞吐量和交易确认时间。
* **交易吞吐量：** 是指单位时间内交易完成的数量；
* **交易确认时间：** 是指交易从打包进入区块到第一次被确认的时间。

在讨论区块链的性能时，通常会研究这两个性能指标随着网络大小的变化。但是，无线网络具有特殊性，并且无线网络中的节点具有动态性。因此在无线网络中，需要从以下几个角度分析协议的安全性：
* 分析区块链协议的通信复杂度，尤其是共识协议的通信复杂度；
* 分析协议的时间复杂度。达成共识所需的时间与共识机制关系紧密。必要时可以观察网络中某些参数变化引起共识时间的变化来讨论协议的性能；
* 网络节点的密度也是影响区块链性能的重要因素，通过观察节点密度的变化对于吞吐量和交易确认时间的影响可以分析协议的性能；
* 此外，在无线网络中还面临着阻塞攻击的威胁。阻塞攻击通常会延长达成共识的时间，进而影响吞吐量。因此可以通过探究阻塞攻击时参数的变化对共识时间和吞吐量的影响来分析区块链协议的性能；
* 女巫攻击是区块链协议面临的常见攻击。攻击者通过伪造身份获得更多的权益，进而使得自己获益。因此在讨论无许可的区块链协议时需要讨论女巫攻击节点数量的变化对于共识达成时间以及吞吐量的影响。

### 总结

无线网络区块链协议的核心组成为：**共识协议和网络通信协议**。在分析区块链协议的安全性时，主要是考虑区块链共识协议的安全性。这个主要是根据共识协议安全性的定义——一致性和活性两个方面展开讨论。在分析区块链协议的性能时，主要从网络协议下区块链性能指标的主要影响因素——网络大小、攻击节点的数量、网络密度等来分析区块链协议的性能。由于无线网络中通信协议的特殊性会影响区块链的性能，我们需要从实际网络通信协议出发来针对具体的区块链协议进行分析讨论。此外，仿真阻塞攻击参数变化和女巫攻击节点数量的变化对于协议性能的影响可以分析协议的女巫攻击和阻塞攻击的抗性。对于双花攻击，就需要考虑共识协议是否是概率性共识。如果是，则需要分析其双花攻击成功的概率以及收益，一次来分析区块链协议的双花攻击抗性等。


## 物联网中的区块链协议

### Concordia共识协议

### Microchain共识协议

### 自适应PBFT共识协议


