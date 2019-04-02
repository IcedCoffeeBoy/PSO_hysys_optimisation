import numpy as np
from pso_column import distCol_optimization
from column_algorithm import distColumn_model

# # 01 Hysys file name
hy_filename = 'PG_separation.hsc'

# # 02
hy_best_model_filename = 'Best_Solution_Test_Column.hsc'

# # 03 Bounds on the conditional trays
#      rr   CondP    NT    NS   Feed   Vapor-flow
lb = [0.7,  121.5,   2,    2,   130,     300]
ub = [0.7,  150.0,  30,   30,   150,     450]

# # 04 Integer variables index
IntVars = [2, 3]

# # 05 Aspen Hysys Graphical User Interface Visible
hy_visible = 1  # [1 ==> Visible    0 ==> No Visible]


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<< END


# # Problem Structure -----------------------------------------------------
class Problem:
    pass


Problem = Problem()
Problem.hy_filename = hy_filename
Problem.hy_best_model_filename = hy_best_model_filename
Problem.lb = lb
Problem.ub = ub
Problem.IntVars = IntVars
Problem.hy_visible = hy_visible

# # Run PSO ###############################################################
# Hyperparameter
swarm_size = 20

Result = distCol_optimization(Problem, swarm_size)  # from pso_column

print('Obj_fnc = ', Result.best_fitness)
print('x_best  = ', Result.x_best)
distColumn_model(Result.x_best, Problem)

# ---------------------------------------------------------------------- end


## Saving the data into a csv file
history = Result.history.reshape(6, swarm_size * 6)
history_val = Result.history_val
np.savetxt("history.csv", history, delimiter=";")
np.savetxt("history_val.csv", history_val, delimiter=";")
