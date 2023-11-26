from fpdf import FPDF
import os
import ast
from PIL import Image
from valuator import plotThis

import time




class pdfManager:
    columnDescriptions = None
    PumpData = None


    cursorPosition = 25
    interval = 4
    TableLeftAlign = 125
    FontSize = 10
    imgOffset = 22
    CachImafesNames = ['cache_images\H_Q_plot.png', 'cache_images\_NPSH_P2_plot.png']
    pdf = None

    def makeBasicPDF(self):
        class PDF(FPDF):
            pass
        self.pdf = PDF()
        self.pdf.alias_nb_pages()
        self.pdf.add_page()
        self.pdf.add_font('Times', '', 'TimesNewRomanRegular.ttf', uni=True)
        self.pdf.add_font('TimesB', 'B', 'Times New Roman Bold.ttf', uni=True)
        self.Font()
        return self.pdf

    def move(self):
        self.cursorPosition = self.cursorPosition + self.interval
        return self.cursorPosition

    def Font(self,bold = False, FontSize = 10 ):
        if bold == True:
            self.pdf.set_font('TimesB', style='B', size=FontSize)
        else:
            self.pdf.set_font('Times', style='', size=FontSize)

    def printLine(self,text1, text2, Bold = False):
        if Bold:
            self.Font(bold = True, FontSize = 10)
        self.pdf.text(self.TableLeftAlign, self.cursorPosition, text1)
        self.pdf.text(self.TableLeftAlign + 53, self.cursorPosition, text2)
        self.Font()
        self.move()

    def tablePart(self,Header, CategoryAndValue):
        self.move()
        self.printLine(Header, "", Bold = True)
        for Category, Value in CategoryAndValue.items():
            self.printLine(Category, Value)

    def assembleTable(self):
        resultingTable = {}
        # собрать пары ключ - имя колонки значение - заголовок колонки
        for Column_Description in self.columnDescriptions:
            if Column_Description[1] != 'не текст' and Column_Description[1] not in resultingTable.keys():
                resultingTable[Column_Description[1]] = {}
        
        # собрать словарь ключ - заголовок группы. Ключ - словарь из описания поля и значения поля
        for each in self.columnDescriptions:
            if each[1] in resultingTable.keys():
                resultingTable[each[1]][each[2]] = self.PumpData[each[0]]
                
        # фильтруем поля. Если есть такие, в которых есть только (None, "", " ")  то их выкинем

        resultingTable2 = {}
        for groupName, group in resultingTable.items():
            resultingTable2[groupName] = {}
            deleteGroup = True
            for itemName, itemValue in group.items():
                if itemValue not in [None, "", " ","None"]:
                    resultingTable2[groupName][itemName] =itemValue
                    deleteGroup = False
            if deleteGroup == True:
                resultingTable2.pop(groupName)
        return resultingTable2
        pass


    def givePDF(self):
        self.makeBasicPDF()
        print(self.PumpData)

        self.tablePart("Заданные параметры", self.PumpData["Заданные параметры"])

        assembledTable = self.assembleTable()
        for Header, CategoryAndValue in assembledTable.items():
            self.tablePart(Header, CategoryAndValue)

        name1 = 'cache_images\H_Q_plot.png'
        name2 = 'cache_images\_NPSH_P2_plot.png'
        img1 = plotThis(self.PumpData['PlotDict1'], commonEnv=True)
        img1.savefig(name1, bbox_inches='tight')
        img2 = plotThis(self.PumpData['PlotDict2'], commonEnv=True)
        img2.savefig(name2, bbox_inches='tight',transparent = True)

        width1, height1 = img1.get_size_inches() * img1.get_dpi()
        width2, height2 = img2.get_size_inches() * img2.get_dpi()
        pump_im = Image.open(self.PumpData["pump_figure"])
        width3, height3 = pump_im.size


        self.pdf.image(name1, x=10, y=self.imgOffset, w=100)
        self.pdf.image(name2, x=10, y=self.imgOffset + height1 / 10 + 2, w=100)
        self.pdf.image(self.PumpData["pump_figure"], x=10, y=self.imgOffset + 4 + height1 / 10 + height2 / 10 + 4, w=100)

        TheTableData = ast.literal_eval(self.PumpData["Scale_Table"])

        self.pdf.set_xy(10, self.imgOffset + 4 + height1 / 10 + height2 / 10 + height3 / 11)
        for k, v in TheTableData.items():
            self.pdf.cell(12, 6, str(k), 1, 0, 'C')

        self.pdf.set_xy(10, self.imgOffset + 4 + height1 / 10 + height2 / 10 + height3 / 11 + 6)
        for k, v in TheTableData.items():
            self.pdf.cell(12, 6, str(v), 1, 0, 'C')


        self.pdf.set_xy(self.TableLeftAlign - 2, self.cursorPosition)
        self.pdf.cell(40, 6, "Мощность двигателя P2 <= 3 кВт", 0, 0, 'C')
        self.pdf.cell(40, 6, "        P2 >= 3 кВт", 0, 0, 'C')
        self.pdf.image(self.PumpData['pump_wiring_connection_figure'], x=self.TableLeftAlign, y=self.cursorPosition + 6, w=80)



        Filename = str("pdff.pdf")
        try:
            Filename = self.PumpData["Model_Name"]+ ".pdf"
        except:
            pass

        print(Filename)
        self.pdf.output(Filename, 'F')
        try:
            os.startfile(Filename)
        except:
            os.system("xdg-open \"%s\"" % Filename)
















    def __init__(self,columnDescriptions,PumpData):
        self.columnDescriptions = columnDescriptions
        self.PumpData = PumpData























