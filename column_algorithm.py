from turton_cost import turton_cost

def distColumn_model(x, Problem):
    STAGE_EFFICIENCY = 0.5407

    # Independent Variables
    RR = x[0]  # * RR: Reflux Ratio (Not being used)
    P =  x[1]  # * P: Condenser Pressure
    NR = x[2]  # * NR: Number of active trays in rectifying section
    NS = x[3]  # * NS: Number of active trays in stripping  section
    FT = x[4]  # Feed
    VF = x[5]  # Vapor flow

    NT = (NR + NS) + 1  # Total number of active trays
    Feed_S = NR + 1  # Feed location

    # 01 Change Column Topology and Column specifications (degrees of freedom)
    HyObject = Problem.HyObject  # Recover Hysys Objects from structure Problem

    # Vapor flow
    HyObject.MaterialStream.Vapor.MolarFlow.SetValue(VF, 'kgmole/h')

    # Feed Temperature
    HyObject.MaterialStream.Feed.Temperature.SetValue(FT, 'C')

    # Total number of active trays
    HyObject.DistColumn.Main_TS.NumberOfTrays = NT

    # Feed location
    HyObject.DistColumn.Main_TS.SpecifyFeedLocation(HyObject.DistColumn.FeedMainTS, Feed_S)

    HyObject.HySolver.CanSolve = False  ## Pause the hysys solver to avoid generating error

    # Tower pressure
    DeltaP = (0.6895 * NT + 20)
    HyObject.MaterialStream.Bottoms.Pressure.SetValue(P + DeltaP, "kPa")
    HyObject.MaterialStream.Distillate.Pressure.SetValue(P, "kPa")

    # Specify Stage efficiency
    for i in HyObject.DistColumn.Main_TS.SeparationStages.Names:
        HyObject.DistColumn.Main_TS.SeparationStages.Item(i).OverallEfficiency.SetValue(STAGE_EFFICIENCY)

    HyObject.HySolver.CanSolve = True  ## Resume Solver

    # Reflux Ratio
    HyObject.DistColumn.Column.ColumnFlowsheet.Specifications.Item('Reflux Feed Ratio').GoalValue = (VF - 400) / 1000 + 0.7

    # 02 Run Aspen Hysys model with new topology
    # HyObject.DistColumn.ColumnFlowsheet.Reset()
    HyObject.DistColumn.ColumnFlowsheet.Run()  # Run Aspen Hysys model

    # 03 Check model convergence
    RunStatus = HyObject.HyApp.ActiveDocument.Flowsheet.Operations.Item(0).ColumnFlowsheet.CfsConverged

    if RunStatus == 1:
        # 04 Profit = Annual cost - revenue
        ColumnCost = turton_cost(Problem)
        Profit = ColumnCost.Profit

    else:  # In case model does not converge
        print("Column not converged")
        Profit = 1e5

    return Profit
