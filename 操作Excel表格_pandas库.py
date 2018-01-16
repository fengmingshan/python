'''
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



