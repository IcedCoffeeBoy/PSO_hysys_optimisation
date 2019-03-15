from ConventionalDistillationColumn.hyInterface import hy_Dist_Col_Object

class Problem:
    hy_filename = "PG_separation_Best.hsc"
    hy_best_model_filename = "Best_column.hsc"
    hy_visible = 1
    pass


HyObject = hy_Dist_Col_Object(Problem)
# HyObject.DistColumn.Main_TS.TopStagePressure.SetValue(1.2,"atm")
# print(HyObject.DistColumn.Main_TS.TopStagePressure)
# HyObject.MaterialStream.Distillate.Pressure.SetValue(1.5,"atm")
# print(HyObject.MaterialStream.Distillate.ComponentMolarFractionValue)
# print(HyObject.DistColumn.FeedMainTS.Temperature)
# print(HyObject.MaterialStream.Feed.Temperature.SetValue(100,'C'))
# HyObject.DistColumn.FeedMainTS.Temperature =100
# print(HyObject.DistColumn.ColumnFlowsheet.LiquidProducts.Item('Side Draw'))
print( HyObject.MaterialStream.Vapor)





