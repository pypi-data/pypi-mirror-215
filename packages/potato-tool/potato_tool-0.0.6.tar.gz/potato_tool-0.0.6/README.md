# 辅助函数
- 打印 (return void)
  - `p(Str)`


- 清理屏幕输出 (兼容不同OS) (return void)
  - `clear()`


# 字体效果
- 红色
   - `red(Str)` (return str)
   - `redP(Str)` (return void)


- 绿色
  - `green(Str)` (return str)
  - `greenP(Str)` (return void)


- 蓝色 
  - `blue(Str)` (return str)
  - `blueP(Str)` (return void)


- 黄色 
  - `yellow(Str)` (return str)
  - `yellowP(Str)` (return void)


- 青色 
  - `cyan(Str)` (return str)
  - `cyanP(Str)` (return void)


- 紫红 
  - `magenta(Str)` (return str)
  - `magentaP(Str)` (return void)


- 加粗 
  - `bold(Str)` (return str)
  - `boldP(Str)` (return void)


# 输出前置符打印
- 紫红\[Processing\] 
  - `Processing()` (return str)
  - `ProcessingP()` (return void)


- 青色\[Information\] 
  - `Information()` (return str)
  - `InformationP()` (return void)


- 加粗\[Detected\] 
  - `Detected()` (return str)
  - `DetectedP()` (return void)

- 绿色\[Result\] 
  - `Result()` (return str)
  - `ResultP()` (return void)


- 红色\[Error\] 
  - `Error()` (return str)
  - `ErrorP()` (return void)


# 输入前置符打印
- 单行输入 （ Input(startStr='Potato') ）
  - `Input()` （黄色\<Potato\>$ ） (return str)
  - `Input(Str)` （黄色\<Str\>$ ） (return str)
  - `InputP()` （黄色\<Potato\>$ ） (return void)
  - `InputP(Str)` （黄色\<Str\>$ ） (return void)


- 多行输入 （ Input_lines(startStr='Potato', showHead=True) ）
  - `Input_lines()` （黄色\<Potato\>- ,可传参showHead=True(默)/False控制是否固定头部）
  - `Input_lines(Str)` （黄色\<Str\>- ,可传参showHead=True(默)/False控制是否固定头部）


# 格式化输出
- 对字符串宽度(lenMax)、填充字符(placeHolder默认空格)、对齐方式(justify默认居中)进行设置，来格式化输出
  - `printF(strData, lenMax, placeHolder=" ", justify="center")` (return str)
  - `pF(strData, lenMax, placeHolder=" ", justify="center")` (return void)


# 表格化输出
- tableStyle、fontStyle 分别控制字体和表格颜色
- getStr控制return void/str
- **实时**获取数据，**实时**打印表格
  - `printT(dataList,type="body",getStr=False,tableStyle="red",fontStyle="")` (return void)
  - `pT(dataList,type="body",getStr=False,tableStyle="red",fontStyle="")` (return void)

  - 举例：
    - `printT( [8,13,13,10] ,"top")`
    - `printT( [["ip",8],["domin",13,"left"],["icp",13,"center"],["id",10]])`
    - `printT( [8,13,13,10] ,"middle")`
    - `printT( [["ip",8],["域名",13,"left"],["备案",13],["编号",10]],type="body")`
    - `printT( [8,13,13,10] ,"bottom")`

  - 输出：

<div style="margin-left: 70px">

|  ip   | domain | icp | id |
|  :----:  | :----:  | :----: | :----: |
| ip  | 域名 | 备案 | 编号 |

</div>


- **获取数据完毕后**，再打印表格
  - `listPT(dataList, justify=None, getStr=False, tableStyle="red", fontStyle="")` (return void)

  - 举例：
    - `listPT([["ip","domain","icp","id"],["ip","域名","备案","编号"]])`
    
  - 输出：

<div style="margin-left: 70px">

|  ip   | domain | icp | id |
|  :----:  | :----:  | :----: | :----: |
| ip  | 域名 | 备案 | 编号 |

</div>


# logo输出
- `logo_1(ScriptName="potato",Author="potato", QQemil="2431111111", Type="Penetration", Version="0.2.4")`
- `logo_2()`