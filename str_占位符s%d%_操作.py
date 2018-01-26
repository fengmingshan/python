# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 21:56:25 2018
###str的操作_占位符
占位符	说明
%s	字符串(采用str()的显示)  
%d	十进制整数  
常用的是上面两种，不常用的见本文档最后面的附录
"""


print('I like %s')  #占位符后面没有赋值，被视为普通字符串
print('I like %s' % 'yunnan') #占位符后面用%赋值， %s被替换为字符串'yunnan'

print('I like %s' % 'python') #占位符后面的%表示对占位符进行赋值，%后面的内容就是所赋的值
print('I like %s' % 'pascal')

a = '%d years' % 15
print(a)

b= 'qujing is more than %d years. %s lives in here.' % (2000, 'fms')
print (b) 
print('qujing is more than %d years. %s lives in here.' % (2000, 'fms')) #上面的两行代码也能写成1行

print ("Today's temperature is %f" % 13.875)    # %f表示浮点数，后面有多位小数
print ("Today's temperature is %.2f" % 13.875)  # %.2f表示浮点数，保留两位小数（四舍五入）
print ('Today\'s temperature is %+.2f' % 13.875) # %+.2f表示带符号的浮点数，保留两位小数（四舍五入）

###还有一种字典形式的占位符使用
print('I love %(program)s'%{'program':'python'}) 
#和下面s3的例子类似，这样写也很好读，但是在%s中间加个名字不好写.敲黑板，请注意%后面的赋值是个字典
print('I am %(count)d years old'%{'count':18})  #再练习下整数,果然是在%d之间加名字
print('my home is %(meters)f meters away'%{'meters':21.35})     #再练习下浮点数,在%f之间加名字


      
####还有一种更方便和易读的占位符运用 .format
s1 = 'I like {0}'.format('python')   
s1  #这里的集合{0}就是占位符，可以有多个占位符，分别用0,1,2表示
s2 = 'qujing is more than {0} years. {1} lives in here.'.format(2000, 'fms') 
s2  #但是当有很多个占位符的时候，这样写可读性会差一点
s3 = 'qujing is more than {year} years. {name} lives in here.'.format(year=2500, name='fms') 
s3  #这样写就好读多了，将每个集合都取了名字。读起来就很清晰


###比起 %s、%(program)s 这两种方式，还是string.format()这种形式最符合语法习惯，也最好读。





"""
附录：
占位符	说明
%r	字符串(采用repr()的显示)
%c	单个字符
%b	二进制整数
%i	十进制整数
%o	八进制整数
%x	十六进制整数
%e	指数 (基底写为e)
%E	指数 (基底写为E)
%f	浮点数
%F	浮点数，与上相同
%g	指数(e)或浮点数 (根据显示长度)
%G	指数(E)或浮点数 (根据显示长度)
@author: Administrator
"""