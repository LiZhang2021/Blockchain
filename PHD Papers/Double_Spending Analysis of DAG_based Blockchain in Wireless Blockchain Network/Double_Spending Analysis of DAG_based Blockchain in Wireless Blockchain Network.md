# Double-Spending Analysis of DAG-Based Blockchain in Wireless Blockchain Network

## Abstract


## Introduction 


## Preliminaries

In this section, we introduce the characteristics of wireless network and the consensus protocol of DAG-based blockchain respectively. Then, we describe the main procedures that a new transaction is accepted by all nodes in the wireless network whose communication protocol is CSMA/CA protocol.

### Wireless Network 

Wireless Local Area Networks(WLANs)[1-2] with high flexibility and convenience can provide high quality services for users in limited geographical area. Currently, as the de facto standard of WLANs, IEEE 802.11[1] has been wirdly used in wireless network. This standard include Distributed Coordination Function(DCF)[3] as Medium Access Control(MAC)[1] mechanism. The DCF, which based on Carrier Sense Multiple Access with Collision Avoidance(CSMA/CA) and binary slotted exponential backoff, can support asynchronous data transfer on a best effort basis. In this paper, we consider that any node competing for wireless channel broadcast packets by using CSMA/CA as media access protocol.

### DAG-based Blockchain

DAG-based blockchain allows that appending new transaction in a forking topology. The first proposed consensus algorithm for DAG-based blockchain is Tangle[4]. In this paper, we use Tangle as consensus algorithm to analyze the consensus process of DAG-based blockchain. Compare to PoW and PoS, Tangle has higher throughput bacause it allows different branches to merge into the main chain eventually. 
As shown in Fig.1, Tangle uses directed acyclic graph topology to record transaction, and the unit of Tangle should be a recorded trasaction. The basic concepts of Tangle are represented as follows:
<font color = blue>
* **Tip:** the transaction(or block) that has not been approved by any other trasnaction(or block). That is, tips are unapproved transactions in tangle graph;
* **Direct Approval:** two transactions(or blocks) is connected by a direct edge, we can say one transaction is directly approved by another transaction.
* **Indirect Approval:** two transactions are not connected by a direct edge, but there is a directed path of lenth at least two between the two transactions, then we can say the two transactions are indirectly approved.
* **Own Weight:** trasnation's own weight is propotional to the amount of work(computational power or stakes) that issuing node conssumes on proposing a trasnaction(or block).
* **Cumulative Weight:** the sum of the transaction's own weight  and the overall own weight of all transactions that directly or indirectly approve this transaction.
* **Confirmation Weight Threashold:** the threshold value of trasnaction's cumulative weight, when the cumulative weight meet this value, the transaction should be confirmed.
</font>

![](./pics/Figure_1.png)

### Consensus process of DAG-Based Blockchain under Wireless Network

While the broadcast procedure following CSMA/CA in wireless network, the consensus protocol should work to make sure that new issued transaction is accepted by the other nodes. For simplicity,we only consider all nodes under same local area network. Thus, the main procedures that consensus process in wireless network are as follows:
<font color = purple>
* A node finds a nonce to solve a cryptographic puzzle to meet the difficult target.
* The node issues a new transaction which will select two nonconflicting tips to approve based on local information;
* The node uses its private key to sign this new transaction. The new transaction will enter into cache waiting for broadcasting through wireless channel;
* The node competes for wireless channel following CSMA/CA while the new transaction queues in cache following first in first out(FIFO) rule;
* The node either broadcasts the transaction successfully or rebroadcasts with backoff;
* Other nodes receive the new transaction and check it to confirm legality. If the new transaction is legal, then it will become a new tip and wait for the direct or indirect approvement for confirmation. 
</font>

The consensus process of an issued transaction is divided into two stages: reveal stage and weight accumulating stage.
<font color = blue>
  * **Reveal Stage:** The observed transaction is appended into the DAG-based blockchain, that is all nodes can see the transaction.
  * **Weight Accumulating Stage:** the cumulative weight of the observed transaction increases from its own weight to confirmation threshold gradually.
</font>

In order to simplify later analysis, we can define the second to five procedures as reveal stage, and procedure six as the weight accumulating stage of new transaction. As we can see that communication in network may cause a serious delay when nodes compete for wireless channel to broadcast the new transaction.

## Double-Spending Attack in Wireless Blockchain Network

In this section, we first introduce the double-spending attack of DAG-based blockchain. And then we analyze the successfull attack probability of double-spending under wireless network with imperfect CSMA/CA protocol.

### System Model

 We now present some assumptions for double-spending attack analysis.
* Assume that  there are $n$ nodes running Tangle, they communicate with each other directly throught wireless channel.
* Assume that there are $n-1$ honest nodes and one attacker;
* Assume that each node selects two tips with no-conflict by Markov Chain Monte Carlo(MCMC) tips selection algorithm[4].
* The transaction arrival rate of each node follows the Poisson process[5]. Let $\lambda, \mu$ be the arrival rate of new trasnactions on a honest node and a malicious attacker respectively.
* Let the own weight of each transaction be one.
* Let $h$ be the average transmission delay to broadcast a packet through CSMA/CA protocol. In addition, $h$ is also the reveal time to update the new transaction discussed in Tangle. 
* Let $m$ be the maximum number of transactions at one broadcast.

**The Average Transmission Delay $h$**

In CSMA/CA, all nodes will compete to send messages. We always split time into multiple slots, and let the probability of each node sending messages in a slot be $\tau = \frac{1}{n}$. If there are $n$ nodes in wireless blockchain network, the probability of at least one node broadcasting in a slot time  is 
$$P_{tr} = 1 - (1 - \tau)^{n}.$$

The probability of one node broadcasts successfully in a slot time is 
$$P_s = C_n^1 \tau(1 - \tau)^{n-1} = n\cdot\tau\cdot(1 - \tau)^{n-1}$$
 
 The probability of broadcast collision occuring in a slot time is 
 $$P_c = 1 - (1 - \tau)^{n} - P_s.$$

Let $T_s$ be the average time that channel is detected busy due to a successful broadcasting, and its probability is $P_s$. Denoting $T_c$ is the average time that channel is collision, the probability of broadcast collision is $P_c$. Besides, when the channel is free that no node broadcast in a slot time, let $\sigma$ be the duration time of the empty slot time, the probability of this regime is $1 - P_{tr}$. Therefore, the average transmission delay $h$ is the expected value of the above three situations:
$$h = (1 - P_{tr})\cdot\sigma + P_s\cdot T_s + P_c\cdot T_c.$$

In order to  ensure the fairness of CSMA/CA, each node has same probability $\tau$ to access the wireless channel to broadcast. In order to describe the queuing state, we divide the network network load into two regimes.
<font color = red> 待补充</font>

### Attack Model

 A transaction is confirmed in DAG-based blockchain when its cumulative weight reaches to the confirmation weight threshold(large weight). When an attacker wants to tamper this confirmed transaction, it should create a fraudulent subtangle, such that the subtangle that containing the original transaction be orphaned. In this case, we say that the attacker launches double-spending attack successfully, and the attacker can steal the money residing in the original transaction. 
![](pics/Figure_3.png)

As shown in Fig. 3, the typical way that a malicious attacker lunches double spending attack is to construct a fraudulent chain in blockchain system, the main procedures are shown as follows:
<font color = purple>
* At time $t_0$, attacker broadcasts an honest transaction, and honest nodes will approve it.
* At time $t_1$, the attacker builds a fraud chain in offchain to approve a fraudulent transaction that is conflicted with the honest transaction.
* After time $t_1$, the attacker will continually issue trasnactions to grow the cumulative weight of the fraudulent transaction. The time $t_1$ should be earlier than the end of adaption periof of the honest transaction.
* At time $t_2$, the honest transaction has been confirmed while its cumulative weight attaches $w$. In this case, the victim will send goods or services to the attacker.
* While the cumulative weight of the fraudulent transaction overweights the confirmed honest transaction after time $t_2$, the attacker will broadcast the fraudulent chain to the whole wireless blockchain network.
* Once the attacker contending for wireless channel to broadcast fraudulent branch updating the DAG-based blockchain, the fraud transaction will be accepted by other honest nodes based on the MCMC algorithm due to the higher cumulative weight. The confirmed honest transaction will be orphened in DAG-based blockchain, the victim cannot receive the payment even though it has provided goods or services. In this case, the attacker issues double-spending attack successfully.
</font>

### Success Probability of Attack



### Security Goal

### Probability of a Successful Attack



## Simulation and Discussion



## Conclusion

## Related Work

## References

[1] L. S. Committee, "ANSI/IEEE Std 802.11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications". IEEE Computer Society, 1999.
[2] B. P. Crow, J.G. Kim, "IEEE 802.11 Wireless Local Area  Networks", IEEE Communications magazine, Sept. 1997.
[3] H. Wu, S. Cheng, Y. Peng, K. Long and J. Ma, "IEEE 802.11 Distributed Coordination Function (DCF): Analysis and Enhancement," 2002 IEEE International Conference on Communications. Conference Proceedings. ICC 2002 (Cat. No.02CH37333), 2002, pp. 605-609 vol.1, doi: 10.1109/ICC.2002.996924.
[4] S. Popov, "The tangle", White paper, 2018. [Online]. Available:
https://www.iota.org/research/academic-papers.
[5] R. G. Gallager, "Discrete Stochastic Processes". Kluwer Academic Publishers, 1996.
