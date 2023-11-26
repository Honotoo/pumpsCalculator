import tkinter
from tkinter import ttk
from DB import DB_manager
import re
from tools import splitterabstracted,split_size_table
import os
from valuator import calcManager, plotThis
from pdfGen import pdfManager
#pip install openpyxl
#pip install numpy
#pip install matplotlib
#pip install scipy
#pip install sklearn

class fieldAndLabel:
    myName = "UnnamedfieldAndLabel"
    label = ""
    raw = 0
    column = 0
    entryDefault = ''
    entry = None#tkinter.Entry()

    def set(self, value, alsoDefault = False):
        self.entry.delete(0, len(self.entry.get()))
        self.entry.insert(0, str(value))
        if alsoDefault == True:
            self.entryDefault = str(value)
    def content(self):
        try:
            return self.entry.get()
        except:
            print("объект "+self.myName+ " не может взять данные из поля")
            return self.myName,None
    def clear(self):
        try:
            self.entry.delete(0, len(self.entry.get()))
            self.entry.insert(0, self.entryDefault)
        except Exception as e:
            print("не получается очистить Entry в  " + self.myName)
        pass

    def __init__(self, frame, myName, Label, raw, column, entryDefault="" ):
        self.myName = myName
        self.label = Label
        self.raw = raw
        self.column = column
        self.entryDefault = entryDefault

        tkinter.Label(frame, text=self.label).grid(row=self.raw, column=self.column)
        self.entry = tkinter.Entry(frame, width=40)
        self.entry.grid(row=self.raw+1, column=self.column, columnspan=1)
        self.entry.insert(0, self.entryDefault)



class adminWindow:
    columnDescriptions = []
    EntriesList = {}
    db = None

    def fillContent(self,frame):
        def CountXY(amount, Xequals=1, Yequals=10):
            x = 0
            y = 0
            for Ys in range(1, 100):
                for Xs in range(1, 100):
                    if Ys * Yequals * Xs * Xequals >= amount:
                        y = Ys * Yequals
                        x = Xs * Xequals
                        return x, y
            return x, y
        def count(xNow,yNow):
            yNow+=1
            if yNow>X:
                yNow=0
                xNow+=1
            return xNow, yNow
        xNow,yNow = 0,0

        additionalPlacesToDB = 20
        X, Y = CountXY(len(self.columnDescriptions)+additionalPlacesToDB, Xequals=1, Yequals=4)

        flow_rate_Q_m3_h = fieldAndLabel(frame, "flow_rate_Q_m3_h", "Расход - Q(m3 / h) (исп. если не введен для H/NPSH/P2/КПД)", yNow * 2, xNow, entryDefault="")
        self.EntriesList["flow_rate_Q_m3_h"] = flow_rate_Q_m3_h
        xNow, yNow = count(xNow, yNow)

        for columnIndex in range(len(self.columnDescriptions)):
            entryObj = fieldAndLabel(frame, self.columnDescriptions[columnIndex][0], self.columnDescriptions[columnIndex][2], yNow*2, xNow, entryDefault="")
            self.EntriesList[self.columnDescriptions[columnIndex][0]] = entryObj
            xNow, yNow = count(xNow, yNow)

        disAssemble_line = fieldAndLabel(frame, "disAssemble_line", "разбить введенные данные в поля автоматически", yNow * 2, xNow, entryDefault="")
        self.EntriesList["disAssemble_line"] = disAssemble_line
        xNow, yNow = count(xNow, yNow)
        tkinter.Button(frame, text="разобрать по формам", command=lambda: self.disAssemble_line(text=self.EntriesList["disAssemble_line"].content())).grid(row=yNow * 2, column=xNow, columnspan=1, rowspan=2)
        xNow, yNow = count(xNow, yNow)
        tkinter.Button(frame, text=" Предпросмотр PDF ",command=lambda: self.ShowPDF()).grid(row=yNow * 2, column=xNow, columnspan=1, rowspan = 2)
        xNow, yNow = count(xNow, yNow)
        tkinter.Button(frame, text=" Добавить запись в базу",command=lambda: self.add_to_DB()).grid(row=yNow * 2, column=xNow, columnspan=1, rowspan = 2)
        xNow, yNow = count(xNow, yNow)
        AdminKeyEntry = fieldAndLabel(frame,"AdminKeyEntry", "Ключ администратора", yNow * 2, xNow, entryDefault="")
        self.EntriesList["AdminKeyEntry"] = AdminKeyEntry
        xNow, yNow = count(xNow, yNow)
        tkinter.Button(frame, text=" Сменить ключ администратора",command=lambda: self.updateAdminKey()).grid(row=yNow * 2, column=xNow, columnspan=1, rowspan = 2)
        xNow, yNow = count(xNow, yNow)
        Unload_from_DB_to_XLSX_entry = fieldAndLabel(frame,"Unload_from_DB_to_XLSX_entry", "Вывести таблицу из базы данных в excel", yNow * 2, xNow, entryDefault="PumpsColums")
        self.EntriesList["Unload_from_DB_to_XLSX_entry"] = Unload_from_DB_to_XLSX_entry
        xNow, yNow = count(xNow, yNow)
        tkinter.Button(frame, text=" DB => XL",command=lambda: self.Unload_from_DB_to_XLSX()).grid(row=yNow * 2, column=xNow, columnspan=1, rowspan = 2)
        xNow, yNow = count(xNow, yNow)
        Upload_from_XLSX_to_DB_entry = fieldAndLabel(frame,"Upload_from_XLSX_to_DB_entry", "Занести таблицу в БД", yNow * 2, xNow, entryDefault="PumpsColums")
        self.EntriesList["Upload_from_XLSX_to_DB_entry"] = Upload_from_XLSX_to_DB_entry
        xNow, yNow = count(xNow, yNow)
        tkinter.Button(frame, text=" XL => DB",command=lambda: self.Upload_from_XLSX_to_DB()).grid(row=yNow * 2, column=xNow, columnspan=1, rowspan = 2)
        xNow, yNow = count(xNow, yNow)
        tkinter.Button(frame, text="Привести колонки таблицы насосов\nв соответствии с таблицей описания колонок", command=lambda: self.editColumnsAccordingTo()).grid(row=yNow * 2,
                                                                                                    column=xNow,
                                                                                                    columnspan=1,
                                                                                                    rowspan=2)

        try:
            self.EntriesList["pump_figure"].set('pump_figures/Test_pump_image.png', alsoDefault = True)
        except:pass
        try:
            self.EntriesList["pump_wiring_connection_figure"].set('connection_figures/test_connection.png', alsoDefault = True)
        except:pass
        pass


    #Инструменты работы внутри окна
    def Clear_all_entry(self):
        pass
        # for k,v in self.EntriesList.items():
        #     self.EntriesList[k].clear()

    def CollectAllForms(self):
        dict_to_row = {}
        for k,v in self.EntriesList.items():
            dict_to_row[k] = self.EntriesList[k].content()
        # lift_H_m
        dict_to_row['lift_H_m'] =str(splitterabstracted(dict_to_row['lift_H_m']))
        # Cavitation_NPSH_m
        dict_to_row['Cavitation_NPSH_m'] = str(splitterabstracted(dict_to_row['Cavitation_NPSH_m']))
        # motor_power_P2_kW
        dict_to_row['motor_power_P2_kW'] = str(splitterabstracted(dict_to_row['motor_power_P2_kW']))
        # efficiency
        dict_to_row['efficiency'] = str(splitterabstracted(dict_to_row['efficiency']))
        dict_to_row['Scale_Table'] = str(split_size_table(dict_to_row['Scale_Table']))

        # print(dict_to_row['lift_H_m'])
        # print(dict_to_row['Cavitation_NPSH_m'])
        # print(dict_to_row['motor_power_P2_kW'])
        # print(dict_to_row['efficiency'])
        # print(dict_to_row['Scale_Table'])
        return dict_to_row

        # from tkkk import alert_window
        # alert_window("не получилось собрать данные из полей. \nскорее всего неправильно введеный Расход или эффективность:\n" + str(e))
        pass

    def disAssemble_line(self, text="42"):
        variants = {"max_pressure":r"(?<=давление).*?(?=\n)",
                    "liquid_pump_temp":r"(?<=жидкости).*?(?=\n)",
                    "max_env_temp":r"(?<=Среды).*?(?=\n)",
                    "engine_efficiency_class":r"(?<=двигателя).*?(?=\n)",
                    "Net_connection":r"(?<=сети).*?(?=\n)",
                    'rotation_frequency_nominal':r"(?<=вращения).*?(?=\n)",
                    "Nominal_power_P2":r"(?<=мощность).*?(?=\n)",
                    "Nominal_currency":r"(?<=ток).*?(?=\n)",
                    "Moisture_protection":r"(?<=защиты).*?(?=\n)",
                    "Isolation_Class":r"(?<=изоляции).*?(?=\n)",
                    "Sucking_pipe_branch":r"(?<=всасывания).*?(?=\n)",
                    "Pushing_pipe_branch":r"(?<=напорной стороне).*?(?=\n)",
                    "building_length":r"(?<=длина).*?(?=\n)",
                    "frame":r"(?<=Корпус).*?(?=\n)",
                    "working_wheel":r"(?<=колесо).*?(?=\n)",
                    "Shaft":r"(?<=Вал).*?(?=\n)",
                    "Weight":r"(?<=Вес).*?(?=кг)"
                    }
        for k,v in variants.items():
            try:
                self.EntriesList[k].set(re.search(variants[k], text)[0])
            except:
                pass


    def ShowPDF(self):
        The_Line_dict = self.CollectAllForms()
        print(The_Line_dict)
        # try:
        #     The_Line_dict =  self.CollectAllForms()
        #     Filename = 'cache_images\CachePDF.pdf'
        #     makePDF(The_Line_dict, Filename, Q=None, H=None, percents=120)
        # except Exception as e:
        #     # from tkkk import alert_window
        #     alert_window("не получилось открыть пдф:\n" + str(e))

    def add_to_DB(self):
        # собираем контент с полей
        The_Line_dict =  self.CollectAllForms()
        Columns_ordered = self.db.giveColumnDescription("Pumps", what = "Names")
        print(The_Line_dict)
        NewLineOrdered = []
        for each in Columns_ordered:
            NewLineOrdered.append(The_Line_dict[each])


        amount = ""
        for each in range(len(NewLineOrdered)):
            amount = amount + "?"
            if NewLineOrdered.index(NewLineOrdered[each]) < len(NewLineOrdered) - 1:
                amount = amount + ","

        SQLquery = f"INSERT INTO Pumps VALUES({amount})"
        print(SQLquery)
        self.db.RunQueryNoReturn(SQLquery, Values = NewLineOrdered)
        self.Clear_all_entry()

    def updateAdminKey(self):
        num = self.EntriesList["AdminKeyEntry"].content()
        self.db.tableWithSingleValueOperation("AdminKey","set", newValue = "num")
        # NewAdminKeyTable(num)
        self.EntriesList["AdminKeyEntry"].clear()
        print(num)
        # print(get_AdminKeyNow())
        # NewAdminKeyTable.delete(0, last=END)

    def Upload_from_XLSX_to_DB(self):
        try:
            # Upload_from_XLSX_to_DB_entry
            # Unload_from_DB_to_XLSX_entry
            FileName = self.EntriesList["Upload_from_XLSX_to_DB_entry"].content()
            self.EntriesList["Upload_from_XLSX_to_DB_entry"].clear()
            try:
                self.db.RunQueryNoReturn(f"DROP TABLE {FileName};")
            except:
                pass
            self.db.CreateTableWithThisXLS(FileAndTableName=FileName)
            # table = RunQuery(DBName, "SELECT * FROM %s" % (FileName))

            # print(givecolumnNames(DBName, "Pumps"))
            # print(table)
            # CreateTableWithThisXLS(DBName, FileAndTableName="Pumpsxlsx")
            pass
        except Exception as e:
            print(e)
            # from tkkk import alert_window
            # alert_window("загрузить XLS в базу данных не вышло\nВозможно поля изменены как-то странно:\n" + str(e))

    def Unload_from_DB_to_XLSX(self):
        try:
            FileName = self.EntriesList["Unload_from_DB_to_XLSX_entry"].content()
            self.EntriesList["Unload_from_DB_to_XLSX_entry"].clear()
            FileName = self.db.writeXLS(FileName)
            try:
                os.startfile(FileName)
            except:
                os.system("xdg-open \"%s\"" % FileName)
            pass
        except Exception as e:
            print(e)
            # from tkkk import alert_window
            #alert_window("выгрузить базу данных в XLS не вышло:\n" + str(e))
    def editColumnsAccordingTo(self):
        ndb = self.db.RunQuery("SELECT * FROM {}".format("PumpsColums"))
        self.db.editColumnsAccordingTo("PumpsColums", "Pumps", ndb)

    def __init__(self, dbObject):
        self.db = dbObject
        try:
            self.columnDescriptions = self.db.RunQuery("SELECT * FROM {}".format("PumpsColums"))
        except:
            self.db.setDefaultColumnsList("PumpsColums")
            self.db.setDefaultBaseTable("Pumps")
            self.columnDescriptions = self.db.RunQuery("SELECT * FROM {}".format("PumpsColums"))
        root2 = tkinter.Toplevel()
        frame = ttk.Frame(root2, padding=0)
        frame.grid()
        self.fillContent(frame)



class  singleResultPresent:
    columnDescriptions = None
    pumpUnit = None
    rowCount = 0

    def GenPdf(self):
        pdf = pdfManager(self.columnDescriptions, self.pumpUnit)
        pdf.givePDF()
        print("GenPdf")
        pass

    def putText(self,frame):
        self.rowCount = 0
        for sign, value in self.pumpUnit['Заданные параметры'].items():

            tkinter.Label(frame, text=sign)#.grid(row=self.rowCount, column=0, columnspan=2)
            tkinter.Label(frame, text=value)#.grid(row=self.rowCount, column=2, columnspan=1)
            self.rowCount+=1


        bLook2 = tkinter.Button(frame, text="\n Скачать отчет \n", command=lambda : self.GenPdf())#.grid(row=int(self.rowCount/2), column=5, rowspan=2)
        print(self.pumpUnit)
        pass

    def __init__(self,frame, columnDescriptions, pumpUnit):
        self.columnDescriptions = columnDescriptions
        self.pumpUnit = pumpUnit

        self.putText(frame)






class calcWindow :
    frame = None
    columnDescriptions = None
    goodPumps = None
    resultUnits = []

    def fillcalcContent(self):
        for pump in self.goodPumps:
            # print(pump)
            ViewUnit = singleResultPresent(self.frame, self.columnDescriptions, pump)
            self.resultUnits.append(ViewUnit)
            # print(ViewUnit)
            #ViewUnit.putText()
        pass


    def __init__(self, columnDescriptions, goodPumps):
        self.columnDescriptions = columnDescriptions
        self.goodPumps = goodPumps

        root3 = tkinter.Toplevel()
        # self.frame = ttk.Frame(root3, padding=0)
        # self.frame.grid()



class item:
    rowCount = 0

    def GenPdf(self):
        pdf = pdfManager(self.columnDescriptions, self.pumpUnit)
        pdf.givePDF()
        print("GenPdf")
        pass
    def __init__(self,root, frm,canv,Y_position_pointer,columnDescriptions, pumpUnit):
        self.columnDescriptions = columnDescriptions
        self.pumpUnit = pumpUnit


        for sign, value in self.pumpUnit['Заданные параметры'].items():

            tkinter.Label(frm, text=sign).grid(row=self.rowCount, column=0, columnspan=2)
            tkinter.Label(frm, text=value).grid(row=self.rowCount, column=2, columnspan=1)
            self.rowCount+=1

        basicGap = 10
        # tkinter.Label(frm, text="Производительность:").grid(row=0, column=0, columnspan=2)
        # tkinter.Label(frm, text=fr" м3/ч").grid(row=0, column=2, columnspan=1)

        bLook2 = tkinter.Button(frm, text="\n Скачать отчет \n", command=lambda: self.GenPdf())

        bLook2 = bLook2.grid(row=3, column=5, rowspan=2)
        canv.create_window(basicGap, Y_position_pointer + basicGap, anchor=tkinter.NW, window=frm)
        Y_position_pointer = Y_position_pointer + basicGap + 180

        frm = tkinter.Frame(root, width=32, height=123, bg="#ffffff", bd=2)
        frm.config(relief=tkinter.SUNKEN)
        print(pumpUnit)
        img = plotThis(pumpUnit["PlotDict1"])

        img_path = "cache_images" + "/" + pumpUnit['Model_Name'] + ".png"
        img.savefig(img_path, bbox_inches='tight')

        img = tkinter.PhotoImage(file=img_path)


        # img.show()
        # button1 = tkinter.Button(frm, image=img)
        button1 = tkinter.Button(frm, image=img)
        button1.image = img
        button1.pack()
        canv.create_window(basicGap, Y_position_pointer, anchor=tkinter.NW, window=frm)



class calcW:

    def __init__(self,columnDescriptions, goodPumps):
        basicGap = 10
        TextLength = 150
        commonWidth = 456
        ImageLength = 320
        ScrollLength = len(goodPumps)*1000

        root3 = tkinter.Toplevel()  # Note Toplevel, NOT Tk.
        parent = root3
        color = 'white'
        canv = tkinter.Canvas(root3, bg=color, relief=tkinter.SUNKEN)
        canv.config(width=1200, height=1000)

        canv.config(scrollregion=(-20, 0, commonWidth, ScrollLength))
        canv.config(highlightthickness=6)

        ybar = tkinter.Scrollbar(root3)
        ybar.config(command=canv.yview)
        ## connect the two widgets together
        canv.config(yscrollcommand=ybar.set)
        ybar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        canv.pack(side=tkinter.LEFT, expand=tkinter.NO, fill=tkinter.BOTH)

        Y_position_pointer = 0
        spisok_k_frm = []
        for ctr in range(len(goodPumps)):
            frm = tkinter.Frame(root3, width=commonWidth, height=TextLength, bg="#ffffff", bd=2)
            frm.config(relief=tkinter.SUNKEN)
            spisok_k_frm.append(frm)

        for frm,pumpUnit in zip(spisok_k_frm,goodPumps):
            i = item(root3, frm, canv, Y_position_pointer,columnDescriptions, pumpUnit)
            Y_position_pointer+=800





class mainWindow:
    db = DB_manager("DB.sql")
    CalcEntries = {}
    columnDescriptions = []
    modelType = None
    showCalculatedModel = None

    # в калькуляторе я беру из бд сразу всю таблицу и работаю сразу со всей таблицей, что довольно нагруженно,
    # но с другой стороны менеджер калькулятора сразу возврващает готовый для построения ПДФ словарь
    # в общем тут в идеале бы сделать другую систему, или бахнуть генератором, но может и не надо
    def OpenCalculator(self):

        modeltype = "linear"
        if self.modelType.get() == 0:
            modeltype = "linear"
        else:
            modeltype ="poly1d"


        showCalculated = True
        if self.showCalculatedModel.get() == 0:
            showCalculated = False
        else:
            showCalculated =True

        print(" Сбор данных для расчета")
        CalcValues = {}
        for k,v in self.CalcEntries.items():
            CalcValues[k] = v.content()
            # print(k, v.content())
        CalcValues.pop("key")

        dbTable = self.db.RunQuery("SELECT * FROM {}".format("Pumps"))
        dbNames = self.db.giveColumnDescription("Pumps", what="Names")

        dbList = []
        for row in dbTable:
            LineDict = {}
            for name, value in zip(dbNames, row):
                LineDict[name] = value
            dbList.append(LineDict)

        toCalc = {"CalcValues":CalcValues, "modelType":modeltype, "ShowAll":False, "dbList":dbList}
        print("Подбор вариантов")
        self.columnDescriptions = self.db.RunQuery("SELECT * FROM {}".format("PumpsColums"))
        # print(self.columnDescriptions)

        cm = calcManager(toCalc)
        # cm.iterating_matcher(showCalculatedModel = True)
        # pdf = pdfManager(self.columnDescriptions, cm.OkDBList[0])
        goodPumps = cm.giveMeGoodPumps(showCalculatedModel = showCalculated)
        # print(len(goodPumps))

        # CW = calcWindow(self.columnDescriptions, goodPumps)
        CW = calcW(self.columnDescriptions, goodPumps)


        # print(CW)


        # pdf = pdfManager(self.columnDescriptions, goodPumps[1])
        # pdf.givePDF()






        # # for data in cm.OkDBList:
        # #     # print(data)
        # #     pass
        # #
        # #     # print(data["PlotDict1"])
        # #     # cm.plotThis(data["PlotDict1"])
        # #     # cm.plotThis(data["PlotDict2"])
        # # print(toCalc)




    def fillContent(self, frame):
        Flow = fieldAndLabel(frame, "Flow" , "Производительность(Q)", 0, 0, entryDefault = "100")
        pressure = fieldAndLabel(frame, "pressure" , "Напор(H)", 2, 0, entryDefault = "19")
        percents = fieldAndLabel(frame, "percents", "Проценты", 4, 0, entryDefault="120")
        # offsetX = fieldAndLabel(frame, "offsetX", "offsetX", 6, 0, entryDefault="10")
        # offsetY = fieldAndLabel(frame, "offsetY", "offsetY", 8, 0, entryDefault="10")
        # key = fieldAndLabel(frame, "key", "Указание категории насоса(Isolation_Class = F)", 12, 0,entryDefault="")
        key = fieldAndLabel(frame, "key", "Ключ администратора", 14, 0)

        self.CalcEntries["Flow"] = Flow
        self.CalcEntries["pressure"] = pressure
        self.CalcEntries["percents"] = percents
        self.modelType = tkinter.IntVar()
        ttk.Radiobutton( frame, text="линейная", value=0, variable=self.modelType ).grid(row=6, column=0)
        ttk.Radiobutton( frame, text="полиномиальная модель", value=1, variable=self.modelType ).grid(row=7, column=0)

        self.showCalculatedModel = tkinter.IntVar()
        ttk.Radiobutton( frame, text="Скрыть модель", value=0, variable=self.showCalculatedModel ).grid(row=8, column=0)
        ttk.Radiobutton( frame, text="Показать модель расчетов", value=1, variable=self.showCalculatedModel ).grid(row=9, column=0)

        # self.printAllPumps = tkinter.IntVar()
        # ttk.Radiobutton( frame, text="Выбрать только подходящие насосы", value=0, variable=self.printAllPumps ).grid(row=10, column=0)
        # ttk.Radiobutton( frame, text="Показать Все насосы", value=1, variable=self.printAllPumps ).grid(row=11, column=0)


        self.CalcEntries["key"] = key
        tkinter.Button(frame, text="\n\n провести подбор \n\n", command =lambda: self.OpenCalculator()).grid(row=0, column=1, rowspan = 4)
        tkinter.Button(frame, text="Окно администратора", command =lambda: self.OpenAdminWindow()).grid(row=8, column=1, columnspan=1)
        # tkinter.Button(frame, text="Окно администратора", command =lambda: print(r2.)).grid(row=8, column=1, columnspan=1)

    # ['variable', 'value', 'command', 'takefocus', 'text', 'textvariable', 'underline', 'width', 'image', 'compound',
    #  'padding', 'state', 'cursor', 'style', 'class']


    def OpenAdminWindow(self):
        p = adminWindow(self.db)


        # a = self.db.tableWithSingleValueOperation( "AdminKey","get")#get_AdminKeyNow()
        # b = self.FormsList[-1].content()
        # self.FormsList[-1].clear()
        # if a == b:
        #     adminWindow()
        # else:
        #     # alert_window("Пароль не верный")
        #     print("adminWindow error")0-------------------------------


    def __init__(self):
        root = tkinter.Tk()
        window1_frame = ttk.Frame(root, padding=0)
        window1_frame.grid()
        self.fillContent(window1_frame)
        root.mainloop()







if __name__ == '__main__':
    m = mainWindow()
    pass
