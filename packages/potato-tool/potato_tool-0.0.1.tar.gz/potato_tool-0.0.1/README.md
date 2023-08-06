# 字体效果
- 红色
   - `red(Str)`


- 绿色
  - `green(Str)`


- 蓝色 
  - `blue(Str)`


- 黄色 
  - `yellow(Str)`


- 青色 
  - `cyan(Str)`


- 紫红 
  - `magenta(Str)`


- 加粗 
  - `bold(Str)`


# 输出前置符打印
- 紫红\[Processing\] 
  - `Processing()`


- 青色\[Information\] 
  - `Information()`


- 加粗\[Detected\] 
  - `Detected()`

- 绿色\[Result\] 
  - `Result()`


- 红色\[Error\] 
  - `Error()`


# 输入前置符打印
- 单行输入 （ Input(startStr='Potato') ）
  - `Input()` （黄色\<Potato\>$ ）
  - `Input(Str)` （黄色\<Str\>$ ）


- 多行输入 （ Input_lines(startStr='Potato', showHead=True) ）
  - `Input_lines()` （黄色\<Potato\>- ,可传参showHead=True(默)/False控制是否固定头部）
  - `Input_lines(Str)` （黄色\<Str\>- ,可传参showHead=True(默)/False控制是否固定头部）


# 格式化输出
- 对字符串宽度(lenMax)、填充字符(placeHolder默认空格)、对齐方式(justify默认居中)进行设置，来格式化输出
  - `printF(strData, lenMax, placeHolder=" ", justify="center")`


# 表格化输出
- tableStyle、fontStyle 分别控制字体和表格颜色  
  - `printT(dataList,type="body",getStr=False,tableStyle="red",fontStyle="")`


  - 举例：
    - `printT( [8,13,13,10] ,"top")`
    - `printT( [["ip",8],["domin",13,"left"],["icp",13,"center"],["id",10]])`
    - `printT( [8,13,13,10] ,"middle")`
    - `printT( [["ip",8],["域名",13,"left"],["备案",13],["编号",10]],type="body")`
    - `printT( [8,13,13,10] ,"bottom")`


  - 输出：

<div style="margin-left: 50px">

|  ip   | domain | icp | id |
|  :----:  | :----:  | :----: | :----: |
| ip  | 域名 | 备案 | 编号 |

</div>