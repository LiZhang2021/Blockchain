# DAG-Based Blockchain in Wireless Network

## Network Load

* Definitions:
  * Let $\lambda$ be the arrival rate of the new transaction.
  * Let the average duration time in reveal stage be $h_r$, which is determined by the computation and transsmission time.
  * Let $L(t) = 2\lambda h_r$ be the number of tips in the heaviest DAG at time $t$.
      * When the network load is stable, we have $L(t) = L(t-h_r) = L$, where $L$ is a consistant value. There are $\lambda h_r$ new transactions between $t - h_r$ and $t$ on average. Therefore, we can write $L(t) = r + \lambda h_r$, where $r$ is the number of old tips and $\lambda h_r$ is the number of tips chosen by new transactions during $t-h_r$ to $t$(they are not tips anymore, but othere nodes do not know).
      * When a new transaction arrives at time $t$, two tips from $L(t)$ will be chonsen randomly by the transaction. Since $\lambda h_r$ are not tips anymore, tips selection from $r$ or $\lambda h_r$ will affect the value of $L(t)$. If new transaction selects two tips both from $\lambda h_r$, then $L(t)$ will increase by $1$; else if it selects one tip from both $r$ and $\lambda h_r$, $L(t)$ will unchange; else it selects two tips from $r$, then $L(t)$ will decrease by $1$. The expected number of selected tips in $r$ can be computed as $$\frac{\lambda h_r(\lambda h_r - 1)}{(r + \lambda h_r)(r + \lambda h_r -1)}\times 0 + \frac{2r\lambda h_r}{(r + \lambda h_r)(r + \lambda h_r - 1)}\times 1 + \frac{r(r - 1)}{(r + \lambda h_r)(r + \lambda h_r - 1)} \times 2 = \frac{2r}{r + \lambda h_r}$$
        Because of the stability of $L(t)$, value $\frac{2r}{r + \lambda h_r} = 1$. Therefore, $r = \lambda h_r, L = L(t) = 2\lambda h_r$.

* **Stable Network Load**
    * Low Load: 
      * The typical number of tips is small, and frequently becomes $1$;
      * Assume the network is lightly loaded with $\lambda = \lambda_l$,  since each user has the equal probability $(\frac{1}{n})$ to broadcast due to the fairness of CSMA/CA, the average time to compete the broadcasting on each user is $nh$, the  cumulative transactions waiting for broadcasting on each user is $nh\lambda_l$.
      * 
    * High Load: 
      * The typical number of tips is large.
      * Network becomes heavily loaded with $\lambda = \lambda_h$, the cumulative transactions on each user is $nh\lambda_h$.
      * Let $h = \frac{1}{\lambda}$ be the average interarrival time between two transactions. when $h \leq h_r$, the network 
* **Unstable Network Load**
    * High-to-Low Load:
      * 
    * Low-to-High Load:
      * 



