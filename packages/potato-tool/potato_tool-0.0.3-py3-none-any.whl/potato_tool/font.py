#!/usr/bin/python
# -*- coding:utf-8
import os
import sys
import re
import string
import terminal
import console
import wcwidth

def p(*args, **kwargs):
    print(*args, **kwargs)

def red(text):
    return terminal.bold(terminal.red(text))

def redP(*args, **kwargs):
    text = ' '.join(map(str, args))
    p(red(text), **kwargs)

def green(text):
    return terminal.green(text)

def greenP(*args, **kwargs):
    text = ' '.join(map(str, args))
    p(green(text), **kwargs)

def blue(text):
    return terminal.bold(terminal.blue(text))

def blueP(*args, **kwargs):
    text = ' '.join(map(str, args))
    p(blue(text), **kwargs)

def magenta(text):
    return terminal.magenta(text)

def magentaP(*args, **kwargs):
    text = ' '.join(map(str, args))
    p(magenta(text), **kwargs)

def yellow(text):
    return terminal.yellow(text)

def yellowP(*args, **kwargs):
    text = ' '.join(map(str, args))
    p(yellow(text), **kwargs)

def cyan(text):
    return terminal.cyan(text)

def cyanP(*args, **kwargs):
    text = ' '.join(map(str, args))
    p(cyan(text), **kwargs)

def bold(text):#高亮
    return terminal.bold(text)

def boldP(*args, **kwargs):
    text = ' '.join(map(str, args))
    p(bold(text), **kwargs)

def Processing():
    return terminal.magenta(r"[Processing] ")

def ProcessingP(*args, **kwargs):
    text = ' '.join(map(str, args))
    p(Processing(text), **kwargs)

def Information():
    return terminal.cyan(r"[Information] ")

def InformationP(*args, **kwargs):
    text = ' '.join(map(str, args))
    p(Information(text), **kwargs)

def Detected():
    return terminal.bold(terminal.blue(r"[Detected] "))

def DetectedP(*args, **kwargs):
    text = ' '.join(map(str, args))
    p(Detected(text), **kwargs)

def Result():
    return terminal.bold(terminal.green(r"[Result] "))

def ResultP(*args, **kwargs):
    text = ' '.join(map(str, args))
    p(Result(text), **kwargs)

def Error():
    return terminal.bold(terminal.red(r"[Error] "))

def ErrorP(*args, **kwargs):
    text = ' '.join(map(str, args))
    p(Error(text), **kwargs)

def Input(startStr='Potato', *num):
    startStr='Potato' if startStr=="" else startStr
    if(num and num[0]!= 1):
        data = r"<" + startStr + r">- "
    else:
        data = r"<" + startStr + r">$ "
    return terminal.bold(terminal.yellow(data))

def InputP(*args, **kwargs):
    text = ' '.join(map(str, args))
    p(Input(text), **kwargs)

#实现回车换行，而不是结束
def Input_lines(startStr='Potato', showHead=True):
    result = ""
    num = 0
    startStr='Potato' if startStr=="" else startStr
    while True:
        num = num + 1
        data = str(input(Input(startStr, num))) if showHead else str(input())
        if data == '':
            if(num==1):
                p(Error()+'首行不能为空，请重新输入！\n')
                result = ""
                num = 0
                continue
            return result
        result+= data+"\n"#换行


#格式化输出
def printF(strData, lenMax, placeHolder=" ", justify="center"):
    strData = str(strData)
    lenChina = 0
    for i in strData:
        lenChina+=1 if i not in string.printable else 0
    return strData.center(lenMax-lenChina,placeHolder) if justify=="center" else strData.ljust(lenMax-lenChina,placeHolder) if justify=="left" else strData.rjust(lenMax-lenChina,placeHolder)
def pF(strData, lenMax, placeHolder=" ", justify="center", **kwargs):
    strData = str(strData)
    lenChina = 0
    for i in strData:
        lenChina+=1 if i not in string.printable else 0
    result = strData.center(lenMax-lenChina,placeHolder) if justify=="center" else strData.ljust(lenMax-lenChina,placeHolder) if justify=="left" else strData.rjust(lenMax-lenChina,placeHolder)
    p(result, **kwargs)

# 适合实时获取数据，实时打印表格
# printT( [8,13,13,10] ,"top")
# printT( [["ip",8],["域名",13,"left"],["权重",13,"center"],["编号",10]])
# printT( [8,13,13,10] ,"middle")
# printT( [["ip",8],["域名",13,"left"],["权重",13],["编号",10]],type="body")
# printT( [8,13,13,10] ,"bottom")
#tableStyle、fontStyle 分别控制字体和表格颜色
def printT(dataList,type="body",getStr=False,tableStyle="red",fontStyle=""):

    def table(str):
        if tableStyle == "red":
            return red(str)
        elif tableStyle == "green":
            return green(str)
        elif tableStyle == "magenta":
            return magenta(str)
        elif tableStyle == "blue":
            return blue(str)
        elif tableStyle == "yellow":
            return yellow(str)
        elif tableStyle == "cyan":
            return cyan(str)
        elif tableStyle == "bold":
            return bold(str)
        else:
            return str

    def font(str):
            if fontStyle == "red":
                return red(str)
            elif fontStyle == "green":
                return green(str)
            elif fontStyle == "magenta":
                return magenta(str)
            elif fontStyle == "blue":
                return blue(str)
            elif fontStyle == "yellow":
                return yellow(str)
            elif fontStyle == "cyan":
                return cyan(str)
            elif fontStyle == "bold":
                return bold(str)
            else:
                return str

    try:
        str=""
        if type == "top":
            str = table("┌")
            for index, data in enumerate(dataList):
                str += table("─" * data)
                str += table("┬") if index != len(dataList)-1 else table("┐")
        elif type == "bottom":
            str = table("└")
            for index, data in enumerate(dataList):
                str += table("─" * data)
                str += table("┴") if index != len(dataList)-1 else table("┘")
        elif type == "middle":
            str = table("├")
            for index, data in enumerate(dataList):
                str += table("─" * data)
                str += table("┼") if index != len(dataList)-1 else table("┤")
        else:
            str = table("│")
            for data in dataList:
                justify = "center" if len(data)==2 else data[2]
                str += f"{font(printF(data[0], data[1], justify=justify))}{table('│')}"
        if getStr:
            return str
        else:
            p(str)
    except Exception as e:
        p(f"\033[31m[Error] {e}\r\n")
        p('正确使用方法：')
        p('    printT( [8,13,13,10] ,"top")')
        p('    printT( [["ip",8],["域名",13,"left"],["权重",13],["编号",10]])')
        p('    printT( [8,13,13,10] ,"middle")')
        p('    printT( [["ip",8],["域名",13,"left"],["权重",13],["编号",10]])')
        p('    printT( [8,13,13,10] ,"bottom")\033[0m')
def pT(dataList, type="body", getStr=False, tableStyle="red", fontStyle=""):
    printT(dataList, type, getStr, tableStyle, fontStyle)

# 适合获取数据完毕后，再打印表格
# listPT([["ip","domain","icp","id"],["ip","域名","备案","编号"]])
#tableStyle、fontStyle 分别控制字体和表格颜色
def listPT(dataList, justify=None, getStr=False, tableStyle="red", fontStyle=""):
    try:

        lenMaxList = get_column_widths(dataList)
        printT( lenMaxList ,"top", getStr=getStr, tableStyle=tableStyle, fontStyle=fontStyle)

        for index, row in enumerate(dataList):
            if justify is None:
                justify = ["center"] * len(row)
            newPTlist = [[x, y, z] for x, y, z in zip(row, lenMaxList, justify)]
            printT( newPTlist ,"body", getStr=getStr, tableStyle=tableStyle, fontStyle=fontStyle)
            if index != len(dataList) - 1:
                printT( lenMaxList ,"middle", getStr=getStr, tableStyle=tableStyle, fontStyle=fontStyle)

        printT( lenMaxList ,"bottom", getStr=getStr, tableStyle=tableStyle, fontStyle=fontStyle)

    except Exception as e:
        p(f"\033[31m[Error] {e}\r\n")
        p('listPT(dataList, justify=["center","center","center","center"], getStr=False, tableStyle="red", fontStyle="")\n')
        p('正确使用方法：')
        p('    listPT([["ip","domain","icp","id"],["ip","域名","备案","编号"]])')



# 获取二维数组最大宽度
def get_column_widths(array_2d):
    num_rows = len(array_2d)
    num_cols = len(array_2d[0]) if num_rows > 0 else 0

    column_widths = [0] * num_cols

    for col in range(num_cols):
        for row in range(num_rows):
            element = array_2d[row][col]
            element_width = wcwidth.wcswidth(str(element))
            column_widths[col] = max(column_widths[col], element_width)

    return column_widths