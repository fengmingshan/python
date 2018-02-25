# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 17:28:03 2018
用几个小例子帮助理解python中的类
@author: Administrator
"""
#类就是一些：属性+方法（函数） 的集合
#定义类可以简化代码，具有相同属性或者方法（函数），只需要定义一个类，简化代码

class Animal(object):  # 定义类：动物，python3中所有类都是继承于object基类的，这是个固定的格式
   def __init__(self, name, age):   #定义类初始化的方法
       self.name = name     #定义类类的其中一条属性并初始化
       self.age = age   #定义类的其中一条属性并初始化

   def call(self): # 定义类的其他方法/函数：call，self表示对象自己这也是一个固定格式，调用函数的时候不用传入self参数
       print(self.name,'会','叫') 

#类有很多属性，依次来看看：
Animal.__name__    #返回类的名称，类的属性调用：.+属性的名称带'__'这种都是类默认的属性
Animal.__dict__    #返回类所有的属性名称
Animal.__doc__     #返回类的返回文档字符串
Animal.__bases__    #返回类的父类
Animal.__module__   #返回类所在的模块，如果是我们自己定义的类，返回的是'__main__',如果是import的类，则返回它所在的模块
Animal.__class__    #返回所在的类


#类的继承

#现在我们需要定义一个Animal的子类:Cat猫类,它继承于Animal，但猫类比动物类多一个sex属性。
class Cat(Animal):  #定义类：猫，它的父类是Animal，即：继承了Animal类所有的属性和方法
   def __init__(self,name,age,sex):
       super(Cat, self).__init__(name,age)  # 要用 super(Cat, self)初始化父类Animal的name和age属性
       self.sex=sex     #自己新增的属性sex单独定义

if __name__ == '__main__':  # 当类被引用时下面代码不会执行，只有在它位于自己的模块才会执行，一般用于调试
   c = Cat('小花', 2, '男')  #  创建对象/实例c,他属于Cat类，继承了父类Animal的属性
   print(c.name,c.age)
   c.call()  # 输出 喵喵 会叫 ，Cat继承了父类Animal的方法

#子类方法的重构
class Cat(Animal):
   def __init__(self, name, age, sex):
       super(Cat, self).__init__(name,age)
       self.sex = sex

   def call(self):  #重新定义Cat类的方法call,加入了'喵喵叫'
       print(self.name,'会','喵喵叫')

if __name__ == '__main__':
   c = Cat('喵喵', 2, '男')
   c.call()  # 输出：喵喵 会“喵喵”叫

#子类与父类的关系
#判断对象之间的关系，我们可以通过  isinstance(变量,类型)  来进行判断：
A= Animal('旺财',3)
C = Cat('咪咪',2,'女')

print('"A" IS Animal?', isinstance(A, Animal))
print('"A" IS Cat?', isinstance(A, Cat))
print('"C" IS Animal?', isinstance(C, Animal))
print('"C" IS Cat?', isinstance(C, Cat))

#函数 isinstance() 不止可以用在我们自定义的类，也可以判断一个变量的类型，如判断数据类型是否为 int、str、list、dict 等
print(isinstance(100, int))     #
print(isinstance('abc', int))
print(isinstance(100, str))
print(isinstance('abc', str))

#python中类方法的多态
#再定义一个狗类：Dog
class Dog(Animal):
   def __init__(self, name, age, sex):
       super(Dog, self).__init__(name, age)
       self.sex = sex
   def call(self):
       print(self.name,'会','汪汪叫')
       
#这个时候函数call()就是多态，可以是Animal的，也可以是Cat的，也可以是Dog的
#我们定义一个do函数，接收一个变量 ‘all’,并运行一个call()函数,如下：
def do(all):
   all.call()

A = Animal('小黑',4)
C = Cat('喵喵', 2, '男')
D = Dog('旺财', 5, '女')
for x in (A,C,D):
   do(x)   
#当对象不同的时候,同一个call()函数有不同的效果
A.call()
C.call()
D.call()

#在继承中基类的构造方法（__init__()方法）不会被自动调用，它需要在其派生类的构造方法中亲自专门调用。
#在调用基类的方法时，需要加上基类的类名前缀，且需要带上self参数变量。而在类中调用普通函数时并不需要带上self参数。
#Python总是先在本类中查找调用的方法，找不到才去基类中找。










