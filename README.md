# DWave_supply_inventory
## Problem Description
As a grocer, we are facing 2 main problems: 
  1. minimizing the number of suppliers 
  2. maximizing the total profit

We will show how D-Wave Constrained Quadratic Models (CQM) Solver to helps us.

## 1. Supplier Optimization
As a typical logistic problem, a grocer needs to minimize the number of suppliers while fully filling the inventory. More specifically, assume that there are totally $N$ different kinds of items $U=\\{U_0,U_1,\cdots,U_{N-1}\\}$. There are $M$ different suppliers $S=\\{S_0,S_1,\cdots,S_{M-1}\\}$ as well, and each of them covers a subset of our items, i.e., $S_i\subset U$.

Now binary variables $y_i$ are introduced to represent whether or not suppiler $S_i$ should be chosen, i.e.,

$$
y_i = 
\left\\{ 
\begin{array}{cl} 
  1, & \mathrm{choose\ supplier\ } S_i\\ 
  0, & \mathrm{otherwise} 
\end{array} 
\right.
$$

then the objective function can be formulated as

$$
  \min \sum_{i=0}^{M-1} y_i.
$$

To describe the constraints of fully filling the inventory, we need to inspect each item $U_i$ to ensure it is covered by some supplier, i.e.,

$$
  \sum_{i=0}^{M-1} c_{ji} \cdot y_i \geq 1,\ \   j=0,1,\cdots,N-1,
$$

with constant $c_{ji}$ defined by

$$
  c_{ji}=
  \left\\{
  \begin{array}{cc}
    1, & U_j \in S_i,\\
    0, & \mathrm{otherwise}.
  \end{array}
  \right.
$$

Then our "set cover" problem can be formulated as a Constrained Quadratic Models (CQM) as follows:

$$
\begin{align}
   & \min \sum_{i=0}^{M-1} y_i \\
   & s.t. \\
   &\ \ \ \ \ \ \ \ \sum_{i=0}^{M-1} c_{ji} \cdot y_i \geq 1,\ \   j=0,1,\cdots,N-1.
\end{align}
$$

## 2. Profit Optimization
Another typical logistic problem for a grocer is to maximize overall profit by selecting an optimal set of inventory. To build the model for this problem, assumptions should be given at the very beginning:
  1. there are $N$ different kinds of items $U=\\{ U_0, U_1,\cdots,U_{N-1} \\}$
  2. each of the item has its own price $V=\\{ V_0, V_1, \cdots, V_{N-1}\\}$
  3. each of the item has its own cost $W=\\{ W_0, W_1, \cdots, W_{N-1}\\}$
  4. there are also upper bounds for the quantity of each item $B=\\{ B_0, B_1, \cdots, B_{N-1}\\}$
  5. there is a budget limit $C$ for buying the items as well

By introducing discrete variables for $i=0,1,\cdots,N-1$,

$$
x_i\in\mathbb{N},\ s.t.\ 0\leq x_i\leq B_i,
$$

to denote the quantity of each item $U_i$, the CQM of the "Knapsack" problem can be written as

$$
\begin{align}
   & \min \sum_{i=0}^{N-1} (W_i-V_i) \cdot x_i \\
   & s.t. \\
   &\ \ \ \ \ \ \ \ \sum_{i=0}^{N-1} W_i \cdot x_i \geq C,\\
   &\ \ \ \ \ \ \ \ \ 0\leq x_i\leq B_i,\ \ i=0,\cdots,N-1.
\end{align}
$$

