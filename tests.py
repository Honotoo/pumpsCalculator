import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import ast
from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes
import math

from mpl_toolkits.axisartist.parasite_axes import HostAxes
import matplotlib.pyplot as plt


def plotThis(PlotDict, xAxisName, commonEnv = True):
    fig = plt.figure(figsize = [12, 6])

    host = fig.add_axes([0.15, 0.1, 0.65, 0.8], axes_class=HostAxes)
    host.axis["right"].set_visible(False)
    host.axis["left"].set_visible(False)

    d = {}
    maxX = 0
    minX = 0
    maxY = 0
    minY = 0
    for k,XY in PlotDict.items():
        X,Y = XY[0],XY[1]
        par1 = ParasiteAxes(host)#, sharex=host)
        p1, = par1.plot(X, Y, label=str(k))
        d[par1] = p1
        maxX = max(max(X),maxX)
        minX = min(min(X), minX)
        maxY = max(max(Y), maxY)
        minY = min(min(Y), minY)

    maxX = int(maxX/100*110)
    minX = int(minX/100*110)
    maxY = int(maxY/100*110)
    minY = int(minY/100*110)

    indexer = 0
    for AP, kXY in zip(d.items(), PlotDict.items()):
        Axeses, Plots = AP[0], AP[1]
        k, X, Y = kXY[0], kXY[1][0], kXY[1][1]
        host.parasites.append(Axeses)
        Axeses.axis["right"].set_visible(False)

        if indexer == 0:
            Axeses.axis["left"] = Axeses.new_fixed_axis(loc="left", offset=(0, 0))
            Axeses.axis["left"].label.set_color(Plots.get_color())
            if commonEnv:
                Axeses.set(ylim=(minY, maxY),xlim=(minX,maxX), ylabel=k)
            else:
                Axeses.set( ylabel=k)
            Axeses.grid(True)
        else:
            Axeses.axis["right"] = Axeses.new_fixed_axis(loc="right", offset=((indexer-1)*40, 0))
            if commonEnv:
                Axeses.set(ylim=(minY, maxY),xlim=(minX,maxX), ylabel=k)
            else:
                Axeses.set( ylabel=k)
            Axeses.axis["right"].label.set_color(Plots.get_color())

        host.set(xlabel=xAxisName)
        # par1.set(ylim=(0, 4), ylabel="Temperature")


        indexer+=1


    host.legend()
    # host.grid(True)

    plt.show()


PlotDict = {'lift_H_m': [[0.0, 11.77, 23.54, 35.31, 47.07, 58.84, 70.61, 82.38, 94.15, 96.04, 105.92, 117.69, 129.45, 141.22, 152.99, 164.76], [22.96, 22.92, 22.93, 22.92, 22.8, 22.51, 22.02, 21.28, 20.27, 20.08, 18.98, 17.4, 15.55, 13.45, 11.14, 8.65]], 'Cavitation_NPSH_m': [[0.0, 11.77, 23.54, 35.31, 47.07, 58.84, 70.61, 82.38, 94.15, 96.04, 105.92, 117.69, 129.45, 141.22, 152.99, 164.76], [1.14, 1.17, 1.2, 1.24, 1.29, 1.37, 1.46, 1.59, 1.76, 1.79, 1.98, 2.26, 2.61, 3.05, 3.58, 4.23]], 'motor_power_P2_kW': [[0.0, 11.77, 23.54, 35.31, 47.07, 58.84, 70.61, 82.38, 94.15, 96.04, 105.92, 117.69, 129.45, 141.22, 152.99, 164.76], [3.57, 3.84, 4.21, 4.67, 5.17, 5.68, 6.2, 6.7, 7.17, 7.24, 7.6, 7.99, 8.35, 8.67, 8.98, 9.28]], 'efficiency': [[0.0, 11.77, 23.54, 35.31, 47.07, 58.84, 70.61, 82.38, 94.15, 96.04, 105.92, 117.69, 129.45, 141.22, 152.99, 164.76], [0.0, 4.0, 8.0, 12.0, 16.0, 20.0, 24.0, 28.0, 32.0, 36.0, 40.0, 44.0, 48.0, 52.0, 56.0, 60.0]]}

plotThis(PlotDict, "flow_rate_Q_m3_h_for_lift")
