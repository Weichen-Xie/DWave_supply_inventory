from dimod import CQM, Binary, Integer, quicksum
from dwave.system import LeapHybridCQMSampler
import numpy as np

# ---------- Problem set up -------------
num_of_items = 12
# values of every item (e.g. [8, 7, 1, 8, 5, 9, 8, 7, 1, 4, 1, 3])
values = list(np.random.randint(1,10, size=(num_of_items)))
# costs of every item (e.g. [2, 4, 8, 8, 4, 2, 5, 2, 4, 9, 7, 2])
weights = list(np.random.randint(1,10, size=(num_of_items)))
# total cost upper bound (e.g. 23)
weight_capacity = np.random.randint(12, 40)
# upper bounds of selling every item (e.g. [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
variable_bounds = list(np.random.randint(2, 6,size=(num_of_items)))
print('------------- Problem set up -------------')
print('values:',values)
print('weights:',weights)
print('weight_capacity:',weight_capacity)
print('variable bounds:',variable_bounds)

# ---------- Build QCM ------------
cqm = CQM()

# Create discrete variables
x = [Integer(i, upper_bound=variable_bounds[i]) for i in range(num_of_items)]

# -------------- Objective Function ------------------
# maximize total profit
# Add obj to CQM
cqm.set_objective(-quicksum(values[i]*x[i] for i in range(num_of_items)))

# -------------- Constraints -----------------
# no exceeding total weight
cqm.add_constraint( quicksum(weights[i]*x[i] for i in range(num_of_items))<=weight_capacity,
                    label = 'weight capacity' )

# -------------- Submit to CQM sampler ---------------
cqm_sampler = LeapHybridCQMSampler()
sampleset = cqm_sampler.sample_cqm(cqm, label = 'Inventory Demo')

# -------------- Process the results ---------------
print('------------- Solution -------------')
feasible_sols = sampleset.filter(lambda row: row.is_feasible == True)
if not len(feasible_sols):
    print("\nNo feasible solution found.\n")
else:
    sol = [int(feasible_sols.first.sample[i]) for i in range(num_of_items)]
    print('best solution: ', sol)
    print('Total weight: ', quicksum(weights[i]*sol[i] for i in range(num_of_items)))
    print('Total value: ', quicksum(values[i]*sol[i] for i in range(num_of_items)))
