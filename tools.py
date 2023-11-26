import re
import ast
# L:500,B:430,H:855  ==>  {"L":"500","B":"430","H":"855"}
def split_size_table(stroka):
    try:
        if stroka == "":
            return {"size": "?"}
        Return_Dictionary = {}
        K_V_list = stroka.split(',')
        for each in K_V_list:
            Return_Dictionary[each.split(":")[0]] = each.split(":")[1]
        return Return_Dictionary
    except Exception as e:
        # from tkkk import alert_window
        # alert_window("не правильно введены данные в поле таблицы габаритов:\n" + str(e))
        return {"-":"-"}
# a = split_size_table("")
# print(a)
#
# a = split_size_table("'B:fdfd'")
# print(a)

# a = split_size_table("L:500,B:430,H:855 ")
# print(a)





def splitter(stroka = str):
    # stroka = List_cleaner(stroka)
    # print(stroka)
    X = []
    Y = []
    # если введенные точки явно откуда-то скопированы, то там не иначе как будет переход на другую строку
    if '\n' in stroka:
        spisok = stroka.split('\n')
        # если разделители такие, то запятая будет делить целое и не целое
        if '\t' in stroka or ';' in stroka:
            for each in spisok:
                # print(each)
                if ";" in each:
                    X.append(each.split(";")[0])
                    Y.append(each.split(";")[1])
                elif "\t" in each:
                    X.append(each.split("\t")[0])
                    Y.append(each.split("\t")[1])
            if "," in X[0]:
                X = [float(re.sub(r',', '.', element)) for element in X]
                Y = [float(re.sub(r',', '.', element)) for element in Y]
        # Если есть одновременно и запятая и точка. То запятая делит X, Y
        elif ',' in stroka and '.' in stroka:
            for each in spisok:
                try:
                    X.append(float(each.split(",")[0]))
                    Y.append(float(each.split(",")[1]))
                except:
                    pass
        elif ',' in stroka and not '.' in stroka:
            for each in spisok:
                try:
                    # print(each)
                    # print(each.split(","))
                    # X.append(float(each.split(",")[0]))
                    Y.append(float(re.sub(r',', ".", each, flags=re.DOTALL)))
                except:
                    pass
    elif ',' in stroka  and '\n' not in stroka:
        # if "!" in stroka:
        #     xy = stroka.split("!")
        #     xspisok = xy[0].split(',')
        #     for each in xspisok:
        #         try:
        #             X.append(float(each))
        #         except:
        #             pass
        #     yspisok = xy[1].split(',')
        #     for each in yspisok:
        #         try:
        #             Y.append(float(each))
        #         except:
        #             pass
        #     pass
        # else:
        spisok = stroka.split(',')
        for each in spisok:

            try:
                Y.append(float(each))
            except:
                pass
    # Если была введена жесть, то она выкидывает те пары значений, которые не цифры
    if len(X)>=1 and type(X[0]) == str:
        # while str in X:
        indexator = 0
        while indexator<len(X) or indexator<len(Y):
            try:
                X[indexator] = float(re.sub(r',', '.', X[indexator], flags=re.DOTALL))
                Y[indexator] = float(re.sub(r',', '.', Y[indexator], flags=re.DOTALL))
                indexator+=1
            except:
                X.pop(indexator)
                Y.pop(indexator)
    try:
        promezhutok = ast.literal_eval(stroka)
        if type(promezhutok) != tuple:
            if len(promezhutok) == 2:
                X = promezhutok[0]
                Y = promezhutok[1]
            else:
                Y = promezhutok
        return X, Y
    except:
        pass
    return X, Y

# splitter разделяет все вот эти варианты на два списка X, Y если они состоят из двух или только Y если там только он.


def splitterabstracted(stroka = str):
    # stroka = List_cleaner(stroka)
    # print(stroka)
    X = []
    Y = []
    # если введенные точки явно откуда-то скопированы, то там не иначе как будет переход на другую строку
    if "!" in stroka:
        xy = stroka.split("!")
        speeds = []
        for pair in xy:
            # print(pair)
            speeds.append(splitter(stroka=pair))
        return speeds
    else:
        return [splitter(stroka=stroka)]




var1 = '0,694915254\t76,45850759\n22,6313009\t76,59432093\n46,53290777\t76,32687651\n80,39929562\t76,03081664\n111,3178516\t76,33964341\n151,1631081\t76,02641426\n196,9872331\t75,69601585\n233,8569227\t75,59013867\n263,7373982\t75,30552498\n293,5762712\t74,42460929\n339,3726612\t73,69667621\n363,2049307\t72,43539511\n395,0367599\t71,54875633\n422,8688092\t70,47479639\n444,7219899\t69,41800572\n469,5646049\t68,35263042\n493,3968743\t67,09134933\n515,250055\t66,03455866\n547,0125468\t64,1540832\n574,7752586\t62,08628659\n595,6042263\t60,6348228\n618,4400176\t59,37640326\n643,1855602\t56,91965661\n667,9588378\t54,86044464\n688,7323355\t52,61391151\n716,4118424\t49,3535109\n744,0774818\t45,89434295\n767,7572089\t42,44662118\n798,2458728\t36,59366058\n820,9013867\t32,75126568\n828,7206692\t30,54193264\n'
var2 = '0,6949152542372588; 76,45850759410081\n22,631300902487325; 76,59432093330398\n46,53290777019589; 76,32687651331719\n80,39929561963461; 76,03081664098613\n111,31785163988556; 76,33964340744001\n151,16310807836234; 76,02641426370239\n196,9872331058772; 75,69601584855822\n233,85692273827877; 75,59013867488443\n263,7373981950253; 75,30552498349108\n293,57627118644075; 74,42460928901606\n339,3726612370681; 73,69667620515077\n363,2049306625579; 72,43539511336121\n395,0367598503193; 71,54875632841734\n422,86880915694485; 70,47479639005061\n444,72198987453237; 69,41800572309046\n469,5646048866389; 68,35263042042702\n493,3968743121286; 67,09134932863745\n515,2500550297161; 66,0345586616773\n547,0125467752588; 64,15408320493066\n574,7752586396655; 62,08628659476116\n595,6042262821926; 60,634822804314325\n618,4400176095093; 59,37640325775919\n643,1855602025095; 56,91965661457185\n667,9588377723973; 54,860444640105655\n688,7323354611492; 52,61391151221659\n716,4118423948934; 49,35351089588376\n744,0774818401939; 45,89434294519039\n767,7572088928023; 42,44662117543473\n798,2458727712967; 36,593660576711414\n820,9013867488446; 32,75126568346906\n828,7206691613472; 30,541932643627547\n'
var3 = '22,96\n22,92\n22,93\n22,92\n22,80\n22,51\n22,02\n21,28\n20,27\n20,08\n18,98\n17,40\n15,55\n13,45\n11,14\n8,65\n'
var4 = '2.2,96\n22,92\n22,93\n22,92\n22,80\n22,51\n22,02\n21,28\n20,27\n20,08\n18,98\n17,40\n15,55\n13,45\n11,14\n8,65\n'
var5 = '700,100,130'
var6 = '7.7,100,130'
st = 'Q\tH\nm³/h\tm\n0,00\t22,96\n11,77\t22,92\n23,54\t22,93\n35,31\t22,92\n47,07\t22,80\n58,84\t22,51\n70,61\t22,02\n82,38\t21,28\n94,15\t20,27\n96,04\t20,08\n105,92\t18,98\n117,69\t17,40\n129,45\t15,55\n141,22\t13,45\n152,99\t11,14\n164,76\t8,65\n'
st2 = '[0.0, 11.77, 23.54, 35.31, 47.07, 58.84, 70.61, 82.38, 94.15, 96.04, 105.92, 117.69, 129.45, 141.22, 152.99, 164.76]'
st3 = "[[0.0, 11.77, 23.54, 35.31], [22.96, 22.92, 22.93, 22.92]]"
st4 = "[22.96, 22.92, 22.93, 22.92]"
st5 = '1.2, 4 ! 7.7, 12'
st6 = '1.2, 4 ! 7.7, 12 ! 2.2, 5'
st7 = 'Q\tH\nm³/h\tm\n30\t19,96\n101,77\t16,92\n124,54\t9,93\n'+"!"+'Q\tH\nm³/h\tm\n27\t15,96\n97,77\t12,92\n120,54\t5,93\n'+"!"+'Q\tH\nm³/h\tm\n36\t21,96\n120,77\t19,92\n132,54\t11,93\n'

st8 = "0.0, 11.77, 23.54, 35.31/22.96, 22.92, 22.93, 22.92!0.0, 11.77, 23.54, 35.31/22.96, 22.92, 22.93, 22.92"

st9 = "[[0.0, 11.77, 23.54, 35.31], [22.96, 22.92, 22.93, 22.92]]![[0.0, 11.77, 23.54, 35.31], [22.96, 22.92, 22.93, 22.92]]"


print()
print()
print()
print()
print(splitterabstracted(var1))
print(splitterabstracted(var2))
print(splitterabstracted(var3))
print(splitterabstracted(var4))
print(splitterabstracted(var5))
print(splitterabstracted(var6))
print(splitterabstracted(st))
print(splitterabstracted(st2))
print(splitterabstracted(st3))
print(splitterabstracted(st4))
print(splitterabstracted(st5))
print(splitterabstracted(st6))
print(splitterabstracted(st7))
print(splitterabstracted(st8))
print(splitterabstracted(st9))



# print(ast.literal_eval("[([30.0, 101.77, 124.54], [19.96, 16.92, 9.93]), ([27.0, 97.77, 120.54], [15.96, 12.92, 5.93]), ([36.0, 120.77, 132.54], [21.96, 19.92, 11.93])]")[0])