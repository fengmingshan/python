'''
excel表格相关操作#1       
F:/test 目录下有两张表格A,B,分别是几个基站的3G流量和4G流量
要求把两张表按基站名称合并，生成一张基站3/4G流量表
格式如下’’基站名称‘，’3g流量‘，’3g用户数‘，’4g流量‘，’4g用户数’，
'''
import pandas as pd      #导入pandas库

df1 = pd.read_excel(r'f:\test\A.xls',encoding='utf-8')    #导入一张excel97,2003表格赋值给df1
df2= pd.read_excel(r'f:\test\B.xls',encoding='utf-8')    #导入一张excel97,2003表格赋值给df2
#用来打开excel的数据结构pandas.DataFrame，所以在命名变量的时候建议使用df，增加代码可读性

df3=pd.merge(df1,df2,how='right',on='基站名称')
#定义一个新的DataFrame df3 来对df1 和df2 进行合并，合并的关键字是基站名称
#这里的3个参数how是合并方法（right/left/inner不懂的同学复习下数据库的ppt ）on是合并的关键字。

df4=pd.DataFrame(columns=['基站名称','3g流量','3g用户数','4g流量','4g用户数'])
#定义一个空的DataFrame df4用来装最终的结果，列标按照题目要求设置

df4['基站名称']=df3['基站名称']
df4['3g流量']=df3['3G流量（GB）']
df4['3g用户数']=df3['3G在线用户数']
df4['4g流量']=df3['4G流量(Gb)']
df4['4g用户数']=df3['4G在线用户数']

#需要的表格已经完成，可以输出到表格了
df4 .to_excel(r'f:\test\1.xls')    #将df4导出一张xls表格

#本课思考题：如果我需要一张报表，格式如下’’基站名称‘，’总数据流量‘，’4g渗透比‘。要求输出到2.xls
#总数据流量=3g流量+4g流量，4g渗透比='4G在线用户数'/'3G在线用户数'
#请用上面的方法自己写一段代码实现

'''
excel表格相关操作#2  
引用表格元素的几种方法:
'''
#上一课的练习题答案：
import pandas as pd      #导入pandas库

df1 = pd.read_excel(r'f:\test\A.xls',encoding='utf-8')    #导入一张excel97,2003表格赋值给df1
df2= pd.read_excel(r'f:\test\B.xls',encoding='utf-8')    #导入一张excel97,2003表格赋值给df2

df3=pd.DataFrame(columns=['基站名称','总数据流量','4g渗透比'])
df3['基站名称']=df1['基站名称']
df3['总数据流量']=df1['3G流量（GB）']+df2['4G流量(Gb)']
df3['4g渗透比']=df2['4G在线用户数']/df1['3G在线用户数']

df3.to_excel(r'f:\test\2.xls')    #将df4导出一张xls表格

#以下是今天的内容：
#直接输出到表格：df3.to_excel(r'f:\test\2.xls')，这种方法的缺点是每次写入数据都会将原表覆盖掉
#如果需要写入多页，最终只能保留一页。所以需要换一种方法写：
writer = pd.ExcelWriter(r'f:\test\2.xls')        #定义一个对象writer，用于写入excel
df1.to_excel(writer, 'sheet1')                       #将df1写入到sheet1
df2.to_excel(writer, 'sheet2')                       #将df2写入到sheet2
writer.save()                                                     #保存writer对象

#选取DataFrame中的行、列
df1 = pd.read_excel(r'f:\test\A.xls',encoding='utf-8')    #导入一张excel97,2003表格赋值给df1
df2= pd.read_excel(r'f:\test\B.xls',encoding='utf-8')    #导入一张excel97,2003表格赋值给df2

#第1种方法使用.loc
#注意loc[]方括号里面有两个字段，第一个是行号，第二个是列名。
#选择行时第二个字段可以不写，但是选择列时第一个字段必须写成loc[:,'xx']表示选所有行
df1.loc[0:2]    #选取表1的1-3行
df1.loc[:,'基站名称']   #选取表1的基站名称列
df2.loc[:,'4G流量(Gb)']   #选取表1的基站名称列
#这种方法缺点是写代码要写中文的列名不方便
#当表格比较大的时候，需要一列一列效率很低

#第2种方法使用.iloc
#iloc格式同loc，但是可以写列号，不用写列名
a=df1.iloc[:,0]   #选取表1的第一列，注意变量浏览器里的a，实际是两列，第一列是序号
b=df1.iloc[0]   #选取表1的第一行，同样注意看变量浏览器b也有两行，第一行是行名称。




