# DWave_supply_inventory
## Problem Description
As a grocer, we are facing 2 main problems: 
  1. minimizing the number of suppliers 
  2. maximizing the total profit

We will show how D-Wave Constrained Quadratic Models (CQM) Solver to helps us.

### 1. Supplier Optimization
As a typical logistic problem, a grocer needs to minimize the number of suppliers while filling the inventory. More specifically, assume that there are totally $N$ different kinds of items $U=\\{U_0,U_1,\cdots,U_{N-1}\\}$. There are also $M$ different suppliers $V=\\{V_0,V_1,\cdots,V_{M-1}\\}$ and each of them covers a subset of our items, i.e., $V_i\subset U$. In brief, this is done by modelling the problem as a "set cover" problem:
