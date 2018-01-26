'''
excel表格相关操作#1       
F:/test 目录下有两张表格A,B,分别是几个基站的3G流量和4G流量
要求把两张表按基站名称合并，生成一张基站3/4G流量表
格式如下’’基站名称‘，’3g流量‘，’3g用户数‘，’4g流量‘，’4g用户数’，
'''
import pandas as pd      #导入pandas库

A=r'f:\test\A.xls'
B=r'f:\test\B.xls'
df1 = pd.read_excel(A,encoding='utf-8')    #导入一张excel97,2003表格赋值给df1
df2 = pd.read_excel(B,encoding='utf-8')    #导入一张excel97,2003表格赋值给df2
#用来打开excel的数据结构pandas.DataFrame，所以在命名变量的时候建议使用df，增加代码可读性

df3=pd.merge(df1,df2,how='left',on='基站名称')
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
df4.to_excel(r'f:\test\1.xls')    #将df4导出一张xls表格

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
df2.loc[:,'4G流量(Gb)']   #选取表1的基站名称列
#这种方法缺点是写代码要写中文的列名不方便
#当表格比较大的时候，需要一列一列效率很低

#第2种方法使用.iloc
#iloc格式同loc，但是可以写列号，不用写列名
df3=df1.iloc[:,0]   #选取表1的第一列，注意变量浏览器里的a，实际是两列，第一列是序号
df4=df1.iloc[0]   #选取表1的第一行，同样注意看变量浏览器b也有两行，第一行是行名称。


#第3种方法使用.at（十字交叉切片，最后会返回十字交叉点的单元格的值）
#下面使用铁塔维护费的表格来演示纵横切片
df5=pd.read_excel(r'f:\test\weihu.xls',encoding='utf-8')    #导入铁塔维护费表格赋值给df1
a=df5.at[0,'自建砖混机房']    #对第1行，'自建砖混机房'列进行切片，注意行号是从0开始编，第一行就是0行
b=df5.at[4,'自建彩钢板机房']    #对第1行，'自建砖混机房'列进行切片，注意行号是从0开始编，第一行就是0行

 #如果要根据行的关键字进行切片，需要重新设置行索引，默认行索引都是0,1,2，3的数字
df5=df5.set_index('运营商区县')   #将'运营商区县'一列设置为行索引
c=df5.at['马龙县','一体化机柜']    #下面就可以用关键字进行切片了，
d=df5.at['宣威市','一体化机房']    #下面就可以用关键字进行切片了，

#第4种方法使用.iat（纵横切片，同第三种，但是切片的关键字只能使用数字序号）
#下面使用铁塔维护费的表格来演示纵横切片
df6=pd.read_excel(r'f:\test\weihu.xls',encoding='utf-8')    #导入一张excel97,2003表格赋值给df1

e=df6.iat[0,0]  #第1行第1列十字切片，得到第一个县名’富源县‘
f=df6.iat[1,1]  #第2行第2列十字切片，得到的是麒麟区,自建砖混机房的价格。
g=df6.iat[3,2]  #第4行第3列十字切片，得到的是会泽县,自建框架机房的价格。

'''
excel表格相关操作#3 
在表格中插入列:
'''
col_name = df.columns.tolist()  #获取df的列名，转换为list，赋值给col_name
col_name.insert(col_name.index('D'),'B')   # 在 col_name的‘B’ 列前面插入'D'
df.reindex(columns=col_name)  #重排df列的顺序 






