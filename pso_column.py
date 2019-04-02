# -*- coding: utf-8 -*-
import time

from hyInterface import hy_Dist_Col_Object
from PSO_Algorithm import pso_gbest
from column_algorithm import distColumn_model

def distCol_optimization(Problem, swarm_size):
    # 01 Interface between Aspen Hysys and Matlab
    HyObject = hy_Dist_Col_Object(Problem)  # from hiInterface

    Problem.HyObject = HyObject

    # 02 Run Optimization model
    lb = Problem.lb
    ub = Problem.ub
    IntVars = Problem.IntVars

    t_start = time.time()

    Result = pso_gbest(distColumn_model, lb, ub, IntVars,swarm_size, Problem)  # #### PSO ####

    t_stop = time.time() - t_start

    # 03 Print Results
    Result.etime = t_stop

    # printResult_cdc(Result, Problem)
    return (Result)
