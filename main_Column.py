from ConventionalDistillationColumn.pso_column import distCol_optimization
from ConventionalDistillationColumn.column_algorithm import distColumn_model

# # 01 Hysys file name
hy_filename = 'PG_separation.hsc'

# # 02
hy_best_model_filename = 'Best_Solution_Test_Column.hsc'

# # 03 Bounds on the conditional trays
#      CR    CondP   NR    NS    ND  Feed_Temp
lb = [0.98, 121.0,   5,    5,    5,   111.2]
ub = [1.00, 130.0,  30,   30,   30,   140.0]

# # 04 Integer variables index
IntVars = [2, 3, 4]

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
