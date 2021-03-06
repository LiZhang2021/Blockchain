#  DAG Blockchains

Some previous papers pay more attention on blockchain system with "single chain" structure. However, this architecture makes forking illegal. 

To reduce the probability of forking and maintain a single version of blockchain among all nodes in the network, the conventional approaches must *slow down the generation rate of new blocks*. This design principle causes the following two bottlenecks:
* **Throughput limitation:** since the capacity of the blocks is limited, the transaction throughput is usually limited to dozens.
*  **Confirmation delay:** low block generation rate results in long confirmation delay.

To maintain the security of the single chain structure, one block needs to contain high computational power or coinage. This causes the other two bottlenecks for IoT systems:
*  **Fairless:** only the nodes with high computational power or coinage have the right to generate new block. 
*  **High Transaction fee:** unfairness leads to professional and powerful miners. 

These bottlenecks restrict the application of blockchain in IoT systems with limited resource and large-scale. For these restriction, some papers proposed DAG-based blockchain that allows any node to insert a new block into the ledger immediately. In the following, we introduce some blockchain systems with DAG(Directed Acyclic Graph ) structure, which improves the throughput of transaction in Blockchain, and reduces the delay of confirming transaction. Thus, the DAG-based blockchain system may be more suitable for IoT field. 

## IOTA

IOTA is a new micro payment cryptocurrency optimized for the Internet of Things, with tamper-proof data, feeless micro transactions and low resource requirements. The main innovation of IOTA is Tangle, which is scalable, lightweight, and exchange value and data securely, without any fees. It ensures that the information is trustworthy and cannot be tampered with nor destroyed. We will introduce the details of Tangle in the following.

### Basic Concepts


Compare to PoW and PoS, Tangle has higher throughput because it allows different branches to merge into the main chain eventually. 
As shown in Fig.1, Tangle uses directed acyclic graph topology to record transaction, and the unit of Tangle should be a recorded **transaction, approved tips, digital signature, own weight, and cumulative weight**. The basic concepts of Tangle are represented as follows:
<font color = blue>
* **Transaction:** In Tangle, a transaction contains transaction identity, own weight, cumulative weight, and its references parents' identities.
* **Tip:** the transaction(or block) that has not been approved by any other trasnaction(or block). That is, tips are unapproved transactions in tangle graph;
* **Direct Approval:** two transactions(or blocks) is connected by a direct edge, we can say one transaction is directly approved by another transaction.
* **Indirect Approval:** two transactions are not connected by a direct edge, but there is a directed path of lenth at least two between the two transactions, then we can say the two transactions are indirectly approved.
* **Own Weight:** trasnation's own weight is propotional to the amount of work(computational power or stakes) that issuing node conssumes on proposing a trasnaction(or block).
* **Cumulative Weight:** the sum of the transaction's own weight  and the overall own weight of all transactions that directly or indirectly approve this transaction.
* **Confirmation Weight Threashold:** the threshold value of trasnaction's cumulative weight, when the cumulative weight meet this value, the transaction should be confirmed.
</font>

![](./pics2/Figure_1.png)

### Transaction Confirmation

Before issuing a transaction, nodes should compute a nonce, which makes the solution of a cryptographic puzzle meet the difficult target.  A transaction is confirmed when its cumulative weight is large enough. In this case, the consensus mechanism of Tangle is PoW cumulative weight. The weigh accumulating process of an issued transaction is divided into two stages: reveal stage and weight accumulating stage.
<font color = blue>
  * **Reveal Stage:** The observed transaction is appended into the DAG-based blockchain, that is all nodes can see the transaction.
  * **Weight Accumulating Stage:** the cumulative weight of the observed transaction increases from its own weight to confirmation threshold gradually.
</font>

After issuing a transaction, node will choose two issued transactions(unverified transactions-Tips) randomly by MCMC selection algorithm. Then, the node will verify the legality of the two selected transaction.  Node will check the correctness of transaction signature, the proof of work of transaction, and whether it conflicts with transactions directly or indirectly connected to it. If there is a conflict, the old transaction is reselected; otherwise, the verification is passed. After transactionverification, the new generated transaction will reference these verified transaction. 

### DAG Consensus Process

In IOTA, all nodes reach agreement on system by DAG consensus that requires  new transaction sent by nodes verify the previous transaction by referencing them. The main procedures of consensus process in Tangle are as follows:
<font color = purple>
* A node finds a nonce to solve a cryptographic puzzle to meet the difficult target.
* The node creates a new transaction which will select two nonconflicting tips to approve by MCMC tips selction algorithm;
* The node uses its private key to sign this new transaction, and broadcasts the transaction to others;
* Other nodes receive the new transaction and check it to confirm legality. If the new transaction is legal on the digital signature and nonce, then it will become a new tip and wait for the direct or indirect approvement for confirmation. 
</font>

### Double-Spending Scenarios


If an attacker tries to spend the same output twice, there are two possible situations:
* If there is approvement relationship between the two transactions(i.e. one trasnaction directly or indirectly approve another one), then it is obviours that we will reject the later transaction.
* If there is no approvement relationship. In this case, it is possible for the attacker that its dishonest subtangle outpaces the honest subtangle. If this happens, the main tangle continues growing from the doublespending transaction, and the legitimate branch with the original payment to the merchant is orphaned. Thus, IOTA relies on the honesty of transaction.

![](./pics3/Figure_1.png)

Because a transaction is confirmed when its cumulative weight reaching threshold, thus the subtangle with more transactions(more PoW cumulative weight) will win. In this case, we can compute the the successful double-spending attack probability to analyze the security of IOTA. As result, we can improve the security of IOTA by reducing the impact of factors that related to the probability of successful double-spending attack.

Besids, all these results are based on high-frequency trading.  Since low-frequency transactions will lead to lower transaction generation rate, which means that some transactions may not be confirmed quickly according to preseted confirmation threshold. For this situation, a new mechanism is needed in IOTA to ensure fast confirmation of transactions. IOTA had proposed centralized coordinator to confirm transaction in low-frequency trading situation. However, this solution is highly centralized, which is contrary to the decentralized nature of blockchain technology.
 
## Byteball

Byteball is a decentralized	system that allows	tamper proof storage of	arbitrary data. Storage	units are linked to	each other such that each	storage	unit includes one or more hashes of	earlier	storage	units, which serves	both to	confirm	earlier	units and establish	their partial order. The set	of links among units forms a DAG (directed acyclic graph). To store data in the global decentralized database we have to pay a fee in internal currency called bytes, and the amount we pay is equal to the size of data you are going to store(including all headers, signatures, etc). 

### Basic Concepts

The storage unit in Byteball include **unit message, signature and parent unit**
* **Unit Message:** A unit message includes more than one data package(i.e. Message).
* **Signature:** A unit contains the signatures of users who creates the unit.
* **Parent Unit:** A unit contains the hash of referenced previous units.

Byteball adopts UXTO transaction model.  The	message	contains:
* An array of outputs: one or more addresses that receive the bytes	and	the amounts	they receive.
* An array of inputs: one or more references to	previous outputs that are used to fund the transfer. These are outputs that were sent to the author address(es)	in the past and are	not yet	spent.

Storage units connected into a DAG, units are werticesand parent-child links are the edges of the DAG. Soecially, the arrows of the DAG are from child unit to parent unit. 
![](pics2/Figure_2.png)

The basic concepts of Byteball are represented as follows:

* **Parent Unit & Child Unit:** If unit A directly arrows unit B, i.e. the path length from unit A to unit B is $1$, then the unit B is the parent of unit A and unit A is unit B's child.
* **Directly Include:** If unit A is the children of unit B, then unit A directly include or verify unit B.
* **Indirectly Include:** If the length of the path that from unit A to unit B is bigger than $1$, then the unit A indirectly include or verify unit B.
* **Tip Unit:** A unit is defined as tip unit if the unit has no child unit. We also call it  unverified unit.
* **Genesis Unit:** The unit that constructed by the genesis transaction is called genesis unit. The genesis unit has no parent unit. The index of genesis unit is $0$.
* **Witeness:** Witnesses are reputable users with real-world identities, and users who name them expect them to never try to double-spend.
* **Main Chain:** The main chain is constructed by selecting the "*best parent*" unit from all parent units of a child unit. The main chain built starting from a specific unit, and will never change as new unit are added. 
* **Stable Point:** Different candidate main chains will intersection in some intersection points, which is called **stable point**. The first stable point is genesis unit.
*  **Stable Main Chain:** For all candidate main chain, the path from stable point to genesis unit is exactly same, which is called **stable main chain**. 
* **Unit Level:** the level of a unit is defined as the path length from the unit to genesis unit;
* **Witnessed Level:** Backtracking along the main chain from current unit, and count the number of different witnesses in the path until encountering enough witnesses. Witnessed level is the unit level of the backtracking stop position.
* **The "near-conformity rule":** best parent must be selected among those parents whose witness list differs from child's by at most $1$ mutation. That is, the best parent unit can only be selected from the parents unit that compatible with the current unit to ensure the continuity of the historical perspective. Incompatible parent units are still recognized, but they cannot be the best parent unit. In particular, if a new unit is incompatible with all tips, the parent of the unit should be selected from the parent units of the previous level. 

### Double-Spending Problem

If a node wants to spend the same output twice, there are two possible situations:
* There is partial order between the two conflict units., i.e. one unit directly or indirectly includes the other unit. In this case, it is significant that we can safely reject the later unit.
* There is no partial order between the two units. Byteball will accept both, and then establish a total order between the units, when they are buried deep enough under newer units(usually set a threshold). The unit that appears earlier on the total order is regarded as valid, while the other one is invalid. 

![](./pics3/Figure_2.png)

If someone posts two units such that there is no partial order between them (nonserial	units),	the two units are treated like double-spends even if they don???t try to spend the same output. Such nonserials are handled as described in situation 2 above.


###  The Main Chain Selection Rule

In normal way, nodes mostly like to select slightly less recent units as its new unit's parents. In this case, we can choose a single chain along parent-child links within the DAG, and relate all units to this chain. All the units will either directly lie on main chain, or be reachable from it by a ralatively small number of hops along the edges of the graph.

In Byteball, the optimal paths from any tip its to the genesis unit are denoted as **Candidate Main Chain**. The main chain is constructed by selecting the "*best parent*" unit from all parent units of a child unit. The main chain built starting from a specific unit, and will never change as new unit are added. If nodes star from another tip, they will build another main chain. Different candidate main chains will intersection in some intersection points, which is called **stable point**. (the worst case is that chains are intersection in genesis unit). For all candidate main chain, the path from stable point to genesis unit is exactly same, which is called **stable main chain**. Stable main chain is a deterministic path, and transition from a candidate path to a stable path is a process that gradually changes from uncertain to certain. Thus, the main chain can establish a total order beyween two conflicting nonserial units. The genesis unit has index $0$, the next main chain unit that is a child of genensis has index$1$ and the main chain index can be assigned so on. For units that not lie on the main chain, we can find a main chain indes where this units is first included(directly or indirectly).
![](./pics2/Figure_3.png)

Witnesses is the participants of network that are non-anonymous, high reputable and mainning the network healthy. Nodes select the best parent unit of a new incoming unit according to the level of unit and witnessed. The best parent unit selection strategy consists of the following three components:
* When selecting the best parent unit, a parent unit with higher witnessed level is the best parent unit;
* If the witness level is the same, the one with smaller unit level is regared as the best parent unit;
* If both witness level and unit level are the same, the one with lower unit hash value should be selected as the best parent unit.

In the mentioned strategy, witnesses become the historical perspective of a unit. Each unit can maintian its own witnesses list, and can also refer other units' witnesses list through witnesslistunit function. Ifthe witnesslist of  two units differs at most $1$ mutation, then the two units is **Unit Compatible**.

Byteball requires	that the number of witnesses	is exactly $12$.
* it is sufficiently large to protect against the occasional failures of a few witnesses (they might prove dishonest, or be hacked,	or go offline for a long time, or lose their private keys and go offline forever);
* it is sufficiently small that humans can keep track of all the witnesses to know who is who and change the list when necessary;
* the	one allowed	mutation is sufficiently small compared with the $11$ unchanged witnesses.

### Consensus Process

Byteball adopts DAG consensus and witnesses voting consensus to improve transaction throughput and reduce delay in transaction confirmation, thus effectively solving the problem of Excessive Bifurcation and double-spending. Every new child unit in	the	DAG	confirms its parents, all parents of parents. Thus, it is impossible to revise a unit without cooperating with all its childrens or stealing their private keys. Once a unit is broadcast	into	the	network,and	other	users	start	building their units on	top of it	(referencing it	as parent),	the	number	of	secondary	revisions required to	edit this	unit hence	grows	like	a	snowball.


The main procedures of consensus process in Byteball are as follows:
<font color = purple>
* Before generating a new unit, a node(including general nodes anf witenesses) will choose its parent from candidates according to the best parent selction algorithm(main chain unit with higher witnessed level, lower unit level, and lower unit hash value ).
* The node sign the new unit, pays a fee equal to the size of added date in bytes, and broadcasts the unit to others;
* Other nodes receive the new unit and check it to confirm legality. If the new unit is legal on the digital signature, then it will become a new tip and wait for the direct or indirect approvement for confirmation. 
</font>

The main chain inroduces a total order of all unit in DAG-based blockchain. All new incoming units would like to be the units of his current main chain. The current main chain may be different at different nodes because they may see different sets of childless units. In order to establish total order of units in DAG, Byteball introduces witness, which can also compose a new unit, and select parents from candidates according to the best parent selction algorithm.  The reality of a candidate main chains one might travel along the main chain back in time and count the witness-authored units. According to 12 witnesses mechanism, nodes will stop travel if they had encountered the majority of witnesses. Then, nodes measure the length of path on the graph from the stopped unit to the genesis unit. The candidate main chains with greater witnessed level is considered more "real", and parent bearing this main chain is selected as best parent. If two units have same witnessed leve, unit with lower unit level will be the best parent unit. If many candidate parents have same witnessed level and unit level, the the unit with lower hash value wihh be the best parent. 

Once we have a main chain, we can establish a total order on DAG. We first index the units that lie directly on the main chain. The genesis unit has index $0$, the index of next main chain unit should be increases by $1$, and so on we will assign indexes to units lie on main chain. For units that nit lie on main chain, we can find the index of an main chain unit that first directly or indirectly include these units. According the total order, we can sefely reject the unit with higher MCI when two nonserial conflicting units appear in DAG.
![](./pics3/Figure_3.png)

## TrustNote

TrustNote is a minable public DAG-ledger with an innovative, two-tier consensus mechanism(DAG Consensus and TrustME Consensus) designed for new applications. Its digital token is called ???TTT???. TrustNote has a light architecture and intelligent contract system that supports lightweight application extensions and micro wallets.

### Basic Concepts

In TrustNote, a transaction is viewed as a message. Multiple messages can be combined in to a data block which is called **unit**, and a DAG is formed by inter-referenced units. In TustNote, each Unit must reference multiple previous Units, nodes do not require to *spend computing power and time* for solving consensus problem, nor need to wait for the *completion of strong inter-node data synchronization*.

The basic concepts of Byteball are represented as follows:
* **Unit:** a data structure which can contains many messages generated by the nodes including: Transactions messages, text messages and etc. A unit consists of multiple messages(transactions) of various types.
  * *Header:* The hash value of the previous Unit(parent unit);
  * *Messages:* A Unit contains one or more messages, there are various types of message, and each message type has its own unique data structure.
  * *Signatures:* A Unit contains one or more users??? signatures.
  * *Address:* A user can have multiple addresses; the addresses are generated with BIP- 0044 algorithm.
* **Nodes:** Aany active user, installed TrustNote client (any devices such as phone, pc, IoT, etc.) and having a valid wallet address.TrustNote supports four types of Nodes: Super Node, Full Node, Light Node and Micro Node.
  * *Super Node:* Mining Systems, Cloud Host Server/Workstation, and PC, which generates a deposit contract and paying the deposit, and running the TrustME-PoW mining program.
  * *Full Node:* Cloud Host Server/Workstation, and PC, which maintaining synchronization and verification of ledger data. 
  * *Micro-Node:* Client running on Microcontrollers and Smart Cards.
  * *Light Node:* Client running on Smartphone and Tablet PC.
* **Parent unit & Child unit:** If unit A directly includes unit B, then the unit B is the parent of unit A and unit A is unit B's child. Each unit in TrustNote should reference multiple parents;
* **Genesis Unit:** The genesis unit has no parent and is the first unit in TrustNote DAG ledger.
* **Childness Unit:** Units have no Parent-Child relationship with each other. 
* **Unit Level:** The unit level is defined as the longest path length from that unit to Genesis unit. 
* **Attestor:** A Super node, which participates in a round of consensus and successfully obtains Attestation power.
* **Attestation Level:** To determine the Attestation Level for any unit labelled as starting unit, follow the path along best parent chain, until finding more than half of all Attestors??? Attestation unit along the path. Then calculating the unit level of the stop unit, this value is the Attestation Level of the starting unit. The genesis unit is created by all initial Attestors, so it???s the best parent naturally.
* **PoW Unit:** A unit containing Equihash solution.
* **TrustME unit:** A unit used to determine the MC and its first message is a TrustME Coinbase message.

* **Main Chain:**  A single chain along Child-Parent links within the DAG which is determined by applying the Parent Selection Algorithm recursively.
* **MCI:** Main Chain Index.

### Transaction Confirmation

As new Units are created, each Node keeps track of its current MC, which will constantly change itself as new units arrive. However, certain parts of the MC that are old enough, will remain unchanged. When traveling back, all MCs will come to some point, this point and any previous Units are stable and won???t be changed by the arrival of new Units. Thus,  units referenced(directly or indirectly) by stable unit will be assigned determined main chain index and all transactions contained in theses unit will be confirmed.

### Consensus Process

TrustNote adopts a two-tier consensus mechanism comprising base consensus and TrustME consensus:
* **The based Consensus(DAG consensus)** requires new transaction Units sent by Nodes verify the previous units by referencing them. 
* **The Attested consensus(TrustME consensus)** requires that the sequences of Non-TrustME Units be rigorously determined by TrustME Units generated by the Attestors. (TrustME-PoW scheme, TrustME-BA scheme)

When a TrustME unit becoming a stable unit in the Main Chain, it could finally justify that an Attestor has contributed to TrustNote positively, and thus receive the Attestation reward. A transaction fee is divided and paid to:
* The Node(s) who generate newer Unit and reference this Unit as Parent.
* The Attestor who attested the Unit.

If a Unit is referenced by multiple Child Units, the Node who sends the Child Unit with the smallest hash value will get the referencing fee. To qualifying the rewards, the Main Chain Index (MCI) of the Child Unit must equal or be slightly greater than its Parent???s MCI.

The **best parent unit selection algorithm** is showed as below:
  * Selecting the parent unit with the highest Attestation level as its best parent unit.
  * If there are multiple candidate units, the unit with the lowest unit level will be selected as the best parent unit;
  * If there are still multiple candidate units, the unit with the smallest unit hash is the best parent.

The main procedures of consensus process in TrustNote are as follows:
<font color = purple>
* A node issues a new unit, and select parents from candidates according to the best parent selction algorithm(find less recent main chain unit with higher Attestation level, lower unit level and the smallest unit hash value). 
* The node signs the new unit, and broadcasts the unit to other nodes;
* Other nodes main curretn main chain. when receiving the new unit, nodes will check it to confirm legality. If the new unit and its parent-child link is legal, then it will become a new tip and wait for the direct or indirect approvement for confirmation.
</font>

The double-spending problem in TrustNote is similar to that in Byteball. To solve double-spending problem, TrustNote will first try to find a Main Chain (MC) starting from Genesis Unit on the DAG and assign indexes to the Units that lie on the MC, the Genesis Unit???s index is 0, and so on. Second, for those Units that do not lied on the MC, define their indexes equal to the first MC Unit references this Unit. Eventually, every unit on the DAG has an index. If two units try to use the same output, we just need to compare the value of their indexes named Main Chain Index (MCI). The Unit with a smaller index is valid, the Unit with a larger index is invalid. Besides, the total order of TrustNote is ensured by TrustME-PoW consensus. TrustNote will select a small number of super nodes as Attestors using TrustME-PoW or TrustME-BA. These Attestors have the authority to send TrustME Units, which are similar to other nodes. Only when the TrustME Unit becomes the stable Unit on the MC, the corresponding attestation reward can be obtained, and it references units will be confirmed. 


## Hashgraph

Hashgraph is a distributed ledger technology that has been described as an alternative to blockchains. The hashgraph technology is currently patented, and the only authorized ledger is Hedera Hashgraph.

### Basic Concepts

The hashgraph consensus algorithm is based on the following core concepts.
* **Transactions:** any member can create a signed transaction at any time. All members get a copy of it, and the community reaches Byzantine agreement on the order of those transactions.
* **Gossip:** information spreads by each member repeatedly choosing another member at random, and telling them all they know
* **Hashgraph:** a data structure that records who gossiped to whom, and in what order.
* **Event???** an even includes transactions, two events, timestamp, signature, and communicates with each other by Gossip protocol.
* **See:** If some event $w$ has even$x$ as ancestor, then the event $w$ see event $x$.
* **Strongly See:** An event $x$ can strongly see event $y$ if $x$ can see $y$ and there is a set $S$ of events by more than \frac{2}{3} of the members such that $x$ can see every event in $S$, and every event in $S$ can see $y$.
* **Ancestor & Self-ancestor:** An event $x$ is defined to be an ancestor of event $y$ if $x$ is $y$, or a parent of $y$, or a parent of a parent of $y$, and so on. It is also a self-ancestor of $y$ if $x$ is $y$, or a self-parent of $y$, or a self-parent of a self-parent of $y$ and so on.
* **Round Created Number:** The round created number (or round) of an event $x$ is defined to be $r + i$, where $r$ is the maximum round number of the parents of $x$ (or 1 if it has no parents), and $i$ is defined to be $1$ if $x$ can strongly see more than $\frac{2n}{3}$ witnesses in round $r$ (or 0 if it can???t).
*  **Round Received Number:** The round received number (or round received) of an event $x$ is defined to be the first round where all unique famous witnesses are descendants of $x$.
*  **Witness:** A witness is the first event created by a member(node) in a round.
* **Famous witnesses:** A famous witness is a witness that has been decided to be famous by the community. Informally, the community tends to decide that a witness is famous if many members see it by the start of the next round. A **unique famous witness** is a famous witness that does not have the same creator as any other famous witness created in the same round. In the absence of forking, each famous witness is also a unique famous witness.

![](./pics2/Figure_4.png)

### Event Confirmation

In Hashgraph, members votes according to "see" and "strongly see". An witness(the fir t event of a nodes in a round) is famous if it can be voted by majority witnesses of next round. Then, the withness of the following round will encount the votes. If the witness can strongly see supermajority witnesses of last round, then nodes achieve consensus on the famous witness. In this case, the witness and its ancestors can be confirmed.

### Forking

A node may cheat others by forking or creating two events from same parent event. In this case, the node could have two witnesses in a round. For this problem, Hashgraph use byzantine fault tolerance local vitual voting to ensure that even if an attacker tries to cheat by forking, the events that issued by attacker will still be unable to cause different nodes to decide on different orders.
![](./pics3/Figure_4.png)

### Consensus Process

The main procedures of consensus process in Hashgraph are as follows:
<font color = purple>

* Node repeatly syncs all known eventa to a random node.
* A node who receives a sync will create a new event to record these events with valid signatures containing valid hashes of parent events it has. 
* After gossip sync, the node calls three procedures to determined the consensus order for as many events as possible:
  * Divide Rounds: All known events are then divided into rounds. And node B should assign the round numberto all known events.
  * Decide Fame: Then the first events by each member in each round (the ???witnesses???) are decided as being famous or not, through purely local Byzantine agreement with virtual voting. 
  * Find Order: The total order is found on those events for which enough information is available.
    * the received round is calculated. Event has a received round of $r$ if that is the first round in which all the unique famous witnesses were descendants of it, and the fame of every witness is decided for rounds less than or equal to $r$.
    * the received time is calculated. The received time for an even is the median of all the timestamps of events that is the descendant of the event and the self-ancestors of next round witnesses who can see the event.
    * the consensus order is calculated. All events are sorted by their received round. If two events have the same received round, then they are sorted by their received time. If there are still ties, they are broken by simply sorting by signature, after the signature is whitened by XORing with the signatures of all the unique famous witnesses in the received round.
</font>

The Hashgraph consensus algorithm virtually orders all events through Byzantine consensus protocol. The algorithm does not need to select a leader to order transactions. Sorting phase only requires minimal communication overhead, which is more suitable for consortium blockchain that requires a large number of nodes participating in consensus. However, it is not suitable for public blockchain, because it requires the information of the entire network. Besides, the consensus process takes at least two rounds to determine the order of transactions in the current round, the efficiency of consensus and the timeliness of transaction processing may be not effective. 

## Nano(RaiBlocks XRB)

Nano is a cryptocurrency with a novel block-lattice architecture where each account has its own blockchain, delivering near instantaneous transaction speed and unlimited scalability. Nano was launched in 2014 as a side project of Colin LeMahieu, and completed by launching a fully functional mainnet in 2017. The total token of Nano is fixed and uppers to 133248289 XRB, which is generated at the time that launching mainnet. All transaction in Nano are free and confirmed in 5 seconds. The throughput of Nano is extremely high, and only restricted by computing speed and data transfer latency.

### Basic Concepts

The individual components of Nano are shown as follows:
* **Account:** An account is the public-key portion of a digital signature key-pair. One user may control many accounts, but only one public address may exist per account.
* **Block/Transaction:** A block contains a single transaction. Transaction specifically refers to the action while block refers to the digital encoding of the transaction. 
* **Ledger:** The ledger is the global set of accounts where each account has its own transaction chain. 
* **Node:** A node is a piece of software running on a computer that conforms to the Nano protocol and participates in the Nano network. A node may either store the entire ledger or a pruned history containing only the last few block of each account???s blockchain. Nodes only have to record and rebroadcast blocks for most transactions.
* **Open Transaction:** An open transaction is the first transaction of every account-chain and can be created upon the first receipt of funds.
* **Genesis Balance:** The genesis balance is a fixed quantity and can never be increased. The genesis balance is divided and sent to other accounts via send transactions registered on the genesis account-chain. 
* **Representative:** 
* **Change Transaction:** A change transaction changes the representative of an account by subtracting the vote weight from the old representative and adding the weight to the new representative.
* **Vote Weight:** The weight of a node???s vote is the sum of the balances of all accounts that have named it as its representative.
* **Transaction Verification???** For a block to be considered valid, it must have the following attributes:
  * The block must not already be in the ledger (duplicate transaction).
  * Must be signed by the account???s owner.
  * The previous block is the head block of the accountchain. If it exists but is not the head, it is a fork.
  * The account must have an open block.
  * The computed hash meets the PoW threshold requirement
* **Representative:** representatives are chosen by account holders to represent vote on their behalf.

Nano uses a block-lattice structure. Each account has its own blockchain (account-chain) equivalent to the account???s transaction/balance history. Each account-chain can only be updated by the account???s owner.
![](./pics2/Figure_5.png)

Every transfer of funds requires a send block (S) and a receive block (R). Transferring amounts as separate transactions in the sender???s and receiver???s accounts serves a few important purposes:
* Sequencing incoming transfers that are inherently asynchronous.
* Keeping transactions small to fit in UDP packets.
* Facilitating ledger pruning by minimizing the data footprint.
* Isolating settled transactions from unsettled ones.
![](./pics2/Figure_6.png)

### Transaction Confirmation

In Nano, a sender needs to issue a send transaction in their own blockchain when sending fund, and receiverneeds to issue a corresponding receive transction in their blockchain when reveiving the fund. Since accounts are the only entities that can update their blockchains, each blockchain can be updated instantly and asynchronously. This makes transactions very fast. Once a blockchain update is made, the transaction is broadcast to the whole network. The transaction will be confirmed as long as no validator finds conflict transctions. 

### Forking Problem

A fork occurs when an account  signed blocks claim the same block as their predecessor. These blocks cause a conflicting view on the status of an account and must be resolved. Only the account???s owner has the ability to sign blocks into their account-chain, so a fork must be the result of poor programming or malicious intent (double-spend) by the account???s owner.
![](pics3/Figure_5.png)

When detecting forking, representative will create a vote referencing the block in its ledger, and broadcast network. the weight of a node's vote is the sum of te balances of all accounts that have named it as its representative. The most popular block will have the majority of the votes and will be retained in the node???s ledger. The block(s) that lose the vote are discarded. If a representative replaces a block in its ledger, it will create a new vote with a higher sequence number and broadcast the new vote to network. This is the only scenario where representatives vote.

### Consensus Process

The main procedures of consensus process in Nano are shown as follows:
<font color = purple>
* Each Node creates an account by issuing an open transaction. On account creation, a representative must be chosen to vote on your behalf; this can be changed later. (The system is initiated with a genesis account containing the genesis balance. )
* when transfering a fund, source account should create a send block(transaction). Once broadcasted to network, fund is immediately deducted from the balance of the source account and waits as pending until the receiving party signs a block to accept
this fund. 
* when receiving the fund, destination account will  create a receive block(transaction) on its own account-chain. Once this block is created and broadcasted, the destination account's balance is updated and the fund have officially moved into its account. 
* When detecting a conflicting view on the status of an account, a representative(node) will create a vote referencing the block in its ledger and broadcast it to the network.
* The node will observe incoming votes from the other $M$ online representatives and keep a cumulative tally for $4$ voting periods(1 minute total), and confirm the winning block. The most popular block will have the majority votes and will  be retain in the node's ledger.
</font>

In Nano, the sending and receiving of transactions can be performed asynchronously, which means that an account can receive founds from multiple amounts at the same time. The final amount is the addition of all the amounts received. It doesn???t a matter if the receiver is not online, the unaccounted amount will be marked separately. When the receiving account online, the amount will be entered into the receiving block from the unsettled area to complete the transaction. 


## Conflux

 Conflux is a fast, scalable, and decentralized
blockchain system that can process thousands of transactions per second while confirming each transaction in minutes. 

### Basic Concepts

![](pics2/Figure_7.png)

Some basic concepts of Conflux are shown in the following"
* **Block:** a block consists of transactions, parent ID, reference ID and the signature of its creator ect.
* **Genesis Block:** The firt generated block in conflux.
* **Parent Edge:** Each block except Genesis has exactly one outgoing parent edge (solid line arrows in Figure 2). The parent edge corresponds to a voting relationship, i.e., the node that generates the child block votes for the transaction history represented by the parent block. 
* **Reference Edge:** Each block can have multiple outgoing reference edges (dashed lines arrows in Figure 2). A reference edge corresponds to generated before relationships between blocks. 
* **Pivot Chain:** Note that all parent edges in a DAG together form a parental tree in which the genesis block is the root. In the parental tree, Conflux selects a chain from the genesis block to one of the leaf blocks as the *pivot chain*. Pivot chain Selection rule that Conflux does not select this longest chain because the subtree of A contains more blocks than the subtree of B. Therefore, the chain selection algorithm selects A over B at its first step.
* **Local DAG State:** Each node maintains a local state that contains all blocks which the node is aware of. Because in Conflux each block may contain links to reference several previous blocks not just one, the result state is a direct acyclic graph (DAG)
* **Epoch:** Parent edges, reference edges, and the pivot chain together enable Conflux to split all blocks in a DAG into epochs. 
* **Generating New Block:** Whenever a node generates a new block, it first computes the pivot chain in its local DAG state and sets the last block in the chain as the parent of the new block.
* **Block Total Order:** Conflux determines the total order of the blocks in a DAG as follows. Conflux first sorts the blocks based on their corresponding epochs and then sorts the blocks in each epoch based on their topological order. If two blocks in an epoch have no partial order relationship, Conflux breaks ties deterministically with the unique ids of the two blocks. 
* **Transaction Total Order:** Conflux first sorts transactions based on the total orders of their enclosing blocks. If two transactions belong to the same block, Conflux sorts the two transactions based on the appearance order in the block.

### Transaction Confirmation

The user locates the first epoch that contains a block including the confirming transaction. The user identifies the corresponding pivot chain block of the epoch. The user then decides how much risk it can tolerate based on the estimations of the block generation power that the attacker controls. The user finally estimates the risk of the pivot chain block being reverted to decide whether to confirm the transaction.

### Double-Spending Problem

If an attacker tries to spend the same output twice, there are two possible situations:
* If there is reference relationship between the two conflict transactions(i.e. one trasnaction directly or indirectly reference the other one), then it is obviours that we will reject the later transaction.
* If there is no reference relationship. In this case, it is possible for the attacker that its dishonest subchain outpaces the honest subchain. If this happens, the main chain continues growing from the double-spending transaction, and the legitimate branch with the original payment to the merchant is orphaned. 

In order to prevent double- spending attack, Conflux introduce a pivod chain to order all blocks on DAG ledger. 
* we first sort the blocks referencing only the parent blocks form a pivot chain according to GHOST rule,
* we then divide blcoks into epochs according to pivot chain, and then sort the blocks in each epoch topologically. The principle of determining whether blocks included in an epoch should follows the two conditions at the same time:
  * The block can be tracked through the parent edge or reference edge of the pivot chain,
  * the block is not included in the previous epochs
* Sorting blocks between different epochs according to the happens-before principle (that is, who is ahead of whom).

### Consensus Process

The main procedures of consensus process in Conflux are as follows:
<font color = purple>
* A node packets some transactions from Pending Transaction Pool, and generates a new block.
* The node computes the pivot chain in its local DAG state by pivot chain selection algorithm, and sets the last block in the chain as the parent of the new block. Then the Node selects sibling blocks as the reference blocks of the new block.
*  The node will update its local  DAG state, and broadcasts the updated local DAG blockchain to other nodes.
*  Other node receiving the updated local DAG state will update its local DAG state(after verifying the correctness), and broadcast the updated local DAG state to others.
</font>

The finality of Conflux is based on the estimation of the block computing power controlled by attacker, and transaction confirmation of Conflux is based on the estimated risk. Once generating a new block,  Conflux needs to find a pivot chain from the Genesis block. This process may lead to heavy computing load, which will eventually affect performance. For example, increasing the time of the block generation process and confirmation process. 


## Table of All DAG blockchain Systems

![](pics3/Figure_6.png)

## Summary

DAG????????????????????????????????????????????????????????????DAG????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????

### Advantages of DAG Blockchain

DAG????????????????????????????????????????????????
* **??????????????????????????????** DAG????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????DAG????????????IoT???????????????????????????????????????????????????????????????
* **???????????????** ???????????????????????????????????????????????????????????????????????????????????????????????????POW???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????DAG+TrustMe-POW???????????????TrustNode???
* **??????????????????** IOTA????????????????????????IOTA???????????????????????????????????????????????????????????????????????????????????????????????????IOTA???????????????????????????????????????????????????????????????????????????

### Disadvantages of DAG Blockchain

DAG???????????????????????????
* **????????????????????????????????????????????????** DAG????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
* **????????????????????????** DAG????????????GHOST????????????????????????????????????????????????????????????????????????????????????????????????????????????DAG????????????????????????????????????????????????????????????????????????????????????????????????DAG????????????????????????????????????????????????????????????????????????????????????DAG???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
* **??????????????????????????????????????????:** DAG????????????????????????????????????????????????????????????????????????DAG????????????????????????????????????????????????????????????????????????????????????????????????DAG???????????????????????????????????????**??????**???DAG????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????*????????????DAG???????????????????????????????????????????????????????????????* ???????????????????????????????????????????????????????????????????????????DAG???????????????????????????????????????????????????????????????DAG????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????

## Future Work

????????????????????????????????????

* DAG????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????Tangle??????????????????????????????????????????DAG??????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
* ???????????????????????????????????????Byteball???TrustNote, Hashgraph???????????????????????????????????????????????????????????????DAG????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
* ????????????DAG????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????DAG?????????witnessed consensus(??????????????????????????????????????????CSMA/CA??????????????????????????????????????????????????????????????????????????????????????????DAG?????????????????????)???
  


