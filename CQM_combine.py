from dimod import CQM, Binary, Integer, quicksum
from dwave.system import LeapHybridCQMSampler
import numpy as np
import pandas as pd

# ---------- Problem set up -------------
np.random.seed(10)

print('------------- Problem set up -------------')
# inventory universe
U = list(set(np.random.randint(16, size=(10))))
# Average cost of items
W_avg = {U[i]: int(np.random.randint(9)+1) for i in range(len(U))}
# Price of items
V = [int(1.2*W_avg[U[i]]) for i in range(len(U))]
# Upper bound on number of items
upper_bound = list(np.random.randint(2, 8, size=(len(U))))
# Budget
Wbudget = 100
# Print set up
print('------------- Inventory -------------')
print('Budget:', Wbudget)
print('Number of elements in the universe: {:d}'.format(len(U)))
print('The inventory universe is', U)
print('The price of each item is', V)
print('Bound on item quantity is', upper_bound)
print('------------------------------------------')

# suppliers 
S = [set(U[i] for i in np.random.randint(len(U), size=(6))) for j in range(5)]
# Costs from each supplier
W = list(S)
for i in range(len(S)):
    W[i] = list(S[i])
    for j in range(len(W[i])):
        W[i][j] = int(np.random.randint(75,125,1)*W_avg[list(S[i])[j]]/100) + 1
# Print set up
print('------------- Suppliers -------------')
print('There are {:d} suppliers:'.format(len(S)))
print('----------------------------')
for i in range(len(S)):
    print('Supplier{:d}'.format(i), S[i])
    print('Costs: ', W[i])
    print('----------------------------')
print('------------------------------------------')


# ---------- Build QCM ------------
cqm = CQM()

# Create discrete variables
# Quantity of each item from each supplier
x = [[Integer((j,i), upper_bound=upper_bound[i]) for i in range(len(U))] for j in range(len(S))]
# Create binary variables
# Indicator for choosing each supplier
y = [[Binary((j,len(U)+1))] for j in range(len(S))]

# -------------- Objective Function ------------------
# maximize total profit
obj1 = -quicksum(V[i]*x[j][i]*int(U[i] in S[j])*y[j][0] for i in range(len(U)) for j in range(len(S)) )
# minimize total cost
obj2 = quicksum(W[j][i]*x[j][ U.index(list(S[j])[i]) ]*y[j][0] for j in range(len(S)) for i in range(len(W[j])) )
# minimize number of 

# Add obj to CQM
cqm.set_objective(obj1+obj2)

# -------------- Constraints -----------------
# suppliers should cover all items
for i in range(len(U)):
    cqm.add_constraint( quicksum( int(U[i] in S[j])*x[j][i]*y[j][0] for j in range(len(S))) >= 1,
                        label = 'cover item {:d}'.format(i) )
# cannot buy without supply
for i in range(len(U)):
    for j in range(len(S)):
        if U[i] not in S[j]:
            cqm.add_constraint( x[j][i] == 0, 
                                label = 'supplier{:d} sells no item{:d}'.format(j, U[i]) )
# no exceeding total budget
cqm.add_constraint( quicksum(W[j][i]*x[j][ U.index(list(S[j])[i]) ]*y[j][0] for j in range(len(S)) for i in range(len(W[j])) ) <= Wbudget,
                    label = 'budget' )
# no exceeding upper bound
for i in range(len(U)):
    cqm.add_constraint( quicksum(x[j][i] for j in range(len(S))) <= upper_bound[i], 
                        label = 'bound item {:d}'.format(i) )
# minimize number of suppliers
cqm.add_constraint( quicksum( y[j][0] for j in range(len(S))) <= 3,
                    label = 'mini supplier' )

# -------------- Submit to CQM sampler ---------------
cqm_sampler = LeapHybridCQMSampler()
sampleset = cqm_sampler.sample_cqm(cqm, label = 'Combine Demo')

# -------------- Process the results ---------------
print('------------- Solution -------------')
feasible_sols = sampleset.filter(lambda row: row.is_feasible == True)
if not len(feasible_sols):
    print("\nNo feasible solution found.\n")
else:
    sol = feasible_sols.first.sample
    choosing_plan = [int(sol[(j,len(U)+1)]) for j in range(len(S))]
    purchase_plan = [int(sol[(j,i)])*choosing_plan[j] for i in range(len(U)) for j in range(len(S))]
    purchase_plan = np.array(purchase_plan).reshape( len(U), len(S) )

    df = pd.DataFrame( purchase_plan, index=pd.Index(U, name='Item'),
                       columns=pd.Index(list(range(len(S))), name='Supplier'))
    print('Choosing', choosing_plan)
    print(df)
    cost = quicksum(W[j][i]*purchase_plan[ U.index(list(S[j])[i]) ][j] for j in range(len(S)) for i in range(len(W[j])) )
    profit = quicksum( purchase_plan[i][j]*V[i] for i in range(len(U)) for j in range(len(S)) )
    print('Profit: ', profit)
    print('Cost: ', cost)
    print('Net Profit: ', profit-cost)