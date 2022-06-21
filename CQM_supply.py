from dimod import CQM, Binary, quicksum
from dwave.system import LeapHybridCQMSampler
import numpy as np

# -------------- Problem set up --------------
# items (e.g. [0,2,3,4,9])
U = list(set(np.random.randint(10, size=(10))))
# suppliers (e.g. [{0,2,3,4,9}, {0,9,2}, {0,2,3,4}, {0,9,2,3}, {0,2,3,4,9}])
V = [set(U[i] for i in np.random.randint(len(U), size=(8))) for j in range(5)]

# Print set up
print('The universe is',U)
print('Number of elements in the universe: {:d}'.format(len(U)))

print('There are {:d} collections:'.format(len(V)))
for i in range(len(V)):
    print('Supplier{:d}:'.format(i), V[i])
print('Number of sets: N={:d}'.format(len(V)))

# Build CQM
cqm = CQM()

# Create Binary variables
bin_variables = [Binary(i) for i in range(len(V))]

# -------------- Objective Function ------------------
# minimize total number of suppliers
# Add obj to CQM
cqm.set_objective(quicksum(bin_variables[i] for i in range(len(V))))

# -------------- Constraints -----------------
# suppliers should cover all items
for a in range(len(U)):
    cqm.add_constraint( quicksum(int(U[a] in V[i])*bin_variables[i] for i in range(len(V))) >= 1,
                        label = 'cover item {:d}'.format(a) )

# -------------- Submit to CQM sampler ---------------
cqm_sampler = LeapHybridCQMSampler()
sampleset = cqm_sampler.sample_cqm(cqm, label = 'Supply Demo')

# -------------- Process the results ---------------
print('CQM Solution:')
#feasible_sols = np.where(sampleset.record.is_feasible == True)
feasible_sols = sampleset.filter(lambda row: row.is_feasible == True)
if not len(feasible_sols):
    print("\nNo feasible solution found.\n")
else:
    sol = [int(feasible_sols.first.sample[i]) for i in range(len(V))]
    print(sol)
    print('There are {:d} supplier selected.'.format(int(quicksum(sol))))
    suppliers = [f'suppiler{i}' for i in np.where(sol)[0]]
    print('Selected Suppliers:', suppliers)
