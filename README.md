# DWave_supply_inventory
## Problem Description
As a grocer, we are facing 2 main problems: 
  1. minimizing the number of suppliers 
  2. maximizing the total profit

We will show how D-Wave Constrained Quadratic Models (CQM) Solver to helps us.

## 1. Supplier Optimization
As a typical logistic problem, a grocer needs to minimize the number of suppliers while fully filling the inventory. More specifically, we have the following assumptions:
  1. there are $N$ different kinds of items $U=\\{U_0,U_1,\cdots,U_{N-1}\\}$
  2. there are $M$ different suppliers $S=\\{S_0,S_1,\cdots,S_{M-1}\\}$, and each of them covers a subset of our items, i.e., $S_i\subset U$.

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

See [notebook](https://github.com/Weichen-Xie/DWave_supply_inventory/blob/main/CQM_supply.ipynb) for more details.

## 2. Profit Optimization
Another typical logistic problem for a grocer is to maximize overall profit by selecting an optimal set of inventory. To build the model for this problem, assumptions should be given at the very beginning:
  1. there are $N$ different kinds of items $U=\\{ U_0, U_1,\cdots,U_{N-1} \\}$
  2. each of the item has its own selling price $V=\\{ V_0, V_1, \cdots, V_{N-1}\\}$
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
   &\ \ \ \ \ \ \ \ \sum_{i=0}^{N-1} W_i \cdot x_i \leq C,\\
   &\ \ \ \ \ \ \ \ \ 0\leq x_i\leq B_i,\ \ i=0,\cdots,N-1.
\end{align}
$$

See [notebook](https://github.com/Weichen-Xie/DWave_supply_inventory/blob/main/CQM_inventory.ipynb) for more details.

## 3. Merging 2 problems
In a more realistic situation, a grocer needs to consider the above 2 problem simultaneously: maintaining the inventory from smallest number of suppliers while chasing the largest profit. This can be modelled by combining the "set cover" problem from supplier optimization and "knapsack" problem from profit optimization. As always, notations and assumptions are first given as follows:
  1. there are $N$ different kinds of items $U=\\{ U_0, U_1,\cdots,U_{N-1} \\}$
  2. each of the item has its own selling price $V=\\{ V_0, V_1, \cdots, V_{N-1}\\}$
  3. there are $M$ different suppliers $S=\\{ S_0, S_1, \cdots, S_{M-1}\\}$
  4. costs are different from suppliers $W_j=\\{ W_{j0}, W_{j1}, \cdots, W_{j(N-1)}\\}$ with $j=0,\cdots,M-1$
  5. there are also upper bounds for the quantity of each item $B=\\{ B_0, B_1, \cdots, B_{N-1}\\}$
  6. there is a budget limit $C$ for buying the items as well

As used in the supplier optimation problem, binary variables $y_j$ indicates if supplier $S_j$ is chosen or not. To maximize the net profit, discrete variables $x_{ji}$ denotes the quantity of buying item $U_i$ from supplier $S_j$. Then the combined CQM can be described as

$$
\begin{align}
   & \min A\cdot \sum_{i,j=0}^{N-1,M-1} (W_{ji}-V_i) \cdot x_{ji} \cdot y_j + B\cdot \sum_{j=0}^{M-1} y_j\\
   & s.t. \\
   &\ \ \ \ \ \ \ \ \sum_{i,j=0}^{N-1,M-1} (1-c_{ji})\cdot x_{ji} = 0\\
   &\ \ \ \ \ \ \ \ \sum_{i,j=0}^{N-1,M-1} W_{ji} \cdot x_{ji} \cdot y_{j} \leq C\\
   &\ \ \ \ \ \ \ \ 0\leq\sum_{j=0}^{M-1} x_{ji}\leq B_i,\ \ i=0,\cdots,N-1\\
   &\ \ \ \ \ \ \ \ \sum_{j=0}^{M-1} c_{ji} \cdot x_{ji} \cdot y_j \geq 1,\ \ i=0,\cdots,N-1
\end{align}
$$

where $A,B$ are Lagrange Multipliers.

See [notebook](https://github.com/Weichen-Xie/DWave_supply_inventory/blob/main/CQM_combine.ipynb) for more details.
