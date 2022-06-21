from dimod import CQM, Binary, quicksum
from dwave.system import LeapHybridCQMSampler
import random
import numpy as np

# Problem set up (specific exmaple)
# items
U = [0,2,3,4,9]
# suppliers
V = [{0,2,3,4,9}, {0,9,2}, {0,2,3,4}, {0,9,2,3}, {0,2,3,4,9}]

# Build CQM
cqm = CQM()

# Create Binary variables
bin_variables = [Binary(i) for i in range(len(U))]

# -------------- Objective Function ------------------
# minimize total number of suppliers
# Add obj to CQM
cqm.set_objective(quicksum(bin_variables[i] for i in range(len(U))))

# -------------- Constraints -----------------
# suppliers should cover all items
