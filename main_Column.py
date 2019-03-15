from ConventionalDistillationColumn.pso_column import distCol_optimization
from ConventionalDistillationColumn.column_algorithm import distColumn_model

# # 01 Hysys file name
hy_filename = 'PG_separation.hsc'

# # 02
hy_best_model_filename = 'Best_Solution_Test_Column.hsc'

# # 03 Bounds on the conditional trays
#      RR   CondP   NR    NS   Feed  Vapor-flow
lb = [0.75, 121.1,   5,    5,   140,  350]
ub = [1.0,  150.0,  30,   30,   150,  450]

# # 04 Integer variables index
IntVars = [2, 3]

# # 05 Aspen Hysys Graphical User Interface Visible
hy_visible = 1  # [1 ==> Visible    0 ==> No Visible]


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<< END


# # Problem Structure -----------------------------------------------------
class Problem:
    pass


Problem.hy_filename = hy_filename
Problem.hy_best_model_filename = hy_best_model_filename
Problem.lb = lb
Problem.ub = ub
Problem.IntVars = IntVars
Problem.hy_visible = hy_visible

# # Run PSO ###############################################################
Result = distCol_optimization(Problem)  # from pso_column

print('Obj_fnc = ', Result.best_fitness)
print('x_best  = ', Result.x_best)
distColumn_model(Result.x_best, Problem)
# ---------------------------------------------------------------------- end
