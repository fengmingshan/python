from dateutil.parser import parse  # 导入模块
from dateutil.rrule import *

# parse 任意格式字符串转datetime格式（可以用时间日期的英文单词，可以用横线、逗号、空格等做分隔）
date1 = parse('November 1')  # 默认年份是系统年份
print(date1)

date2 = parse('11/01')
print(date2)

date3= parse('20181101165959')
print(date3)

date4 = parse('2018-11-01')
print(date4)

date5 = parse('16:59:59')
print(date2)

date6 = parse('2020-10-1 10:30')
print(date6)

# fuzzy开启模糊匹配，过滤掉无法识别的时间日期字符
date7 = parse("this is the wonderful moment 16:59:59,I feel good",fuzzy=True)
print(date7)

# rrule 处理时间间隔的函数
# 函数参数
# rrule(self, freq, dtstart=None,
#      interval=1, wkst=None, count=None, 
#      until=None, bysetpos=None, bymonth=None, 
#      bymonthday=None, byyearday=None, byeaster=None, 
#      byweekno=None, byweekday=None, byhour=None, 
#      byminute=None, bysecond=None, cache=False)

# freq:可以理解为单位。可以是 YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY, SECONDLY。即年月日周时分秒。
# dtstart,until:是开始和结束时间。
# wkst:周开始时间。　
# interval:间隔。　
# count:指定生成多少个。
# byxxx:指定匹配的周期。比如byweekday=(MO,TU)则只有周一周二的匹配。byweekday可以指定MO,TU,WE,TH,FR,SA,SU。即周一到周日。

# 生成区间内的所有日期
print(list(rrule(DAILY,dtstart=parse('2013-08-01'),until=parse('2013-08-07'))))

# 日期间隔为3
print(list(rrule(DAILY,interval=3,dtstart=parse('2013-08-01'),until=parse('2013-08-07'))))

# 只生成前三个
print(list(rrule(DAILY,count=3,dtstart=parse('2013-08-01'),until=parse('2013-08-07'))))

# 只生成前周一和周二的
print(list(rrule(DAILY,byweekday=(MO,TU),dtstart=parse('2013-08-01'),until=parse('2013-08-07'))))

# 以月为单位生成
print(list(rrule(MONTHLY,dtstart=parse('2013-05-19'),until=parse('2013-08-20'))))


