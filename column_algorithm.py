# -*- coding: utf-8 -*-

from .Test_Column_ObjFnc import tac_column
import time

"""
% -------------------------------------------------------------------------
%   SIMULATION-BASED OPTIMIZATION OF A SINGLE CONVENTIONAL DISTILLATION 
%        COLUMN USING THE PARTICLE SWARM OPTIMIZATION ALGORITHM
%--------------------------------------------------------------------------
%                                      Juan Javaloyes Antón. Sep 2016 v.3
%--------------------------------------------------------------------------
% # 04 # Distillation column model
%--------------------------------------------------------------------------
"""


def distColumn_model(x, Problem):
    # Independent Variables
    RR = x[0]  # * RR: Reflux Ratio
    # BR = x[1]  # * BR: Boil up Ratio
    P = x[1]  # * P: Condenser Pressure

    NR = x[2]  # * NR: Number of active trays in rectifying section
    NS = x[3]  # * NS: Number of active trays in stripping  section
    FT = x[4]  # Feed Temperature

    HyObject = Problem.HyObject  # Recover Hysys Objects from structure Problem
    NT = (NR + NS) + 1  # Total number of active trays
    Feed_S = NR + 1  # Feed location

    # 01 Change Column Topology and Column specifications (degrees of freedom)
    HyObject = Problem.HyObject  # Recover Hysys Objects from structure Problem

    ##Tower pressure
    HyObject.HySolver.CanSolve = False  ## Pause the hysys solver to avoid generating error
    DeltaP = (0.6895 * NT + 20)
    HyObject.MaterialStream.Bottoms.Pressure.SetValue(P + DeltaP, "kPa")
    HyObject.MaterialStream.Distillate.Pressure.SetValue(P, "kPa")
    HyObject.HySolver.CanSolve = True  ## Resume Solver

    # Total number of active trays
    HyObject.DistColumn.Main_TS.NumberOfTrays = NT

    # Feed location
    HyObject.DistColumn.Main_TS.SpecifyFeedLocation(HyObject.DistColumn.FeedMainTS, Feed_S)

    # Reflux Ratio
    HyObject.DistColumn.Column.ColumnFlowsheet.Specifications.Item('Reflux Ratio').GoalValue = RR

    # Feed Temperature
    HyObject.MaterialStream.Feed.Temperature.SetValue(FT, 'C')

    # Boilup Ratio
    # HyObject.DistColumn.Column.ColumnFlowsheet.Specifications.Item('Boilup Ratio').GoalValue = BR
    ##-------------------------------------------------------------------------------------------------##

    # 02 Run Aspen Hysys model with new topology
    HyObject.DistColumn.ColumnFlowsheet.Run()  # Run Aspen Hysy model
    time.sleep(0.3)

    # 03 Check model convergence
    RunStatus = HyObject.HyApp.ActiveDocument.Flowsheet.Operations.Item(0).ColumnFlowsheet.CfsConverged

    if RunStatus == 1:

        # 04 Compute the Total Annual Cost of the Distillation Column
        ColumnCost = tac_column(Problem)  # from Test_Column_ObjFnc

        # 05 Check purity constraints
        PG_purity = 0.95
        Comp_frac_PG_Bott = HyObject.MaterialStream.Bottoms.ComponentMolarFractionValue[2]

        w1 = 0

        if Comp_frac_PG_Bott < PG_purity:
            w1 = (PG_purity - Comp_frac_PG_Bott) * 1e10

        # Total Annual Cost + penalty terms

        TAC = ColumnCost.TAC + w1
    else:  # In case model does not converge

        TAC = 1e5
    return (TAC)
