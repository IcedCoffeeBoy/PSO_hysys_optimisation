from ConventionalDistillationColumn.hyInterface import hy_Dist_Col_Object

class Problem:
    hy_filename = "Test_Column.hsc"
    hy_best_model_filename = "Best_column.hsc"
    hy_visible = 1
    pass


HyObject = hy_Dist_Col_Object(Problem)
# HyObject.DistColumn.Main_TS.TopStagePressure.SetValue(1.2,"atm")
print(HyObject.DistColumn.Main_TS.TopStagePressure)
# HyObject.MaterialStream.Distillate.Pressure.SetValue(1.5,"atm")
HyObject.HySolver.CanSolve = False

