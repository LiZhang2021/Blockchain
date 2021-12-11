# DAG-Based Blockchain in Wireless Network

## DAG-based Blockchain Definitions

* **Block:** the storage unit to records information including transaction, digital signature, and hash value. In tangle, a block just records one transaction;
* **Tip:** the transaction(or block) that has not been approved by any other trasnaction(or block). That is, tips are unapproved transactions in tangle graph;
* **Direct Approval:** two transactions(or blocks) is connected by a direct edge, we can say one transaction is directly approved by another transaction.
* **Indirect Approval:** two transactions are not connected by a direct edge, but there is a directed path of lenth at least two between the two transactions, then we can say the two transactions are indirectly approved.
* **Own Weight:** trasnation's own weight is propotional to the amount of work(computational power or stakes) that issuing node conssumes on proposing a trasnaction(or block).
* **Cumulative Weight:** the sum of the transaction's own weight  and the overall own weight of all transactions that directly or indirectly approve this transaction.
* **Confirmation Weight Threashold:** the threshold value of trasnaction's cumulative weight, when the cumulative weight meet this value, the transaction should be confirmed.

## System Model 

### Network Model

In this subsection, we give some assumptions of Network Model and the definitions of different network load regimes.
<font color = red>
* Assuming that there are $n$ nodes running Tangle, and communicating with each other directly throught wireless channel;
* Assuming that the nodes of a DAG-based blockchain are roughly independently distributed in a large scale IoT network;
* Assuming that the transaction arrival of each user follows the Poisson point process, and the transaction arrival rate of honest user is $\lambda$, and the transaction arrival rate of malicious attacker is $\mu$;
* A new transaction selects two tips according to MCMC select algorithm;
* Assuming that the average own weight of each transaction is setted to  $1$. And the cumulative weight of the observed transaction is its own weight plus the overall number of transactions that directly or indirectly approve it;
* The average transmission delay to broadcast a packet through CSMA/CA is denoted as $h$, which is determined by the computation and transsmission time. That is the time interval between two broadcasted transactions. We can caculate $h$ by the correspongding setting of wireless network. Therefore, $h$ is the reveal time to update the new transactions;
* Assuming that a node can broadcast at most $m$ transactions at once in CSMA/CA. Due to the constrain of broadcast capacity, each user can broadcast a maximum packet of $m$ transactions in each time;
* Assuming that the cache lenth of each node is $Q = km$, and the cumulative weight of an observed transaction at time $t$ is $W(t)$, the total number of tips at time $t$ is $L(t)$.
</font>
### Network Load Regimes

**Definitions:**<font color = blue>
  * Let $\lambda$ be the arrival rate of the node in network.
  * Let the average duration time in reveal stage be $h$, which is determined by the computation and transsmission time.
  * Let $L(t) = 2n\lambda h$ be the number of tips in DAG-based blockchain at time $t$ when considering CSMA/CA protocol. Let $W(t)$ be the cumulative weight of an observed transaction at time $t$ in CSMA/CA.</font>
      
<font color = blue>The network load is stable if $L(t) = L(t-h) = L$, where $L$ is a consistant value.</font> There are $n\lambda h$ new transactions between $t - h$ and $t$ on average. Therefore, we can write $L(t) = r + n\lambda h$, where $r$ is the number of old tips and $n\lambda h$ is the number of tips chosen by new transactions during $t-h$ to $t$ (they are not tips anymore, but other nodes do not know). <font color = green>When a new transaction arrives at time $t$, two tips from $L(t)$ will be chonsen randomly by the transaction.</font> Since $\lambda h$ are not tips anymore, tips selection from $r$ or $\lambda h$ will affect the value of $L(t)$. 
* If new transaction selects two tips both from $n\lambda h$, then $L(t)$ will increase by $1$; 
* If it selects one tip from $r$ and $n\lambda h$, $L(t)$ will unchange; 
* If it selects two tips from $r$, then $L(t)$ will decrease by $1$. 

The expected number of selected tips in $r$ can be computed as $$\frac{n\lambda h(n\lambda h - 1)}{(r + n\lambda h)(r + n\lambda h -1)}\times 0 + \frac{2rn\lambda h}{(r + n\lambda h)(r + n\lambda h - 1)}\times 1 + \frac{r(r - 1)}{(r + n\lambda h)(r + n\lambda h - 1)} \times 2 = \frac{2r}{r + n\lambda h}$$

Because of the stability of $L(t)$, we have $\frac{2r}{r + n\lambda h} = 1$. Therefore, $r = n\lambda h, L = L(t) = 2n\lambda h$.

According to the state of network load, we can divide the network load into Steady and unsteady.

* **Steady Network Load**

  The network load keeps steady means that the transaction arrival rate in network is stable. We can divide steady network load into light load regime and heavy load regime.  
    * **Light Load Regime:** 
      * The typical number of tips is small, and frequently becomes $L_l(t) = 1$;
      * Assume the network is lightly loaded with $\lambda_l$, since each node has the equal probability $(\frac{1}{n})$ to broadcast due to the fairness of CSMA/CA, the average time to compete the broadcasting on each user is $nh$, the  cumulative transactions waiting for broadcasting on each user is $nh\lambda_l$.
      * Let $h_l$ be the average interarrival time between two transactions. In CSMA/CA, the value of $h_l$ is closely related to CSMA/CA communication protocol. If $L(0) > 1$, the number of tips will reduced to $1$ gradually because of the low transaction arrival rate. If $L(0) = 1$, then the DAG-based blockchain will be a single chain.
    * **Heavy Load Regime:**
      * The typical number of tips is large.
      * Network becomes heavily loaded with $\lambda_h$, the cumulative transactions on each node is $nh\lambda_h$.
      * Let $h_h$ be the average interarrival time between two transactions. That is determined by the computation and competitive power of nodes in network. In this case, the number of tips is randomly determined by the approval tips selection algorithm of system. And the number of tips at any time $t$ should be $L(t) = 2n\lambda_hh_h$

* **Unsteady Network Load**
  
  Network load may not alway keep steady. Based on the difinition of two steady load regimes, we can define the unsteady regimes as follows:  
    * **Heavy-to-Light Load:** 
      * <font color = blue>A regime is defined as Heavy-to-Light load when the transaction arrival rate decreases from $\lambda_h$ to $\lambda_l$ suddenly.</font>
      * In H2L(Heavy-to-Light ) regime, the number of tips should be $L(0) = 2n\lambda_hh_r$ if the transaction is observed before network load is changed. If a transaction is revealed after the time that transaction arrival rate has changed to $\lambda_l$, and earlier than the time that $L = 1$, then the $L(0) \in (2n\lambda_h, 2]$. If a transaction is observed to all nodes when the number of tips satisfies $L(0) = 1$, then all new incoming transactions would indirectly approve the observed transactions.
      * We can analyze the propability of an observed transaction in each step as follows. When a new transaction arriving, two tips in $L(k), k = 0, h, 2h, \cdots$ will be chosen to approval. The transaction's cumulative weight either increase $1$ or not. We have that the probability that selecting to approve the observed transaction for $W(k+1) = W(k) + 1$ is $\frac{2}{L(k)}$, and the probability that new transaction not approve the observed transaction for $W(k + 1) = W(k)$ is $1 - \frac{2}{L(k)} = \frac{L(k) - 2}{L(k)}$. Thus, the probability in each time interval $h$ should be summarized as follows:
        $$\left\{
          \begin{aligned}
          P\{i+1,j-1 | i,j\} = \frac{2}{j}, &  & i = 1, 2, \cdots, L_h - 1, j = 2,3,\cdots, L_h, \\
          P\{i,j-1 |i,j\} = 1 - \frac{2}{j}, &  & i = 1, 2, \cdots, L_h - 1, j = 2,3,\cdots, L_h, \\
          P\{i+1, 1 | i,j\} = 1, & & i = 2, \cdots, \infty, j = 1.
          \end{aligned}
        \right.$$
        where $i$ is the number of cumulative weight of the observed transaction, and $j$ is the number of tips.
      * There are three possible cases in H2LR(Heavy-to-Light Regime).
        * The first case is that transaction arrival rate changes from $\lambda_h$ to $\lambda_l$ before $W(t) = w$, where $w$ is transaction confirmation weight threshold. In this case, the consensus process is similar to the heavy regime. 
        * The second case is that transaction arrival rate changes from $\lambda_h$ to $\lambda_l$ when observed trasnaction has $W(t) = 1$. In this case, the number of tips in DAG-based blockchain will gradually decrease to $1$. We have that the probability that new trasnaction approves the observed transaction should be:
        $$\left\{
          \begin{aligned}
          P\{i+1,j-1 | i,j\} = \frac{2}{j}, &  & i = 1, 2, \cdots, L_h - 1, j = 2,3,\cdots, L_h, \\
          P\{i,j-1 |i,j\} = 1 - \frac{2}{j}, &  & i = 1, 2, \cdots, L_h - 1, j = 2,3,\cdots, L_h.
          \end{aligned}
        \right.$$
        * The third case is that transaction arrival rate changes from $\lambda_h$ to $\lambda_l$ at earlier time. The number of tips in DAG-based blockchain satisfies $L(0) = 1$ when a trasnaction is observed. In this case, the consensus process is similar to the light regime. 
    * **Light-to-Heavy Load:**
      * <font color = blue>A regime is defined as Light-to-Heavy load when the transaction arrival rate changes from $\lambda_l$ to $\lambda_h$ suddenly. The number of tips will increase to $2n\lambda_h h_h$ gradually.</font>
      * The number of tips in DAG-based blockchain should be $L(0) = 1$ before transaction arrival rate increasing from $\lambda_l$ to $\lambda_h$ in L2HR(Light-to-Heavy Regime). If a transaction is observed when transaction arrival rate increasing from $\lambda_l$ to $\lambda_h$, the number of tips may increase from $1$ to $2n\lambda_hh$. If a transaction is revealed before network load is changed, the observed transaction will be covered by all new incoming transactions, which means that the cumulative weight of the observed transaction will increase linearly. The transition probability under L2HR should be $P\{W(k+1) = i+1 | W(k) = i\} = 1$. While $L(0) = 2n\lambda_hh$, the consensus process of L2HR should be same with HR.
      * There are four possible cases in L2RR(Light-to-Heavy Regime).
        * The first case is that transaction arrival rate increase from $\lambda_l$ to $\lambda_h$ when the cumulative weight of an observed transction is $W(t) = w$. In this case, the weight accumulating process should satisfy $W(t) = n\lambda_lt, L(t) = L(0) = 1$.
        * The second case is that transaction arrival rate increase from $\lambda_l$ to $\lambda_h$ when the cumulative weight of an observed transction is $W(0) = 1$. In this case, the weight accumulating process should satisfy $W(t) = n\lambda_ht, L(t)\in(1, 2n\lambda_hh_h]$. 
        * The third case is that transaction arrival rate increase from $\lambda_l$ to $\lambda_h$ when the number of tips is $L(0) = 2n\lambda_hh_h$. In this case, the consensus process of an observed transaction under L2HR is same with HR.
        * The forth case is that an trasnaction is observed while $1 < L(0) < 2n\lambda_hh_h$ under L2HR. In this case, the number of tips in DAG-based blockchain will gradually increase. <font color = yellow>We have that the probability that new trasnaction approves the observed transaction should be:
        $$\left\{
          \begin{aligned}
          P\{i+1,j-1 | i,j\} = \frac{2}{j}, &  & i = 1, 2, \cdots, L_h - 1, j = 2,3,\cdots, L_h, \\
          P\{i,j-1 |i,j\} = 1 - \frac{2}{j}, &  & i = 1, 2, \cdots, L_h - 1, j = 2,3,\cdots, L_h.
          \end{aligned}
        \right.$$</font>

## Consensus Process

The consensus process of an issued transaction is divided into two stages: reveal stage and weight accumulating stage.
  * **Reveal Stage:** The observed transaction ia appended to the DAG-based blockchain, that is all nodes can see the transaction.
  * **Weight Accumulating Stage:** the cumulative weight of the observed transaction increases from its own weight to confirmation threshold gradually.

The main procedures that consensus process in wireless network are as follows:
<font color = pink>
* A node finds a nonce to solve a cryptographic puzzle to meet the difficult target.
* The node issues a new transaction which will select two nonconflicting tips to approve based on local information;
* The node uses its private key to sign this new transaction. The new transaction will enter into cache waiting for broadcasting through wireless channel;
* The node competes for wireless channel following CSMA/CA while the new transaction queues in cache following first in first out(FIFO) rule;
* The node either broadcasts the transaction successfully or rebroadcasts with backoff;
* Other nodes receive the new transaction and check it to confirm legality. If the new transaction is legal, then it will become a new tip and wait for the direct or indirect approvement for confirmation. 
</font>
As we can see that communication may cause a serious delay when user competes for wireless channel to broadcast the new transaction. This delay is depends on the network traffic load.

## Performance Ananlysis

When analyzing the performance of DAG-based blockchain, we usually discuss two metrics: transaction confirmation delay and transaction cumulative weight.

### Cumulative Weight

In this section, we discuss the weight accumulating process of an observed transaction in different network load regimes. 

#### Steady Regime

In these regimes, the transaction arrival rate keeps steady. Let $\lambda_l, \lambda_h$ be the transaction arrival rates in light network load and heavy network load, and $h_l, h_h$ be the during time between two transactions.

* **Light Load Regime:** In this regime, the earlier transaction is revealed to the DAG-based blockchain before a new transaction arriving. The total number of tips will gradually decrease to $1$. Thus, it is available to represent the number of tips in LR as $L_l = 2n\lambda_lh_l \approx 1$. When $L_l(0) = 1$, the DAG-based blockchain should be a single chain. And the cumulative weight of an observed transaction will grow with speed $\lambda_l$, which means that the weight of the observed transaction should be increased linearly. More over, all newcoming transactions will approve this transaction. We can define the weight accumulating function with variable time $t$ under light load regime as 
  $$W_\ell(t) = 1 + \lambda_lt.$$

* **Heavy Load Regime:** As analyzed in [The Tangle](../References/33.%20The%20Tangle(S.Popov,%20Apr.2018).pdf), the weight accumulation in HR consists of two periods: adaption priod and linear increasing period.
<font color = blue>
  * **Adaption period:** The time from observed transaction is reveal to DAG-based blockchain to the time that almost all tips become the indirected approval of the transaction. Thus, the weight grows with $W_h(t) = 2\exp(\frac{0.352t}{h})$. 
  * **Linear increasing period:** All incoming trancsactions are indirectly approve the observed transaction. The weight grows with speed $\lambda_h$.
</font>
  * Let $L_h = 2n\lambda_hh_h$ be the number of tips in DAG-based blockchain at time $t$, and $t_0$ is the end time of adaption period. The cumulative weight in adaption period increases exponentially, while in linear increasing period increasing linearly. Thus, the gradient at the end of adaption period is same with the gradient in linear increasing period, i.e. $\frac{dW_h(t)}{dt} = \lambda_h$. We can compute the value of $t_0 = \frac{nh_h}{0.352}\cdot\ln(\frac{n\lambda_hh_h}{0.704}), W_h(t_0) = \frac{n\lambda_hh_h}{0.704}$. The cumulative weight of an observed transaction in high load is 
  $$W_h(t)) = \left\{
  \begin{aligned}
    2\exp(\frac{0.352t}{nh_h}), &  & t \leq t_0\\
   \frac{n\lambda_hh_h}{0.704} + \lambda_h(t-t_0), & & t > t_0.
    \end{aligned}
  \right.$$

#### Unsteady Regime

In unsteady regimes, transction arrival rate will be changed suddenly. We will discuss two special unsteady regimes: light-to-high load and high-to-light load.

* **Heavy-to-Light Load Regime:**
  The initial tips of H2L regime is $L_{h2l}(0) = 2n\lambda_hh_h$. After modifying the network load, Before the network load is changed, the time of the transaction that has been observed will impact the weight accumulation.
  * If a transaction is confirmed before transaction arrival rate decreasing to $\lambda_l$, then the transaction weight accumulating of H2L regime should same with HR: 
  $$W_{h2l}(t)) = \left\{
  \begin{aligned}
    2\exp(\frac{0.352t}{nh_h}), &  & t \leq t_0\\
   \frac{n\lambda_hh_h}{0.704} + \lambda_h(t-t_0), & & t > t_0.
    \end{aligned}
  \right.$$
  * If a transaction is observed after the time that transaction arrival from $\lambda_h$ to $\lambda_l$, we have $L_{h2l} \in (2n\lambda_hh_h, 1), W_{h2l}(0) = 1$ for the observed transaction. The transition probability of the trasnaction in a time interval $h_l$ should be
  $$\left\{
    \begin{aligned}
     P\{i+1,j-1 | i,j\} = \frac{2}{j}, &  & i = 1, 2, \cdots, L_h - 1, j = 2,3,\cdots, L_h, \\
      P\{i,j-1 |i,j\} = 1 - \frac{2}{j}, &  & i = 1, 2, \cdots, L_h - 1, j = 2,3,\cdots, L_h.
    \end{aligned}
  \right.$$
  Thus,we obtain the weight accumulation of this transction under H2L regime is 
  $$W_{h2l}(t)) = \left\{
  \begin{aligned}
    2\exp(\frac{0.352t}{nh_l}), &  & t \leq t_0\\
   \frac{n\lambda_lh_l}{0.704} + \lambda_l(t-t_0), & & t > t_0.
    \end{aligned}
  \right.$$
  * If a transaction is observer while $L_{h2l}(0) = 1$ under H2L regime, all new incoming transactions would become the approvement of the transaction. In this case, the cumulative weight of the observed transaction is similar to LR
  $$W_{h2l}(t) = 1 + \lambda_lt.$$


* **Light-to-Heavy Load Regime:** 
  Due to $L_{l2h}(0) = 2n\lambda_lh \approx 1$ before network load is changed, we thought that all new incoming transctions will approve an observed transction. However, the time of the transaction that has been observed will impact the weight accumulation. 
  * If a transaction is confirmed before the time that transaction arrival rate increases from $\lambda_l$ to $\lambda_h$, the cumulative weight of the transaction at time $t$ should be $$W_{l2h}(t) = 1 + \lambda_lt.$$
  * If a transaction is revealed before the time that transaction arrival rate increases from $\lambda_l$ to $\lambda_h$, which means that the number of tips is $L_{l2h}(t) = 1$, all new incoming transaction with speed $\lambda_h$ will approve the transaction. Thus, the cumulative weight of the transaction at time $t$ should be $$W_{l2h}(t) = 1 + \lambda_ht.$$
  * If transaction is observed after the network load is modified, which means that the number of tips in DAG-based blockchain is $L_{l2h}(t) > 1$, then the cumulative weight of the transaction is
  $$W_{l2h}(t)) = \left\{
  \begin{aligned}
    2\exp(\frac{0.352t}{nh_h}), &  & t \leq t_0\\
   \frac{n\lambda_hh_h}{0.704} + \lambda_h(t-t_0), & & t > t_0.
    \end{aligned}
  \right.$$


### Transaction Confirmation Delay

In order to confirm a new transaction, two periods of delay may happens in both **queuing in communication network** and **blockchain weight accumulating in consensus process**. Weight accumulating of a new transaction is composed of two subperiods: **adaptation subperiod** and **linear increasing subperiod**. Therefore, transaction confirmation delay consists of the queuing delay(counting  from the time that the transaction arrives into cache to the time that it is broadcast) and the weight accumulating delay(adaptive duration time and linear incrase duration time). In this case, we can express the confirmation delay $T_d$ as follows:
$$T_d = T_q + T_a + T_l.$$
where $T_q, T_a, T_l$ are transaction queuing delay, cumulative weight adapting delay and cumulative weight linear increasing delay respectively. Both transaction queuing delay and weight accumulating delay are closely related to the during time between two neiboring transactions $h$. 

**The Average Transmission Delay $h$**

In CSMA/CA, all nodes will compete to send messages. We always split time into multiple slots, and let the probability of each node sending messages in a slot be $\tau$. If there are $n$ nodes in wireless blockchain network, the probability of at least one node broadcasting in a slot time  is 
$$P_{tr} = 1 - (1 - \tau)^{n}.$$

The probability of one node broadcasts successfully in a slot time is 
$$P_s = C_n^1 \tau(1 - \tau)^{n-1} = n\cdot\tau\cdot(1 - \tau)^{n-1}$$
 
 The probability of broadcast collision occuring in a slot time is 
 $$P_c = 1 - (1 - \tau)^{n} - P_s.$$

Let $T_s$ be the average time that channel is detected busy due to a successful broadcasting, and its probability is $P_s$. Denoting $T_c$ is the average time that channel is collision, the probability of broadcast collision is $P_c$. Besides, when the channel is free that no node broadcast in a slot time, let $\sigma$ be the duration time of the empty slot time, the probability of this regime is $1 - P_{tr}$. Therefore, the average transmission delay $h$ is the expected value of the above three situations:
$$h = (1 - P_{tr})\cdot\sigma + P_s\cdot T_s + P_c\cdot T_c.$$

The RTS/CTS exchange in the CSMA/CA protocol are shown as follows:
![](./../pics/Figure_1.png)

In order to  ensure the fairness of CSMA/CA, each node has same probability $\tau$ to access the wireless channel to broadcast. We first analyze the average queuing time of a new transaction in different network load regimes.
* **Light Regime:** When the network load is light, the cache on each node may has less than $m$ transactions(where $m$ is the maximum number of transaction that one packet containning). 
  * **Queuing Time:** If $n\lambda_lh \leq m$, the average queuing delay of a transaction is 
  $$T_q = \frac{n\lambda_lh}{2\lambda_l} = \frac{nh}{2}.$$
  If $n\lambda_lh > m$, the average queuing delay of a transaction is 
  $$T_q = knh - \frac{m}{2\lambda_l}.$$
   Where $k$ is competition times for broadcasting because of FIFO(all new incoming transaction should wait in cache until the previous transactions have been sent), and $\frac{m}{2\lambda_l}$ is the average time of a new transaction from the time that it is stored in cache to the time that it becomes the first transaction in cache. 

  * **Weight Accumulating Time:** While  $n\lambda_lh \leq m$, the cumulative weight of an observed transaction grows with speed $\lambda_l$. Thus, the weight accumulating delay is $$T_w = \frac{w-1}{\lambda_l},$$
  where $w$ is the cumulative weight threshold. In this case, the transaction confirmation delay is 
  $$T_d = T_q + T_w = \frac{nh}{2} + \frac{w-1}{\lambda_l}.$$
  If $n\lambda_lh > m$, and a transaction is confirmed in adaption period, the weight accumulating delay is the adaption delay $T_a = \frac{h}{0.352}\cdot \ln(\frac{w}{2})$. If a transaction cannot be confirmed in adaption period, the cumulative weight of a new transaction grows with $W_a(t) = 2\exp(\frac{0.352t}{h})$. Therefore, the duration time of adaption period in light load is $T_a = \frac{h}{0.352}\cdot\ln(\frac{n\lambda_lh}{0.704})$. The cumulative weight of the transaction at the end of adaption period is $w_a = 2\exp(\frac{0.352}{h}\cdot\frac{h}{0.352}\cdot\ln(\frac{n\lambda_lh}{0.704}))$. When the transaction is confirmed in linear increasing period, we can compute the linear increasing duration time is $T_l = \frac{w - w_a}{\lambda_l}$. Thus, we summarize that the transaction confirmation delay in light network load is
  $$T_d = \left\{
  \begin{aligned}
    knh - \frac{m}{2\lambda_l} + \frac{h}{0.352}\cdot\ln(\frac{n\lambda_lh}{0.704}) + \frac{w - w_a}{\lambda_l}, &  & w > w_a\\
    knh - \frac{m}{2\lambda_l} + \frac{h}{0.352}\cdot\ln(\frac{w}{2}), & & w \leq w_a,
    \end{aligned}
  \right.$$
  where $w_a$ is thecum,ulative weight at time $t_0$.

* **Heavy Regime:** 
  * **Queuing Time:** When the network load is heavy, the cache on each node is always full. If a node compete successfully, it will broadcast $m$ transactions, and $m$ new transactions can be stored in cache accordingly. In this case, the average queuing time for new transaction in HR is 
  $$T_q = \frac{kn\lambda_hh - m}{2\lambda_h} = knh - \frac{m}{2\lambda_h}.$$
  * **Weight Accumulating Time:** Similar to light regime, we can calculate the adaption duration time of heavy regime. The cumulative growth rate in adaption period is defined as $\lambda_h$. Therefore, we have $\frac{dW_a(t)}{dt} = n\lambda_h$. The adapton during time is $T_a = \frac{h}{0.352}\cdot\ln(\frac{w}{2})$ when transaction is confirmed in adaption period, where $w$ is the transaction confirmation weight threshold. When the transaction is confirmed during linear increasing period, the adaption delay in heavy load should be $T_a = \frac{h}{0.352}\cdot\ln(\frac{n\lambda_hh}{0.704})$. The cumulative weight of the transaction at the end of adaption period is $w_a = 2\exp(\frac{0.352}{h}\cdot\frac{h}{0.352}\cdot\ln(\frac{n\lambda_hh}{0.704}))$. When the transaction is confirmed in linear increasing period, we can compute the linear increasing duration time is $T_l = \frac{w - w_a}{\lambda_h}$. Thus, we summarize that the transaction confirmation delay in heavy network load is
  $$T_d = \left\{
  \begin{aligned}
    knh - \frac{m}{2\lambda_h} + \frac{h}{0.352}\cdot\ln(\frac{n\lambda_hh}{0.704}) + \frac{w - w_a}{\lambda_h}, &  & w > w_a\\
   knh - \frac{m}{2\lambda_h} + \frac{h}{0.352}\cdot\ln(\frac{w}{2}), & & w \leq w_a,
    \end{aligned}
  \right.$$
  where $w_a$ is thecum,ulative weight at time $t_0$.
 
* **Light to Heavy Regime:** 
  * **Queuing Time:** If a transaction is observed before network load is changed, the average transaction queuing delay may be $T_q = \frac{nh}{2}$ or $T_q = knh - \frac{m}{2\lambda_l}$. While a transaction is observed after the network load modified, the queuing delay of the trasnaction will be changed. Because the transaction arrival rate is increasing from $\lambda_l$ to $\lambda_h$ suddenly, the cache of a node can quickly be full. Thus, the average queuing time in L2HR is 
    $$T_q = knh - \frac{m}{2\lambda_h}.$$
  
  * **Weight Accumulating Delay:** If a transaction in this regime is confirmed before network is changed, the weigit accumulating delay is same with LR. If a transaction is observed before network load is changed, which means the transaction arrival rate increases to $\lambda_h$ suddenly. The transaction confirmation delay is 
  $$T_d = \left\{
  \begin{aligned}
    \frac{nh}{2} + \frac{w-1}{\lambda_h}, &  & m > n\lambda_lh\\
   knh - \frac{m}{2\lambda_l} + \frac{h}{0.352}\cdot\ln(\frac{w}{2}), & & m \leq n\lambda_lh\ \&\ w \leq w_a,\\
   knh - \frac{m}{2\lambda_l} + \frac{h}{0.352}\cdot\ln(\frac{n\lambda_hh}{0.704}) + \frac{w - w_a}{\lambda_h}, &  & m \leq n\lambda_lh\ \&\ w > w_a.
    \end{aligned}
  \right.$$ 

  If a transaction is observed after network changed, the computation of transaction confirmation delay in this regime is identical to high load regime.


* **Heavy to Light Regime:** The  cache of each node in this regime is full before the network load is changed. 
  * **Queuing Delay:** If transaction is observed before network load is changed, the queuing delay of this trasnaction is $T_q = knh - \frac{m}{2\lambda_h}$. If a trasnaction is observed after network load is changed, the average queuing delay of this regime should be
  $$T_q = \left\{
  \begin{aligned}
    knh - \frac{m}{2\lambda_l}, &  & m \leq n\lambda_lh,\\
    \frac{nh}{2\lambda_l}, & & m > n\lambda_lh,
    \end{aligned}
  \right.$$
  * **Weight Accumulating Delay:** If a transaction is confirmed before network load is changed, the computation of transaction confirmation delay in this regime is same with that in high regime. If a trasnaction is observed before network load is changed, the weight accumulating delay is 
   $$T_w = \left\{
  \begin{aligned}
    \frac{h}{0.352}\cdot\ln(\frac{w}{2}), & & w \leq w_a,\\
    \frac{h}{0.352}\cdot\ln(\frac{n\lambda_lh}{0.704}) + \frac{w - w_a}{\lambda_l}, &  & w > w_a.
    \end{aligned}
  \right.$$ 
  In this case, the average transaction confirmation delay is 
   $$T_d = \left\{
  \begin{aligned}
   knh - \frac{m}{2\lambda_l} + \frac{h}{0.352}\cdot\ln(\frac{w}{2}), & & m \leq n\lambda_lh\ \&\ w \leq w_a,\\
   knh - \frac{m}{2\lambda_l} + \frac{h}{0.352}\cdot\ln(\frac{n\lambda_lh}{0.704}) + \frac{w - w_a}{\lambda_l}, &  & m \leq n\lambda_lh\ \&\ w > w_a.
    \end{aligned}
  \right.$$ 

### Throughput of DAG-based Blockchain 

Throughput is an improtant metric that used to measure the performance of blockchain. Throughput of blockchain is the number of confirmed transactions per second. The computation of throughput in these four regimes are shown as follows:
* **LR:** 
  $$TPS_{lr} = \left\{
  \begin{aligned}
   \frac{m}{T_d^{lr}}, & & m \leq n\lambda_lh,\\
   \frac{n\lambda_lh}{T_d^{lr}}, &  & m > n\lambda_lh.
    \end{aligned}
  \right.$$ 
* **HR:** 
  $$TPS_{hr} = \frac{m}{T_d^{hr}}.$$ 
* **L2HR:** 
  $$TPS_{l2hr} = \left\{
  \begin{aligned}
   \frac{m}{T_d^{l2hr}}, & & m \leq n\lambda_lh,\\
   \frac{n\lambda_lh}{T_d^{l2hr}}, &  & m > n\lambda_lh,\\
   \frac{n\lambda_hh}{T_d^{l2hr}}, &  & m \leq n\lambda_hh.
    \end{aligned}
  \right.$$ 
* **H2LR:** 
  $$TPS_{h2lr} = \left\{
  \begin{aligned}
   \frac{m}{T_d^{h2lr}}, & & m \leq n\lambda_lh,\\
   \frac{n\lambda_lh}{T_d^{h2lr}}, &  & m > n\lambda_lh,\\
   \frac{n\lambda_hh}{T_d^{h2lr}}, &  & m \leq n\lambda_hh.
    \end{aligned}
    \right.$$ 

### Transaction Loss Probability

In order to measure the quality of service of the DAG-based blockchain, we define the transaction loss probability recording the ratio that a new transaction cannot be insert into blockchain.
  $$P_{TLP} = \left\{
  \begin{aligned}
   1 - \frac{m}{n\lambda_lh}, & & m \leq n\lambda_lh,\\
   0, &  & m > n\lambda_lh,\\
   1 - \frac{m}{n\lambda_hh}, &  & m \leq n\lambda_hh.
    \end{aligned}
  \right.$$ 


## Security Analysis

In this section, we introduce the most typical double-spending attack model in DAG-based blockchain. Then, we analyze the successful attack probability for double-spending considering CSMA/CA protocols in qireless blockchain network.

### Attack Process and Model

![](./../pics/Figure_2.png)

The typical way that a malicious attacker lunches double spending attack is to construct a fraudulent chain in blockchain system, the main procedures are shown as follows:
* At time $t_0$, attacker broadcasts an honest transaction, and honest nodes will approve it.
* At time $t_1$, the attacker builds a fraud chain in offchain to approve a fraudulent transaction that is conflicted with the honest transaction.
* After time $t_1$, the attacker will continually issue trasnactions to grow the cumulative weight of the fraudulent transaction. The time $t_1$ should be earlier than the end of adaption periof of the honest transaction.
* At time $t_2$, the honest transaction has been confirmed while its cumulative weight attaches $w$. In this case, the victim will send goods or services to the attacker.
* While the cumulative weight of the fraudulent transaction overweights the confirmed honest transaction after time $t_2$, the attacker will broadcast the fraudulent chain to the whole wireless blockchain network.
* Once the attacker contending for wireless channel to broadcast fraudulent branch updating the DAG-based blockchain, the fraud transaction will be accepted by other honest nodes based on the MCMC algorithm due to the higher cumulative weight. The confirmed honest transaction will be orphened in DAG-based blockchain, the victim cannot receive the payment even though it has provided goods or services. In this case, the attacker issues double-spending attack successfully.

We now present some assumptions for double-spending attack analysis.
* Assuming that there are $n-1$ honest nodes and one attacker;
* Let $\lambda, \mu$ be the arrival rate of new trasnactions on a honest node and a malicious attacker respectively.
* let the own weight of each transaction be one.

### Successfull Attack Probability

In this subsection, we analyze the successful attack probability from the perspective of wireless communication. In this case, attacker should win the transaction competition and broadcast the fraudulent chain successfully. I CSMA/CA, the maximum number of broadcast transactions is limited to $m$, thus, the maximum new transaction arrival rate is $\frac{m}{nh}$. 

Recall that we assume there are $n-1$ honest nodes and $1$ attacker in a one-hop wireless blockchain network, the arrival rates of new trasnactions on a honest node and a malicious attacker shold be 
$$\left\{
  \begin{aligned}
   \lambda' = \min\{\lambda, \frac{m}{nh}\},\\
   \mu' = \min\{\mu, \frac{m}{nh}\}.
    \end{aligned}
  \right.$$ 
Thus, we can define the broadcast trasnaction issued by honest nodes and attacker respectively as follows:
$$\left\{
  \begin{aligned}
   p = \frac{(n-1)\lambda'}{(n-1)\lambda' + \mu'},\\
   q = \frac{\mu'}{(n-1)\lambda' + \mu'}.
    \end{aligned}
  \right.$$ 

We can describe the abovementioned attack process as a Markov chain. Let $N_h, N_a$ be the number of transactions issued by honest nodes and attacker frome time $t_1$ to time $t_2$. Because the number of trasnactions that issued by attacker follows negative binomial distribution, the propability mass function of $N_a$ is 

$$P\{N_a = n\} = C_{n + N_h - 1}^{N_h - 1}p^{N_h}q^n.$$ 

If $N_a > N_h$, the attacker issues the double-spending attack successfully at time $t_2$. Otherwise, the attacker requires to catch up the difference of transactions that issued by honest node and attacker until the cumulative weight of fraudulent transaction outnumbers that of honest transaction after time $t_2$. This process can be thought as a Gambler’s Ruin problem, and The attacker needs to catch up the difference of $N_h - N_a + 1$ transactions at least. If $p \leq q$, the attacker will eventually catch up successfully with probability $1$. Otherwise, the attacker will catch up successfully with probability 

$$P_c(N_h - N_a) = (\frac{q}{p})^{N_h - N_a + 1}.$$

Thus, the successful attack probability is
$$\begin{align*}
  P\{\text{attack succeed}\} &= P\{N_a > N_h\}\cdot 1 + P\{N_a \leq N_h\}\cdot P_c(N_h - N_a) \\
   &= \sum_{N_a = N_h + 1}^\infty C_{N_a + N_h -1}^{N_h-1}p^{N_h}p^{N_a} + \sum_{N_a = 0}^{N_h} C_{N_a + N_h -1}^{N_h-1}p^{N_h}p^{N_a}(\frac{p}{p})^{N_h - N_a +1} \\
   &= 1 - \sum_{N_a = 0}^{N_h} C_{N_a + N_h -1}^{N_h-1}(p^{N_h}p^{N_a} - p^{N_a - 1}p^{N_h + 1}), p > q.
   \end{align*}$$

At time $t_1$, the number of transactions approcving the honest trasnactionis $W(t_1) - 1$. Therefore, we can have $N_h = w - W(t_1) + 1$ transactions from $t_1$ to $t_2$. The successful attack probability can be expressed as 
$$P\{\text{attack succeed}\} =  1 - \sum_{N_a = 0}^{w - W(t_1) + 1} C_{N_a + w - W(t_1)}^{w - W(t_1)}(p^{w - W(t_1) + 1}q^{N_a} - p^{N_a - 1}q^{w - W(t_1) + 2}), p > q,$$
where $W(t_1)$ is the cumulative weight of the honest transaction at the end of adaption period. And $p = \frac{(n-1)\lambda'}{(n-1)\lambda' + \mu'}, q = \frac{\mu'}{(n-1)\lambda' + \mu'}$, where $\lambda' = \min\{\lambda, \frac{m}{nh}\},
   \mu' = \min\{\mu, \frac{m}{nh}\}$.

We use $\lambda, \mu$ representing the transaction arrival rates of honest nodes and attacker to model double-spending attack. Besides, our analysis depends on wireless communication protocol, we use $m$ presenting the number of broadcast trasnactions in wireless blockchain network.

### Attack Strategy

In this subsection, we analyze the strategy that can increase the successful attack probability on the perspective of attacker. Because the probability of a successful attack is identically equal to $1$ when $p\leq q$, we only need to analyze the case that $p > q$.

![](./../pics/Figure_3.png)
In order to increase successful attack probability, attacker can adopt a strategy that constructing the fraudulent branch before broadcasting the honest transaction. In this case, there are $N_p$ transactions belongs to honest chain from time $t_1$ to $t_0$. To ensure the success of attack, the number of transactions issued by attacker $N_a$ should be bigger than the number of transactions issued by honest nodes $N_h + N_p$. If $N_a > N_p + N_h$ at time $t_2$, attacker will broadcast fraudulent chain due to attack successfully. Otherwise, attacker should catch up the difference of $N_h + N_p - N_a$. If $p > q$, the successful attack probability of this situation is 
$$P_c(N_h + N_p - N_a) = 1 - \sum_{N_a = 0}^{N_h + N_p}C_{N_h + N_a - 1}^{N_h - 1}(p^{N_h}q^{N_a}-p^{N_a - N_p - 1}q^{N_h + N_p + 1}).$$
<font color = red>随后可以通过试验来分析$N_p, N_h$对于双花攻击成功概率的影响。最后得出结论攻击者想要提高攻击成功的概率就要最小化$N_p, N_h$的值。攻击者无法影响诚实链上的tips选择过程，但是攻击者可以在诚实交易的权重累积过程处于适应期结束之前选择tips创建欺诈链分支。否则一旦诚实交易的权重累积过程进入线性增长时期，所有的tips都将是诚实交易的间接支持，此时发起攻击必定失败。攻击者发起攻击时生成的欺诈交易选择的tips不能直接或者间接支持诚实交易，这样攻击将会无效，最终必然是诚实交易被确认，欺诈交易被孤立。</font>

### Successful Attack Probability in Different Load Regimes

In this paper, we consider four network load regimes: heavy load regime, light load regime, heavy to light load regime and light to heavy load regime. According to the mentioned analysis of double-spending attack, We will discuss the successful attack probability in different network load. To distinguish the impact of network load on $p, q$, we denote $p_h, q_h$ in heavy load and $p_l, q_l$ in light load. Assume that attacker issues attack immediately after broadcasting honest transaction.

* **Heavy Load Regime:** In this regime, transaction arrival rate is very high, and a transaction may be confirmed in adaption period or in linear increasing period. Due to the attacker issuing attack before the end of adaptive period, the cumulative weight of the honest transaction should be $W(t_1)$. Thus, the number of transactions approving the honest transaction at time $t_1$ is $W(t_1) - 1$. At time $t_2$, we have $N_h = w - W(t_1) + 1$, where $w$ is the transaction confirmation weight threshold. Therefore, the successfull attack probability in heavy load can be expressed as 
  $$P_h\{\text{Attack Succeeds}\} = 1 - \sum_{N_a = 0}^{w - W(t_1) + 1} C_{N_a + w - W(t_1)}^{w - W(t_1)}(p_h^{w - W(t_1) + 1}q_h^{N_a} - p_h^{N_a - 1}q_h^{w - W(t_1) + 2})$$
  where $p_h = \frac{(n-1)\cdot\min\{\lambda_h, \frac{m}{nh}\}}{(n-1)\cdot\min\{\lambda_h, \frac{m}{nh}\} + \min\{\mu_h, \frac{m}{nh}\}}, q_h = \frac{\min\{\mu_h, \frac{m}{nh}\}}{(n-1)\cdot\min\{\lambda_h, \frac{m}{nh}\} + \min\{\mu_h, \frac{m}{nh}\}}$.

* **Light Load Regime:** In this regime, the DAG-based blockchain can be considered as a single chain since $L_0 = 1$.The honest transaction is indirectly approved by all tips at time $t_0$. Attacker issues attack immediately after broadcasting the honest transaction. Because the own weight of the honest transaction is $1$, we can know that $N_h = w-1$. The successful attack probability in light load regime is 
  $$P_l\{\text{Attack Succeeds}\} = 1 - \sum_{N_a = 0}^{w} C_{N_a + w - 2}^{w - 2)}(p_l^{w - 1}q_l^{N_a} - p_l^{N_a - 2}q_l^{w + 1})$$
  where $p_l = \frac{(n-1)\cdot\min\{\lambda_l, \frac{m}{nh}\}}{(n-1)\cdot\min\{\lambda_l, \frac{m}{nh}\} + \min\{\mu_l, \frac{m}{nh}\}}, q_l = \frac{\min\{\mu_l, \frac{m}{nh}\}}{(n-1)\cdot\min\{\lambda_l, \frac{m}{nh}\} + \min\{\mu_l, \frac{m}{nh}\}}$.

* **Heavy to Light Load Regime:** In this regime, transaction arrival rate would decrease from $\lambda_h$ to $\lambda_l$ suddenly, which will result the number of tips $L_0 = 2n\lambda_hh$ reducing to $L_0 = 1$.
  * If the honest transaction is confirmed before network change, the attack process in this regime is same with heavy load regime. The probability that attacker launches double-spending attack successfully is 
    $$P_{h2l}\{\text{Attack Succeeds}\} = 1 - \sum_{N_a = 0}^{w - W(t_1) + 1} C_{N_a + w - W(t_1)}^{w - W(t_1)}(p_h^{w - W(t_1) + 1}q_h^{N_a} - p_h^{N_a - 1}q_h^{w - W(t_1) + 2})$$
  where $p_h = \frac{(n-1)\cdot\min\{\lambda_h, \frac{m}{nh}\}}{(n-1)\cdot\min\{\lambda_h, \frac{m}{nh}\} + \min\{\mu_h, \frac{m}{nh}\}}, q_h = \frac{\min\{\mu_h, \frac{m}{nh}\}}{(n-1)\cdot\min\{\lambda_h, \frac{m}{nh}\} + \min\{\mu_h, \frac{m}{nh}\}}$.
  * If network load is changed while revealing the honest transaction, DAG-based blockchain will quickly be a single chain. The probability that attacker launches double-spending attack successfully is 
    $$P_{h2l}\{\text{Attack Succeeds}\} = 1 - \sum_{N_a = 0}^{w - W(t_1) + 1} C_{N_a + w - W(t_1)}^{w - W(t_1)}(p_l^{w - W(t_1) + 1}q_l^{N_a} - p_l^{N_a - 1}q_l^{w - W(t_1) + 2})$$
    where $p_l = \frac{(n-1)\cdot\min\{\lambda_l, \frac{m}{nh}\}}{(n-1)\cdot\min\{\lambda_l, \frac{m}{nh}\} + \min\{\mu_l, \frac{m}{nh}\}}, q_l = \frac{\min\{\mu_l, \frac{m}{nh}\}}{(n-1)\cdot\min\{\lambda_l, \frac{m}{nh}\} + \min\{\mu_l, \frac{m}{nh}\}}$.
  * If the honest transaction is revealed after modifying network load, the probability of successful attack in this case is same with light load regime. Therefore, the successfull attack probability in heavy to light load regime can be expressed as 
  $$P_{h2l}\{\text{Attack Succeeds}\} = 1 - \sum_{N_a = 0}^{w} C_{N_a + w - 2}^{w - 2}(p_l^{w - 1}q_l^{N_a} - p_l^{N_a - 2}q_l^{w + 1})$$
  where $p_h = \frac{(n-1)\cdot\min\{\lambda_h, \frac{m}{nh}\}}{(n-1)\cdot\min\{\lambda_h, \frac{m}{nh}\} + \min\{\mu_h, \frac{m}{nh}\}}, q_h = \frac{\min\{\mu_h, \frac{m}{nh}\}}{(n-1)\cdot\min\{\lambda_h, \frac{m}{nh}\} + \min\{\mu_h, \frac{m}{nh}\}}$.

* **Light to Heavy Load Regime:** 
  * If the honest transaction is confirmed before network change, all new incoming transactions will indirectly approve the honest transaction. The probability that attacker launches double-spending attack successfully is 
    $$P_{l2h}\{\text{Attack Succeeds}\} = 1 - \sum_{N_a = 0}^{w} C_{N_a + w - 2}^{w - 2}(p_l^{w - 1}q_l^{N_a} - p_l^{N_a - 2}q_l^{w + 1})$$
    where $p_l = \frac{(n-1)\cdot\min\{\lambda_l, \frac{m}{nh}\}}{(n-1)\cdot\min\{\lambda_l, \frac{m}{nh}\} + \min\{\mu_l, \frac{m}{nh}\}}, q_l = \frac{\min\{\mu_l, \frac{m}{nh}\}}{(n-1)\cdot\min\{\lambda_l, \frac{m}{nh}\} + \min\{\mu_l, \frac{m}{nh}\}}$.
  * If network load is changed while revealing the honest transaction, all new incoming transactions will indirectly approve the honest transaction. The probability that attacker launches double-spending attack successfully is 
    $$P_{l2h}\{\text{Attack Succeeds}\} = 1 - \sum_{N_a = 0}^{w} C_{N_a + w - 2}^{w - 2}(p_h^{w - 1}q_h^{N_a} - p_h^{N_a - 2}q_h^{w + 1})$$
    where $p_h = \frac{(n-1)\cdot\min\{\lambda_h, \frac{m}{nh}\}}{(n-1)\cdot\min\{\lambda_h, \frac{m}{nh}\} + \min\{\mu_h, \frac{m}{nh}\}}, q_h = \frac{\min\{\mu_h, \frac{m}{nh}\}}{(n-1)\cdot\min\{\lambda_h, \frac{m}{nh}\} + \min\{\mu_h, \frac{m}{nh}\}}$.
  * If the honest transaction is revealed after modifying network load, the probability of successful attack in this case is same with heavy load regime. Therefore, the successfull attack probability in light to heavy load regime can be expressed as 
  $$P_{l2h}\{\text{Attack Succeeds}\} = 1 - \sum_{N_a = 0}^{w - W(t_1) + 1} C_{N_a + w - W(t_1)}^{w - W(t_1)}(p_h^{w - W(t_1) + 1}q_h^{N_a} - p_h^{N_a - 1}q_h^{w - W(t_1) + 2})$$
  where $p_h = \frac{(n-1)\cdot\min\{\lambda_h, \frac{m}{nh}\}}{(n-1)\cdot\min\{\lambda_h, \frac{m}{nh}\} + \min\{\mu_h, \frac{m}{nh}\}}, q_h = \frac{\min\{\mu_h, \frac{m}{nh}\}}{(n-1)\cdot\min\{\lambda_h, \frac{m}{nh}\} + \min\{\mu_h, \frac{m}{nh}\}}$.
