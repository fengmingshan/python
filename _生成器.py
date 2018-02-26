# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 22:38:31 2018
python生成器：当Python 函数不用return 返回值，用yield关键字的时候，函数的返回值为生成器对象。

1.语法上和函数类似：生成器函数和常规函数几乎是一样的。它们都是使用def语句进行定义。
差别在于，生成器使用yield语句返回一个值，而常规函数使用return语句返回一个值。
2.自动实现迭代器协议：对于生成器，Python会自动实现迭代器协议，以便应用到迭代背景中（如for循环，sum函数）。
由于生成器自动实现了迭代器协议，所以，我们可以调用它的next方法，并且，在没有值可以返回的时候，生成器自动产生StopIteration
3异常状态挂起：生成器使用yield语句返回一个值。yield语句挂起该生成器函数的状态，保留足够的信息，以便之后从它离开的地方继续执行

@author: Administrator
"""
#定义一个生成器的例子：
def gensquares(N):
    for i in range(N):
        yield i ** 2

for item in gensquares(5):
    print (item,)

#如果用普通函数实现需要构造list，多谢2行代码。
def gensquares(N):
    res = []
    for i in range(N):
        res.append(i*i)
    return res

for item in gensquares(5):
    print item,

squares = [x**2 for x in range(5)]      # 使用列表推导，将会一次产生所有结果：
squares

squares = (x**2 for x in range(5))     # 将列表推导的中括号，替换成圆括号，就是一个生成器表达式：
squares
next(squares)       # 一次只生成一个数


squares = (x**2 for x in range(5))     # 生成器表达式：
list(squares)       # 当然你也可以通过list，一次显示所有结果

# 运用生成器进行数学运算
sum(x**2 for x in range(4))      # 可以直接对生成器进行求和等运算
sum([x ** 2 for x in range(4)])    # 效果等同于先构造列表再求和

# 生成器对生成器表达式是对内存空间的优化
sum([i for i in range(100000000)])   # list是先构造list再运算，占用很多内存资源，小心死机

# 生成器不需要像方括号的列表解析一样，一次构造出整个结果列表。生成器用一个生成一个基本不占内存，不会死机
# 生成器运行起来比列表解析式可能稍慢一些，因此他们对于非常大的结果集合运算是最优的选择
sum(i for i in range(100000000))    

for x in (x ** 2 for x in range(5)):
    print(x, end=',')

print(sorted((x ** 2 for x in range(5)), reverse=True))
[16, 9, 4, 1, 0]

print(list(x ** 2 for x in range(5)))
[0, 1, 4, 9, 16]

# 生成器对语法的简化而且逻辑更清晰：
def index_word(text):   # 定义一个函数可以找出一句话的首字母所在的位置
    result=[]
    if text:
        result.append(0)
    for index,letter in enumerate(text,1):
        if letter ==' ':
            result.append(index)
    return result

index_word('i am sorry')    # 输入一句话，返回了首字母的位置[0,2,5]

# 使用生成器再写同样的函数：
def index_word(text):   # 定义一个函数可以找出一句话的首字母所在的位置
    if text:
        yield(0)
    for index,letter in enumerate(text,1):
        if letter ==' ':
            yield(index)
            
x=index_word('i am sorry')  # 使用生成器得到的结果必须先赋值
next(x)     # 然后使用next生成结果

#理解生成器的运行流程:
# 在每次循环的时候，生成器函数都会在yield处产生一个值，并将其返回给调用者，即for循环。
#然后在yield处保存内部状态，并挂起中断退出。在下一轮迭代调用时，从yield的地方继续执行
def gen_squares(num):
    for x in range(num):
        yield x ** 2
        print('x={}'.format(x)) 
# 生成器函数计算出x的平方后就挂起退出了，但他仍然保存了此时x的值，
#而yield后的print语句会在for循环的下一轮迭代中首先调用，此时x的值即是上一轮生成器退出时保存的值。
#所以你将会看到在下面的迭代中，平方已经跳到下一个值，而print的 x=？ 还是上一轮的值。
for i in gen_squares(4):
    print('x ** 2={}'.format(i))
    print('--------------')


# 利用生成器生成可以无限取值的斐波那契函数。
def fib():
    a, b = 0, 1
    while True:
        yield b
        a, b = b, a + b
#
p = fib()
print([next(p) for i in range(10)])
# 可以利用迭代工具islice再看看效果
f = fib()
list(islice(f, 0, 10))


#利用生成器求π的值
#小提示：π=4*(1 - 1/3 + 1/5 - 1/7 + ...)
def pi_series():
    total = 0
    i = 1.0
    j = 1
    while True:
        total = total + j / i
        yield 4 * total
        i += 2
        j = j * -1
        
def main(g, n):
	for i in range(n):
		yield next(g)

if __name__ == '__main__':  #测试代码段
    print(list(main(pi_series(), 64))) 
 
    
#用生成器玩递归，捋平list 
def spread_list(lst):
    tmp = []
    for item in lst:
        if isinstance(item, list):
            tmp = spread_list(item)
            for item2 in tmp:
                yield item2
        else:
            yield item            
# 给出几个不平的list
l = [1, 2, 3, 4, 5, [6], [7, 8, [9, [10]]]]
l2 = [[3, 7, [9, 6]], [2, [3, 4], 10], 99, 28]
l3 = []
l4 = [3, 4, 5, 8]
#下面看看捋平的效果吧！
lst = spread_list(l)
print(list(lst))
lst = spread_list(l2)
print(list(lst))
lst = spread_list(l3)
print(list(lst))
lst = spread_list(l4)
print(list(lst))

# 下面来一点花式例子：
# 打印99乘法表
def table_99(max=9):
   n=1
   L=[]
   while n<=max:
      N=['{}*{}={}'.format(i,n,n*i) for i in range(1,n+1)]
      n+=1
      L.append(N) #需要新建一个list：L用来保存99表的每一行
   return L

T=table_99()
for t in T:
   print(t)
   
#用生成器重写一下：
def table_99(max=9):
   n=1
   while n<=max:
      N=['{}*{}={}'.format(i,n,n*i) for i in range(1,n+1)]
      n+=1
      yield N   #用yield来保存N的所有中间状态,代码量小了很多，是不是很简洁

T=table_99()
for t in T:
    print(t)

# 生成斐波那契序列
def fab2(max):
   a,b=0,1
   fab_list=[]
   for i in range(max):
      fab_list.append(b)
      yield fab_list
      a,b=b,a+b

for n in fab2(7):
   print(n)

#生成杨辉三角
def yanghui(max):
   N=[1]
   n=0
   while n <max:
      yield N
      N.append(0)
      N=[N[i-1]+N[i] for i in range(len(N))]
      n+=1
for t in yanghui(10):
   print(t)

#生成器的send（）方法
import time  
def func(n):  
    for i in range(0, n):  
        arg = yield i  
        print('func:', arg)  
  
f = func(10)  
while True:  
    print('main:', next(f))  
    print('main:', f.send(100))  
    print('--------------------')  #加入分割线主要 是让你看清楚执行的流程
# 程序首先调用next函数，使得生成器执行到第4行的时候，把i的值0作为next函数的返回值返回，程序输出main:0。
# 然后生成器挂起。程序往下执行send(100)函数，生成器从第四行继续执行，send函数的参数100作为yield的返回值，并赋值给arg，
# 然后得到func:100的输出。

#生成器的though（）方法

#生成器的close（）方法



        


