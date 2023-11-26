# есть варианты открыть калькулятор для
# вариант модели - линейные и сглаженная
# вывести вообще всё
import numpy as np
from sklearn import linear_model
import ast

import matplotlib.pyplot as plt
# %matplotlib inline
from scipy.optimize import fsolve
import ast
from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes
#from shortFunctions import *
import math

from scipy import optimize




def plotThis(PlotDict, commonEnv = True):
    # две не solid штуки, которые мы тащим со словоря
    # они по идее должны идти отдельно, но поскольку мы в программе шлем словари, а не картинки
    # для скорости.имя оси и точка пересечения упакованы в словарь

    xAxisName = "Ось X"
    try:
        xAxisName = PlotDict['xAxisName']
        PlotDict.pop('xAxisName')
    except:
        pass
    points = None
    try:
        points = PlotDict['points']
        PlotDict.pop('points')
    except:
        pass

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
        # par1 = ParasiteAxes(host, sharex=host)
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

    host.set_xlim(minX, maxX)
    host.set_ylim(minY, maxY)

    indexer = 0
    for AP, kXY in zip(d.items(), PlotDict.items()):
        Axeses, Plots = AP[0], AP[1]
        k, X, Y = kXY[0], kXY[1][0], kXY[1][1]
        # print(X)
        # print(Plots.label)
        host.parasites.append(Axeses)
        Axeses.axis["right"].set_visible(False)
        # Axeses.axis["right"].major_ticklabels.set_visible(True)
        # Axeses.axis["right"].label.set_visible(True)

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
    if points !=None:
        for point in points:

            print("point")
            print(point)
            if point[1] == 0:
                host.plot([point[0], point[0]], [0, maxY], "k--")
                host.text(point[0] + 2, 0.5, fr"{point[2]} {point[0]:.2f}", color="k", fontsize=10)

            elif point[0] == 0:
                host.plot([0, maxX], [point[1], point[1]], "k--")
                host.text(2, point[1] - 3, fr"{point[3]} {point[1]:.2f}", color="k", fontsize=10)
            else:
                host.plot([0, point[0]], [point[1], point[1]], "k--")
                host.text(2, point[1] - 3, fr"{point[3]} {point[1]:.2f}", color="k", fontsize=10)

                host.plot([point[0], point[0]], [0, point[1]], "k--")
                host.text(point[0] + 2, 0.5, fr"{point[2]} {point[0]:.2f}", color="k", fontsize=10)

                host.plot([point[0]], [point[1]], 'o', markersize=5, color="k")
                #host.plot(point[0], calculatedPoints, label="calculated")

    host.legend()
    host.grid(True)
    host.margins(x=0.01)
    # plt.show()
    return plt.gcf()  # .savefig('im.png', bbox_inches='tight')

# PlotDict = {"points":[(96.02 , 35.98, r'Q (m$^3$/s)', 'h (m)')],'lift_H_m': [[0.0, 11.77, 23.54, 35.31, 47.07, 58.84, 70.61, 82.38, 94.15, 96.04, 105.92, 117.69, 129.45, 141.22, 152.99, 164.76], [22.96, 22.92, 22.93, 22.92, 22.8, 22.51, 22.02, 21.28, 20.27, 20.08, 18.98, 17.4, 15.55, 13.45, 11.14, 8.65]], 'Cavitation_NPSH_m': [[0.0, 11.77, 23.54, 35.31, 47.07, 58.84, 70.61, 82.38, 94.15, 96.04, 105.92, 117.69, 129.45, 141.22, 152.99, 164.76], [1.14, 1.17, 1.2, 1.24, 1.29, 1.37, 1.46, 1.59, 1.76, 1.79, 1.98, 2.26, 2.61, 3.05, 3.58, 4.23]], 'motor_power_P2_kW': [[0.0, 11.77, 23.54, 35.31, 47.07, 58.84, 70.61, 82.38, 94.15, 96.04, 105.92, 117.69, 129.45, 141.22, 152.99, 164.76], [3.57, 3.84, 4.21, 4.67, 5.17, 5.68, 6.2, 6.7, 7.17, 7.24, 7.6, 7.99, 8.35, 8.67, 8.98, 9.28]], 'efficiency': [[0.0, 11.77, 23.54, 35.31, 47.07, 58.84, 70.61, 82.38, 94.15, 96.04, 105.92, 117.69, 129.45, 141.22, 152.99, 164.76], [0.0, 4.0, 8.0, 12.0, 16.0, 20.0, 24.0, 28.0, 32.0, 36.0, 40.0, 44.0, 48.0, 52.0, 56.0, 60.0]]}
# plotThis(PlotDict)

class linModel:
    a = None
    b = None
    def linear_fit(self, x, a, b):
        return a * x + b
    def fit(self, XsofLine, YsofLine):
        self.a, self.b = optimize.curve_fit(self.linear_fit, XsofLine, YsofLine)[0]
    def predict(self, x):
        return self.linear_fit(x, self.a, self.b)
    def __str__(self):
        return "a: "+str(self.a)+" b: "+str(self.b)
    def __init__(self):
        pass


class calcManager:
    CalcValues = None
    dbList = None
    OkDBList = []
    modelType = "poly1d"#linear
    ShowAll = False
    model = None

    def plotThis(self, PlotDict):
        plotThis(PlotDict, commonEnv=True)

    def Lines_intersects(self, s0, s1):
        dx0 = s0[1][0] - s0[0][0]
        dx1 = s1[1][0] - s1[0][0]
        dy0 = s0[1][1] - s0[0][1]
        dy1 = s1[1][1] - s1[0][1]
        p0 = dy1 * (s1[1][0] - s0[0][0]) - dx1 * (s1[1][1] - s0[0][1])
        p1 = dy1 * (s1[1][0] - s0[1][0]) - dx1 * (s1[1][1] - s0[1][1])
        p2 = dy0 * (s0[1][0] - s1[0][0]) - dx0 * (s0[1][1] - s1[0][1])
        p3 = dy0 * (s0[1][0] - s1[1][0]) - dx0 * (s0[1][1] - s1[1][1])
        return (p0 * p1 <= 0) & (p2 * p3 <= 0)
    # print(Lines_intersects([(2,1),(9,5)],[(5,1),(3,5)]))
    # print(Lines_intersects([(2,1),(9,5)],[(10,0),(6,2)]))

    def complex_intersection(self, Y1, X1, Y2, X2):
        # X1 = X1[::-1], Y1=Y1[::-1], X2=X2[::-1], Y2=Y2[::-1],
        for each1 in range(len(X1) - 1):
            line1 = [(X1[each1], Y1[each1]), (X1[each1 + 1], Y1[each1 + 1])]
            for each2 in range(len(X2) - 1):
                line2 = [(X2[each2], Y2[each2]), (X2[each2 + 1], Y2[each2 + 1])]
                if self.Lines_intersects(line1, line2) == True:
                    # print("complex_intersection: "+str(line1) + str(line2))
                    return (line1, line2)
                    # return str(line1)+str(line2)
        return None

    # def give_Y_of_line_at_this_X(self, Line_X1, Line_Y1, this_X):
    #
    #     dots = self.complex_intersection([this_X,this_X], [0,1000], Line_X1, Line_Y1)
    #     # modeled = np.poly1d(np.polyfit(Line_X1, Line_Y1, 6))
    #     self.model = linModel()
    #     self.model.fit(Line_Y1, Line_X1)
    #
    #     X_collision = fsolve(lambda k: this_X - self.model.predict(k), 42)[0]
    #     # # просто вставвляем найденный икс в функцию и получаем Y по стандартной матеше
    #     # Y_collision = Formula(Q, H, X_collision)
    #     # self.model
    #     # return modeled(this_X)
    #     print(X_collision)

    def give_Y_of_line_at_this_X(self, Line_X1, Line_Y1, this_X):
        X_collision = 0
        try:
            dots = self.complex_intersection([0, 1000],[this_X, this_X], Line_Y1,  Line_X1)
            XsofLine = np.array([dots[1][0][0], dots[1][1][0]])
            YsofLine = np.array([dots[1][0][1], dots[1][1][1]])
            self.model = linModel()
            self.model.fit(YsofLine, XsofLine)
            X_collision = fsolve(lambda k: this_X - self.model.predict(k), 42)[0]
        except:
            pass
        return X_collision

    def calculator(self, ExistingLineX, ExistingLineY, Q, H, percents, modelType = "linear", checkInterceptBool = False):

        # формула непосредственно для расчета кривой новой
        def Formula(Q, H, EfficiancyValue):
            return (EfficiancyValue /Q) ** 2 *H
        # для новой кривой немного сдвигается значение X по вот этой логике
        def FormulaX (Q, percent_):
            return percent_/100*Q
        # делаем  Y для точек в новой кривой
        def calculate_Hvx_Line_Y(Q, H, Y):
            calculatedPoints = []
            for each in Y:
                calculatedPoints.append(Formula(Q, H, each))
            return calculatedPoints
        # делаем  X для точек в новой кривой
        def calculate_Hvx_Line_X(Q, un_destorted_list):
            to_return=[]
            for percent_ in un_destorted_list:
                to_return.append(FormulaX (Q, percent_))
            return to_return

        # график по расчету
        calculatedPoints_X = calculate_Hvx_Line_X(Q, range(1,percents+1))
        calculatedPoints_Y = np.array(calculate_Hvx_Line_Y(Q, H, calculatedPoints_X))

        # по сути, если нам нужно только проверить факт пересечения, то дальше мы можем не считать.
        if checkInterceptBool == True:
            dots = self.complex_intersection(calculatedPoints_X, calculatedPoints_Y, ExistingLineX, ExistingLineY)
            if dots == None:
                return False
            else:
                return True


        #Строим модель полиномиальной/ линейной регрессии имеющейся линии
        self.model = None
        if modelType == "poly1d":
            self.model = np.poly1d (np.polyfit (ExistingLineX, ExistingLineY , 6))
        if modelType == "linear":
            dots = self.complex_intersection(calculatedPoints_X, calculatedPoints_Y, ExistingLineX, ExistingLineY)
            XsofLine = np.array([dots[1][0][0],dots[1][1][0]])
            YsofLine = np.array([dots[1][0][1],dots[1][1][1]])
            self.model = linModel()
            self.model.fit( YsofLine,XsofLine)
            # print(model)

        # Ищем x точки соприкосновения двух моделей
        X_collision = 0
        Y_collision = 0
        # сделаем ещё график для модели, описывающей имеющиеся данные
        X_plotModel = []
        Y_plotModel = []

        #
        # modeled = np.poly1d(np.polyfit(Line_X1, Line_Y1, 6))
        # # self.model
        # return modeled(this_X)
        #


        #подбор значения при котором разница X между нашей моделью по данным и функцией расчетов будет минимальной
        if modelType == "poly1d":
            X_collision = fsolve(lambda k: Formula(Q, H, k) - self.model(k), 42)[0]
            # просто вставвляем найденный икс в функцию и получаем Y по стандартной матеше
            Y_collision = Formula(Q, H, X_collision)

            # for each in range(int(Y_collision) - int(percents / 2)+offset, int(Y_collision) + int(percents / 2)+offset):
            # for each in range(0, int(max(ExistingLineX))):
            for each in range(0, int(max(ExistingLineX))):
                X_plotModel.append(each)
                Y_plotModel.append(self.model(each))

        if modelType == "linear":
            X_collision = fsolve(lambda k: Formula(Q, H, k) - self.model.predict(k), 42)[0]
            # просто вставвляем найденный икс в функцию и получаем Y по стандартной матеше
            Y_collision = Formula(Q, H, X_collision)

            for each in range(0, int(max(ExistingLineX))):
                X_plotModel.append(each)
                Y_plotModel.append(self.model.predict(each))


        return  calculatedPoints_X, calculatedPoints_Y, X_collision, Y_collision,X_plotModel, Y_plotModel

    def iterating_matcher(self, showCalculatedModel = False):#, modelType = "linear"  "poly1d"#linear

        ourX = "flow_rate_Q_m3_h"
        ourY = "lift_H_m"

        def GiveCalcData():
            Q = int(self.CalcValues["Flow"])
            H = int(self.CalcValues["pressure"])
            percents = int(self.CalcValues["percents"])
            modelType = self.modelType
            return Q, H, percents, modelType

        def isThisPumpOK(pump):
            speed = 1
            # thisPumpOk = False
            for pumpSpeedLine in ast.literal_eval(pump[ourY]):
                # print(pumpSpeedLine)
                ExistingLineX = pumpSpeedLine[0]
                ExistingLineY = pumpSpeedLine[1]
                Q, H, percents, modelType = GiveCalcData()
                # если пересечения нет, то ничего не делаем. Функция вернет false (небольшая надстройка, но мне так удобнее вышло)
                if False == self.calculator( ExistingLineX, ExistingLineY, Q, H, percents, modelType, checkInterceptBool = True):
                    speed+=1
                    continue
                else:
                    return  True, speed
            return False, 0

        def putThisPumpinOkDBList(pump,speed):
            Q, H, percents, modelType = GiveCalcData()
            currentSpeed = 1
            THisPump_X_collision, THisPump_Y_collision = None,None
            PlotDict = {}

            for pumpSpeedLine in ast.literal_eval(pump[ourY]):
                ExistingLineX = pumpSpeedLine[0]
                ExistingLineY = pumpSpeedLine[1]
                calculatedPoints_X, calculatedPoints_Y, X_collision, Y_collision, X_plotModel, Y_plotModel = self.calculator( ExistingLineX, ExistingLineY, Q, H, percents, modelType)
                if currentSpeed == speed:
                    # если нужно напечатать матмодель по данным
                    if showCalculatedModel == True:
                        PlotDict["approximated"] = [X_plotModel, Y_plotModel]
                    THisPump_X_collision, THisPump_Y_collision = X_collision, Y_collision
                    point = (X_collision, Y_collision, r'Q (m$^3$/s)', 'h (m)')
                    PlotDict['points'] = [point]
                    PlotDict['xAxisName'] = ourX
                    PlotDict["Рассчитанная модель"] = [calculatedPoints_X, list(calculatedPoints_Y)]
                PlotDict["Скорость " + str(currentSpeed)] = [ExistingLineX, ExistingLineY]
                currentSpeed+=1
            PlotDict['КПД'] = ast.literal_eval(pump['efficiency'])[0]
            pump["PlotDict1"] = PlotDict


            linesPlot2 = ['motor_power_P2_kW', 'Cavitation_NPSH_m']
            PlotDict = {}
            for lineName in linesPlot2:
                PlotDict[lineName] = ast.literal_eval(pump[lineName])[0]
                # PlotDict["newModel"] = [calculatedPoints_X, calculatedPoints_Y]

                # если нужно напечатать матмодель по данным
                # PlotDict["approximated"] = [X_plotModel, Y_plotModel]


                # print("PlotDict[lineName]")
                # print(PlotDict[lineName])
                point = (THisPump_X_collision, 0, r'Q (m$^3$/s)', ' ')
                PlotDict['points'] = [point]
                PlotDict['xAxisName'] = "Ось Х"
                # plotThis(PlotDict)
            pump["PlotDict2"] = PlotDict
            # print(PlotDict)


            # сбор данных для предварительного отчета и для вывода в Заданных параметрах
            IntersectionData = {}
            proizvNapor = pump["PlotDict1"]["points"]
            IntersectionData["Модель"] = pump["Model_Name"]
            IntersectionData["Производительность"] = f"{proizvNapor[0][0]:.2f} " + " м3/ч"
            IntersectionData["Напор"] = f"{proizvNapor[0][1]:.2f} " + " (m)"

            motor_power_P2_kW = self.give_Y_of_line_at_this_X(ast.literal_eval(pump["motor_power_P2_kW"])[0][0],
                                        ast.literal_eval(pump["motor_power_P2_kW"])[0][1], PlotDict['points'][0][0])
            IntersectionData["Мощность на валу"] = f"{motor_power_P2_kW:.2f} "#  motor_power_P2_kW

            efficiency = self.give_Y_of_line_at_this_X(ast.literal_eval(pump["efficiency"])[0][0], ast.literal_eval(pump["efficiency"])[0][1], PlotDict['points'][0][0])
            IntersectionData["КПД"] = f"{efficiency:.2f} "# efficiency

            Cavitation_NPSH_m = self.give_Y_of_line_at_this_X(ast.literal_eval(pump["Cavitation_NPSH_m"])[0][0],
                                        ast.literal_eval(pump["Cavitation_NPSH_m"])[0][1], PlotDict['points'][0][0])
            IntersectionData["NPSH"] = f"{Cavitation_NPSH_m:.2f} "#  Cavitation_NPSH_m

            # IntersectionData["Перекачиваемая жидкость"] = "Вода 100 %"
            # print(IntersectionData)
            #self.dbList


            pump["Заданные параметры"] = IntersectionData
            self.OkDBList.append(pump)

        for pump in self.dbList:
            ok, speed = isThisPumpOK(pump)
            if True == ok:
                putThisPumpinOkDBList(pump,speed)
            # print(len(self.OkDBList))

    def giveMeGoodPumps(self, showCalculatedModel = False):
        self.OkDBList = []
        self.iterating_matcher(showCalculatedModel)

        # for each in self.OkDBList:
        #     # print(each)
        #     self.plotThis(each["PlotDict1"])
        #     self.plotThis(each["PlotDict2"])


        return self.OkDBList


    def __init__(self,toCalc):
        # print( toCalc)
        self.CalcValues = toCalc["CalcValues"]
        self.dbList = toCalc["dbList"]
        self.modelType = toCalc["modelType"]
        self.ShowAll = toCalc["ShowAll"]



    pass

# # "poly1d"#linear
# # toCalc = {'CalcValues': {'Flow': '100', 'pressure': '19', 'percents': '120', 'offsetX': '10', 'offsetY': '10'}, 'modelType': 'linear', 'ShowAll': False, 'dbList': [{'Model_Name': 'TestingModel1', 'max_pressure': ' 16 бар', 'liquid_pump_temp': ' -15C-110C', 'max_env_temp': ' 40С', 'engine_efficiency_class': ' IE2', 'Net_connection': ' 3~380V/50 Hz', 'rotation_frequency_nominal': ' 2900 1/min', 'Nominal_power_P2': ' P2 P2 15 кВт', 'Nominal_currency': ' 27 А', 'Moisture_protection': ' IP54', 'Isolation_Class': ' F', 'Sucking_pipe_branch': ' DN100', 'Pushing_pipe_branch': ' DN100', 'building_length': ' 480 мм', 'frame': ' GG20', 'working_wheel': ' GG20', 'Shaft': ' 1.4021', 'Weight': 'None', 'lift_H_m': '[([30.0, 101.92, 124.76], [19.96, 16.98, 9.65]), ([27.0, 98.92, 121.76], [15.96, 12.98, 5.65]), ([32.0, 101.92, 124.76], [21.96, 16.98, 9.65])]', 'Cavitation_NPSH_m': '[([0.0, 11.77, 23.54, 35.31, 47.07, 58.84, 70.61, 82.38, 94.15, 96.04, 105.92, 117.69, 129.45, 141.22, 152.99, 164.76], [1.14, 1.17, 1.2, 1.24, 1.29, 1.37, 1.46, 1.59, 1.76, 1.79, 1.98, 2.26, 2.61, 3.05, 3.58, 4.23])]', 'motor_power_P2_kW': '[([0.0, 11.77, 23.54, 35.31, 47.07, 58.84, 70.61, 82.38, 94.15, 96.04, 105.92, 117.69, 129.45, 141.22, 152.99, 164.76], [3.57, 3.84, 4.21, 4.67, 5.17, 5.68, 6.2, 6.7, 7.17, 7.24, 7.6, 7.99, 8.35, 8.67, 8.98, 9.28])]', 'efficiency': '[([0.0, 5.884298443, 11.76859689, 17.65289533, 23.53719377, 29.42149222, 35.30579066, 41.1900891, 47.07438755, 48.02030945, 52.95868599, 58.84298443, 64.72728288, 70.61158132, 76.49587976, 82.3801782], [7.14670725, 7.676693387, 8.429178213, 9.333978421, 10.33019519, 11.36621418, 12.39970552, 13.39762384, 14.33620825, 14.48044964, 15.20098233, 15.98675416, 16.69761627, 17.34694572, 17.957404, 18.56093713])]', 'Scale_Table': "{'size': '?'}", 'pump_wiring_connection_figure': 'connection_figures/test_connection.png', 'pump_figure': 'pump_figures/Test_pump_image.png'}]}
# # toCalc = {'CalcValues': {'Flow': '100', 'pressure': '19', 'percents': '120', 'offsetX': '10', 'offsetY': '10'}, 'modelType': 'poly1d', 'ShowAll': False, 'dbList': [{'Model_Name': 'TestingModel1', 'max_pressure': ' 16 бар', 'liquid_pump_temp': ' -15C-110C', 'max_env_temp': ' 40С', 'engine_efficiency_class': ' IE2', 'Net_connection': ' 3~380V/50 Hz', 'rotation_frequency_nominal': ' 2900 1/min', 'Nominal_power_P2': ' P2 P2 15 кВт', 'Nominal_currency': ' 27 А', 'Moisture_protection': ' IP54', 'Isolation_Class': ' F', 'Sucking_pipe_branch': ' DN100', 'Pushing_pipe_branch': ' DN100', 'building_length': ' 480 мм', 'frame': ' GG20', 'working_wheel': ' GG20', 'Shaft': ' 1.4021', 'Weight': 'None', 'lift_H_m': '[([30.0, 101.92, 124.76], [19.96, 16.98, 9.65]), ([27.0, 98.92, 121.76], [15.96, 12.98, 5.65]), ([32.0, 101.92, 124.76], [21.96, 16.98, 9.65])]', 'Cavitation_NPSH_m': '[([0.0, 11.77, 23.54, 35.31, 47.07, 58.84, 70.61, 82.38, 94.15, 96.04, 105.92, 117.69, 129.45, 141.22, 152.99, 164.76], [1.14, 1.17, 1.2, 1.24, 1.29, 1.37, 1.46, 1.59, 1.76, 1.79, 1.98, 2.26, 2.61, 3.05, 3.58, 4.23])]', 'motor_power_P2_kW': '[([0.0, 11.77, 23.54, 35.31, 47.07, 58.84, 70.61, 82.38, 94.15, 96.04, 105.92, 117.69, 129.45, 141.22, 152.99, 164.76], [3.57, 3.84, 4.21, 4.67, 5.17, 5.68, 6.2, 6.7, 7.17, 7.24, 7.6, 7.99, 8.35, 8.67, 8.98, 9.28])]', 'efficiency': '[([0.0, 5.884298443, 11.76859689, 17.65289533, 23.53719377, 29.42149222, 35.30579066, 41.1900891, 47.07438755, 48.02030945, 52.95868599, 58.84298443, 64.72728288, 70.61158132, 76.49587976, 82.3801782], [7.14670725, 7.676693387, 8.429178213, 9.333978421, 10.33019519, 11.36621418, 12.39970552, 13.39762384, 14.33620825, 14.48044964, 15.20098233, 15.98675416, 16.69761627, 17.34694572, 17.957404, 18.56093713])]', 'Scale_Table': "{'size': '?'}", 'pump_wiring_connection_figure': 'connection_figures/test_connection.png', 'pump_figure': 'pump_figures/Test_pump_image.png'}]}
# toCalc = {'CalcValues': {'Model_Name': 'TestingModel1', 'max_pressure': ' 16 бар', 'liquid_pump_temp': ' -15C-110C', 'max_env_temp': ' 40С', 'engine_efficiency_class': ' IE2', 'Net_connection': ' 3~380V/50 Hz', 'rotation_frequency_nominal': ' 2900 1/min', 'Nominal_power_P2': ' P2 P2 15 кВт', 'Nominal_currency': ' 27 А', 'Moisture_protection': ' IP54', 'Isolation_Class': ' F', 'Sucking_pipe_branch': ' DN100', 'Pushing_pipe_branch': ' DN100', 'building_length': ' 480 мм', 'frame': ' GG20', 'working_wheel': ' GG20', 'Shaft': ' 1.4021', 'Weight': 'None', 'lift_H_m': '[([30.0, 101.92, 124.76], [19.96, 16.98, 9.65]), ([27.0, 98.92, 121.76], [15.96, 12.98, 5.65]), ([32.0, 101.92, 124.76], [21.96, 16.98, 9.65])]', 'Cavitation_NPSH_m': '[([0.0, 11.77, 23.54, 35.31, 47.07, 58.84, 70.61, 82.38, 94.15, 96.04, 105.92, 117.69, 129.45, 141.22, 152.99, 164.76], [1.14, 1.17, 1.2, 1.24, 1.29, 1.37, 1.46, 1.59, 1.76, 1.79, 1.98, 2.26, 2.61, 3.05, 3.58, 4.23])]', 'motor_power_P2_kW': '[([0.0, 11.77, 23.54, 35.31, 47.07, 58.84, 70.61, 82.38, 94.15, 96.04, 105.92, 117.69, 129.45, 141.22, 152.99, 164.76], [3.57, 3.84, 4.21, 4.67, 5.17, 5.68, 6.2, 6.7, 7.17, 7.24, 7.6, 7.99, 8.35, 8.67, 8.98, 9.28])]', 'efficiency': '[([0.0, 5.884298443, 11.76859689, 17.65289533, 23.53719377, 29.42149222, 35.30579066, 41.1900891, 47.07438755, 48.02030945, 52.95868599, 58.84298443, 64.72728288, 70.61158132, 76.49587976, 82.3801782], [7.14670725, 7.676693387, 8.429178213, 9.333978421, 10.33019519, 11.36621418, 12.39970552, 13.39762384, 14.33620825, 14.48044964, 15.20098233, 15.98675416, 16.69761627, 17.34694572, 17.957404, 18.56093713])]', 'Scale_Table': "{'size': '?','size2': '?222'}", 'pump_wiring_connection_figure': 'connection_figures/test_connection.png', 'pump_figure': 'pump_figures/Test_pump_image.png', 'PlotDict1': {'Рассчитанная модель': [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.000000000000001, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.000000000000002, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.000000000000004, 28.999999999999996, 30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0, 40.0, 41.0, 42.0, 43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.00000000000001, 56.00000000000001, 56.99999999999999, 57.99999999999999, 59.0, 60.0, 61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0, 77.0, 78.0, 79.0, 80.0, 81.0, 82.0, 83.0, 84.0, 85.0, 86.0, 87.0, 88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0, 97.0, 98.0, 99.0, 100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.00000000000001, 110.00000000000001, 111.00000000000001, 112.00000000000001, 112.99999999999999, 113.99999999999999, 114.99999999999999, 115.99999999999999, 117.0, 118.0, 119.0, 120.0], [0.0019, 0.0076, 0.0171, 0.0304, 0.04750000000000001, 0.0684, 0.09310000000000002, 0.1216, 0.15389999999999998, 0.19000000000000003, 0.2299, 0.2736, 0.32110000000000005, 0.37240000000000006, 0.4275, 0.4864, 0.5491000000000001, 0.6155999999999999, 0.6859, 0.7600000000000001, 0.8378999999999999, 0.9196, 1.0051, 1.0944, 1.1875, 1.2844000000000002, 1.3851000000000002, 1.4896000000000003, 1.5978999999999999, 1.71, 1.8259, 1.9456, 2.0691, 2.1964000000000006, 2.3274999999999997, 2.4623999999999997, 2.6010999999999997, 2.7436, 2.8899000000000004, 3.0400000000000005, 3.1938999999999993, 3.3515999999999995, 3.5130999999999997, 3.6784, 3.8475, 4.0204, 4.1971, 4.3776, 4.5619, 4.75, 4.9419, 5.137600000000001, 5.3371, 5.540400000000001, 5.7475000000000005, 5.958400000000001, 6.1731, 6.3915999999999995, 6.613899999999999, 6.84, 7.0699, 7.3036, 7.5411, 7.7824, 8.027500000000002, 8.2764, 8.529100000000001, 8.785600000000002, 9.045899999999998, 9.309999999999999, 9.5779, 9.849599999999999, 10.125099999999998, 10.404399999999999, 10.6875, 10.9744, 11.2651, 11.559600000000001, 11.857900000000003, 12.160000000000002, 12.465900000000003, 12.775599999999997, 13.089099999999998, 13.406399999999998, 13.7275, 14.052399999999999, 14.3811, 14.7136, 15.049900000000001, 15.39, 15.733900000000002, 16.0816, 16.433100000000003, 16.7884, 17.1475, 17.5104, 17.8771, 18.2476, 18.6219, 19.0, 19.3819, 19.7676, 20.1571, 20.550400000000003, 20.9475, 21.3484, 21.7531, 22.161600000000004, 22.573900000000002, 22.990000000000002, 23.409900000000004, 23.833600000000004, 24.261099999999995, 24.6924, 25.127499999999998, 25.566399999999998, 26.009099999999997, 26.455599999999997, 26.9059, 27.36]], 'Скорость 1': [[30.0, 101.92, 124.76], [19.96, 16.98, 9.65]], 'Скорость 2': [[27.0, 98.92, 121.76], [15.96, 12.98, 5.65]], 'Скорость 3': [[32.0, 101.92, 124.76], [21.96, 16.98, 9.65]], 'КПД': ([0.0, 5.884298443, 11.76859689, 17.65289533, 23.53719377, 29.42149222, 35.30579066, 41.1900891, 47.07438755, 48.02030945, 52.95868599, 58.84298443, 64.72728288, 70.61158132, 76.49587976, 82.3801782], [7.14670725, 7.676693387, 8.429178213, 9.333978421, 10.33019519, 11.36621418, 12.39970552, 13.39762384, 14.33620825, 14.48044964, 15.20098233, 15.98675416, 16.69761627, 17.34694572, 17.957404, 18.56093713])}, 'PlotDict2': {'motor_power_P2_kW': ([0.0, 11.77, 23.54, 35.31, 47.07, 58.84, 70.61, 82.38, 94.15, 96.04, 105.92, 117.69, 129.45, 141.22, 152.99, 164.76], [3.57, 3.84, 4.21, 4.67, 5.17, 5.68, 6.2, 6.7, 7.17, 7.24, 7.6, 7.99, 8.35, 8.67, 8.98, 9.28]), 'Cavitation_NPSH_m': ([0.0, 11.77, 23.54, 35.31, 47.07, 58.84, 70.61, 82.38, 94.15, 96.04, 105.92, 117.69, 129.45, 141.22, 152.99, 164.76], [1.14, 1.17, 1.2, 1.24, 1.29, 1.37, 1.46, 1.59, 1.76, 1.79, 1.98, 2.26, 2.61, 3.05, 3.58, 4.23])}, 'Заданные параметры': {'Модель': 'TestingModel1', 'Производительность': '97.01  м3/ч', 'Напор': '17.88  (m)', 'Мощность на валу': '7.28 ', 'КПД': '0.00 ', 'NPSH': '1.81 ', 'Перекачиваемая жидкость': 'Вода 100 %'}}}
#
# cm = calcManager(toCalc)
# cm.giveMeGoodPumps()


