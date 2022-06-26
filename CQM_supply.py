from dimod import CQM, Binary, quicksum
from dwave.system import LeapHybridCQMSampler
import numpy as np

# -------------- Problem set up --------------
# items (e.g. [0,2,3,4,9])
U = list(set(np.random.randint(10, size=(10))))
# suppliers (e.g. [{0,2,3,4,9}, {0,9,2}, {0,2,3,4}, {0,9,2,3}, {0,2,3,4,9}])
S = [set(U[i] for i in np.random.randint(len(U), size=(8))) for j in range(5)]

# Print set up
print('------------- Problem set up -------------')
print('The universe is',U)
print('Number of elements in the universe: {:d}'.format(len(U)))

print('There are {:d} collections:'.format(len(S)))
for j in range(len(S)):
    print('Supplier{:d}:'.format(j), S[j])
print('Number of sets: N={:d}'.format(len(S)))

# Build CQM
cqm = CQM()

# Create Binary variables
y = [Binary(j) for j in range(len(S))]

# -------------- Objective Function ------------------
# minimize total number of suppliers
# Add obj to CQM
cqm.set_objective(quicksum(y[j] for j in range(len(S))))

# -------------- Constraints -----------------
# suppliers should cover all items
for i in range(len(U)):
    cqm.add_constraint( quicksum(int(U[i] in S[j])*y[j] for j in range(len(S))) >= 1,
                        label = 'cover item {:d}'.format(i) )

# -------------- Submit to CQM sampler ---------------
cqm_sampler = LeapHybridCQMSampler()
sampleset = cqm_sampler.sample_cqm(cqm, label = 'Supply Demo')

# -------------- Process the results ---------------
print('------------- Solution -------------')
feasible_sols = sampleset.filter(lambda row: row.is_feasible == True)
if not len(feasible_sols):
    print("\nNo feasible solution found.\n")
else:
    sol = [int(feasible_sols.first.sample[i]) for i in range(len(S))]
    print(sol)
    print('There are {:d} supplier selected.'.format(int(quicksum(sol))))
    suppliers = [f'suppiler{i}' for i in np.where(sol)[0]]
    print('Selected Suppliers:', suppliers)
