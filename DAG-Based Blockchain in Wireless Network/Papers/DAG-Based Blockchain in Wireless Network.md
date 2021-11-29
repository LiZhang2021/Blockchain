# DAG-Based Blockchain in Wireless Network

## DAG-based Blockchain Definitions

* **Block:** the storage unit to records information including transaction, digital signature, and hash value. In tangle, a block just records one transaction;
* **Tip:** the transaction(or block) that has not been approved by any other trasnaction(or block). That is, tips are unapproved transactions in tangle graph;
* **Direct Approval:** two transactions(or blocks) is connected by a direct edge, we can say one transaction is directly approved by another transaction.
* **Indirect Approval:** two transactions are not connected by a direct edge, but there is a directed path of lenth at least two between the two transactions, then we can say the two transactions are indirectly approved.
* **Own Weight:** trasnation's own weight is propotional to the amount of work(computational power or stakes) that issuing node conssumes on proposing a trasnaction(or block);
* **Cumulative Weight:** the sum of the transaction's own weight  and the overall own weight of all transactions that directly or indirectly approve this transaction.
* **Confirmation Weight:** the threshold value of trasnaction's cumulative weight, when the cumulative weight meet this value, the transaction should be confirmed.

## Network Load

* Definitions:
  * Let $\lambda$ be the arrival rate of the new transaction.
  * Let the average duration time in reveal stage be $h_r$, which is determined by the computation and transsmission time.
  * Let $L(t) = 2\lambda h_r$ be the number of tips in the heaviest DAG at time $t$.
      * When the network load is stable, we have $L(t) = L(t-h_r) = L$, where $L$ is a consistant value. There are $\lambda h_r$ new transactions between $t - h_r$ and $t$ on average. Therefore, we can write $L(t) = r + \lambda h_r$, where $r$ is the number of old tips and $\lambda h_r$ is the number of tips chosen by new transactions during $t-h_r$ to $t$(they are not tips anymore, but othere nodes do not know).
      * When a new transaction arrives at time $t$, two tips from $L(t)$ will be chonsen randomly by the transaction. Since $\lambda h_r$ are not tips anymore, tips selection from $r$ or $\lambda h_r$ will affect the value of $L(t)$. If new transaction selects two tips both from $\lambda h_r$, then $L(t)$ will increase by $1$; else if it selects one tip from both $r$ and $\lambda h_r$, $L(t)$ will unchange; else it selects two tips from $r$, then $L(t)$ will decrease by $1$. The expected number of selected tips in $r$ can be computed as $$\frac{\lambda h_r(\lambda h_r - 1)}{(r + \lambda h_r)(r + \lambda h_r -1)}\times 0 + \frac{2r\lambda h_r}{(r + \lambda h_r)(r + \lambda h_r - 1)}\times 1 + \frac{r(r - 1)}{(r + \lambda h_r)(r + \lambda h_r - 1)} \times 2 = \frac{2r}{r + \lambda h_r}$$
        Because of the stability of $L(t)$, value $\frac{2r}{r + \lambda h_r} = 1$. Therefore, $r = \lambda h_r, L = L(t) = 2\lambda h_r$.
  * Let $W(t)$ be the cumulative weight of an observed transaction at time $t$.

* **Stable Network Load**
    * Low Load: 
      * The typical number of tips is small, and frequently becomes $1$;
      * Assume the network is lightly loaded with $\lambda = \lambda_l$,  since each user has the equal probability $(\frac{1}{n})$ to broadcast due to the fairness of CSMA/CA, the average time to compete the broadcasting on each user is $nh$, the  cumulative transactions waiting for broadcasting on each user is $nh\lambda_l$.
      * Let $h_l = \frac{1}{\lambda_l}$ be the average interarrival time between two transactions. when $h_l > h_r$, the load of network is Low. In this case, the number of tips will reduced to $1$ gradually. If $L(0) = 1$, then the DAG-based blockchain will be a single chain.
    * High Load: 
      * The typical number of tips is large.
      * Network becomes heavily loaded with $\lambda = \lambda_h$, the cumulative transactions on each user is $nh\lambda_h$.
      * Let $h_h = \frac{1}{\lambda_h}$ be the average interarrival time between two transactions. when $h_h \leq h_r$, the load of network is high. In this case, the number of tips is randomly determined by the approval tips selection algorithm of system.
* **Unstable Network Load**
  The load of network will not still keep consistent. 
    * High-to-Low Load: 
      * A regime is defined as High-to-Low load when the transaction arrival rate changes frome $\lambda_h$ to $\lambda_l$ suddenly. 
      * The initial state of an observed transaction under H2LR is that cumulative weight $W(0) = 1$ and the number of tips id $L(0) = 2\lambda_hh_r$. And the transaction arrival rate in this regime changes to $\lambda_l$.
      * When a new transaction arriving, two tips in $L(k)$ will be chosen to approval. An observed transaction's cumulative weight either increase $1$ or not change. The probability to select the observed transaction for $W(k+1) = W(k) + 1$ is $\frac{2}{L(k)}$. And the probability of  $W(k + 1) = W(k)$ is $1 - \frac{2}{L(k)} = \frac{L(k) - 2}{L(k)}$.
      * 每一步不同的状态的概率：
         $$\left\{
          \begin{aligned}
          P\{i+1,j-1 | i,j\} = \frac{2}{j}, &  & i = 1, 2, \cdots, L_h - 1, j = 2,3,\cdots, L_h, \\
          P\{i,j-1 |i,j\} = 1 - \frac{2}{j}, &  & i = 1, 2, \cdots, L_h - 1, j = 2,3,\cdots, L_h, \\
          P\{i+1, 1 | i,j\} = 1, & & i = 2, \cdots, \infty, j = 1.
          \end{aligned}
          \right.$$
      * The best case of upper performance bound in H2LR is that transaction arrival rate changes from $\lambda_h$ to $\lambda_l$ when $W(0) = m$. In this case, the consensus process is similar to HR regime. The worst case for lower performance bound in H2LR is that transaction arrival rate changes from $\lambda_h$ to $\lambda_l$ when $W(0) = 1$.
    * Low-to-High Load:
      * A regime is defined as Low-to-High load when the transaction arrival rate changes frome $\lambda_l$ to $\lambda_h$ suddenly. The number of tips will increase to $2\lambda_h h_r$ gradually.
      * The initial state of an observed transaction under L2HR is that cumulative weight $L(0) = 1$ and the transaction will be covered by all new transactions that are directly or indirectly approve the observed transaction. In this case, the cumulative weight of the observed transaction $W(k)$ will increase linearly with speed $\lambda_h$. The transition probabilityies under L2HR are $$P\{W(k+1) = i+1 | W(k) = i\} = 1.$$
      * The best case of upper performance bound in L2HR is that transaction arrival rate changes from $\lambda_l$ to $\lambda_h$ when $W(0) = 1$. The worst case for lower performance bound in L2HR is that transaction arrival rate changes from $\lambda_l$ to $\lambda_h$ when $W(0) = m$.

## Consensus Process

The main procedures that a node wants to issue a new transaction and let other nodes accept it are shown as follows:
* A node finds a nonce to solve a cryptographic puzzle to meet the difficult target;
* The node issues a new transaction and stores in a created storage unit;
* The node select two collision-free tips according to tips selcetion algorithm, and adds the hash of the two selected tips into thr transaction's storage units;
* The node uses it private key to sign the new transaction and broadcasts to other nodes;
* Other nodes will check the legal of the new transaction (based on the digital signature and nonce) when receiving it.

The main procedures that consensus process in wireless network are as follows:
* When a new transaction comes at a user, it should select two nonconflicting tips to approval based on ocal information;
* The user uses its private key to sign this new transaction. The new transaction will enter into cache waiting for broadcasting through wireless cahnnel;
* The user competes for wireless channel following CSMA/CA while the new transaction queues in cache foloowing first in first out(FIFO);
* The user either broadcasts the transaction successfully or rebroadcasts with backoff;
* Other users receive the new transaction and check it to confirm legality. If the new transaction is legal, then it will become a new tip and wait for the direct or indirect approvement for confirmation. 

As we can see that communication may cause a serious delay when user competes for wireless channel to broadcast the new transaction. Thid delay is depends on the network trasffic load.

## System Model 

**Wireless Blockchain Network**

We can divide the consensus process of a new transaction in wireless blockchain network into two periods: **the queueing period**(based on CSMA/CA network communication protocol) and **the weight accumulating preiod**(based on DAG-based blockchain consensus protocol).
* Assuming that there are $n$ users running tangle, and communicating with each other directly throught wireless channel;
* Assuming that the transaction arrical of each user follows the Poisson point process;
* Assuming that the transaction arrival rate of honest user is $\lambda$, and the transaction arrival rate of malicious attacker is $\mu$;
* Assuming that each transaction should have same own weigh, that is one;
* The average transmission delay to broadcast a packet through CSMA/CA is denoted as $h$. That is the time interval between two broadcasted transactions. We can caculate $h$ by the correspongding setting of wireless network. Therefore, $h$ is the reveal time to update the new transactions;
* Assuming that the max number of transactions at one broadcast is $m$. Due to the constrain of broadcast capacity, each user can broadcast a maximum packet of $m$ transactions in each time;
* Assuming that the cache lenth of each user is $Q = km$, and the cumulative weight of  an observed transaction at time $t$ is $W(t)$, the total number of tips at time $t$ is $L(t)$.

**General Network**

* The consensus process is ddivided into two stages: reveal stage and weight accumulating stage.
  * **Reveal Stage:** appending the observed transaction to the DAG-based blockchain, that is all nodes can see the transaction.
  * **Weight Accumulating Stage:** the cumulative weight of the observed transaction increases from its own weight to confirmation threshold gradually.
* Assuming that the average duration time in reveal stage $h$ is determined by the computation and transmission time;
* Assuming that the average own weight of each transaction is setted to  $1$. And the cumulative weight of the observed transaction is its own weight plus the overall number of transactions that directly or indirectly approve it;
* Assuming that the nodes of a DAG-based blockchain are roughly
independently distributed in a large scale IoT network;
* Assuming that the new transaction arrival follows Poisson process.;
* Assuming that the new transactions' arrival rate of honest nodes is denoted as $\lambda$;
* The new transaction selects two tips according to MCMC algorithm. 

## Performance Ananlysis

When analyzing the performance of DAG-based blockchain, we usually discuss two metrics: transaction confirmation delay and transaction cumulative weight.

### Transaction Confirmation Delay

In order to confirm a new transaction, two periods of delay may happens in both **queuing in communication network** and **blockchain weight accumulating in consensus process**. Weight accumulating of a new transaction is composed of two subperiods: **adaptation subperiod** and **linear increasing subperiod**. Therefore, transaction confirmation delay consists of the queuing delay(counting  from the time that the transaction arrives into cache to the time that it is broadcast) and the weight accumulating delay(adaptive duration time and linear incrase duration time). In this case, we can express the confirmation delay $T_d$ as follows:
$$T_d = T_q + T_a + T_l.$$
where $T_q, T_a, T_l$ are transaction queuing delay, cumulative weight adapting delay and cumulative weight linear increasing delay respectively.


### Cumulative Weight





