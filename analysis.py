from hyInterface import hy_Dist_Col_Object
from column_algorithm import distColumn_model
import numpy as np
import matplotlib.pyplot as plt

class Problem:
    hy_filename = "PG_separation.hsc"
    hy_best_model_filename = "Best_column.hsc"
    hy_visible = 1
    pass

# To access HYSYS to collect cost
def cost_evaluate_func(x,var,Problem):
    x_default = [0.7, 121.5,  7,   10,   146.9,   422]
    x_default[var[0]] = x[0]
    x_default[var[1]] = x[1]
    TAC= distColumn_model(x_default,Problem)
    return TAC

if __name__=="__main__":
    HyObject = hy_Dist_Col_Object(Problem)
    Problem.HyObject = HyObject

    # Gathering data for contour plot
    X = np.linspace(5,30,26)
    Y = np.linspace(400,450,51)
    x,y = np.meshgrid(X,Y)
    z = np.zeros(x.shape)

    count = 0

    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            z[i,j] = cost_evaluate_func([x[i,j],y[i,j]],[3,5],Problem)

    np.savetxt("z.csv", z, delimiter=";")

    plt.figure()
    cp = plt.contour(x, y, z)
    plt.clabel(cp, inline=True,fontsize=10)
    plt.xlabel('Total number of stages')
    plt.ylabel('Vaporised Feed kmol/h')
    plt.show()