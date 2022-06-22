# DWave_supply_inventory
## Problem Description
As a grocer, we are facing 2 main problems: 
  1. minimizing the number of suppliers 
  2. maximizing the total profit

We will show how D-Wave Constrained Quadratic Models (CQM) Solver to helps us.

### 1. Supplier Optimization
As a typical logistic problem, a grocer needs to minimize the number of suppliers while fully filling the inventory. More specifically, assume that there are totally $N$ different kinds of items $U=\\{U_0,U_1,\cdots,U_{N-1}\\}$. There are $M$ different suppliers $V=\\{V_0,V_1,\cdots,V_{M-1}\\}$ as well, and each of them covers a subset of our items, i.e., $V_i\subset U$.

Now binary variables $y_i$ are introduced to represent whether or not suppiler $V_i$ should be chosen, i.e.,

$$
y_i = 
\left\\{ 
\begin{array}{cl} 
  1, & \mathrm{choose\ supplier\ } V_i\\ 
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
    1, & U_j \in V_i,\\
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
