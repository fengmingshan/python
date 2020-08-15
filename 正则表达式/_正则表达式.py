# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 17:20:26 2018
正则表达式处理中文
@author: Administrator
"""
import re
#==============================================================================
# 正则表达式入门-1
#==============================================================================
key = r"<html><body><h1>hello world<h1></body></html>" # 这是要匹配的文本
p1 = r"(?<=<h1>).+?(?=<h1>)" # 这是我们写的正则表达式规则，你现在可以不理解啥意思
pattern1 = re.compile(p1) # 我们在编译这段正则表达式
matcher1 = re.search(pattern1,key) # 在源文本中搜索符合正则表达式的部分
if matcher1: # 如果匹配成功
    print(matcher1.group(0)) # 打印出来

#==============================================================================
# 正则表达式入门-2
#==============================================================================
key = r"javapythonhtmlvhdl" # 这是源文本
p1 = r"python" # 这是我们写的正则表达式
pattern1 = re.compile(p1) # 编译
matcher1 = re.search(pattern1,key) # 是查询
if matcher1: # 如果匹配成功
    print(matcher1.group(0)) #打印出来

#==============================================================================
#  贪婪与懒惰
#==============================================================================
key = r"chuxiuhong@hit.edu.cn"
p1 = r"@.+\."#我想匹配到@后面一直到“.”之间的，在这里是hit
pattern1 = re.compile(p1)
print pattern1.findall(key)
# 输出结果:['@hit.edu.'] 咋多了呢？我理想的结果是@hit.，你咋还给我加量了呢？
# 正则表达式默认是“贪婪”的,'+'代表是字符重复一次或多次,所以它会尽可能“贪婪”地多给我们匹配字符

# 我们怎么解决这种问题呢？让他变成懒惰模式，只要在“+”后面加一个“？”就好了
key = r"chuxiuhong@hit.edu.cn"
p1 = r"@.+?\."#我想匹配到@后面一直到“.”之间的，在这里是hit
pattern1 = re.compile(p1)
print(pattern1.findall(key))
# 输出结果 ['@hit.']


# =============================================================================
# 匹配开头结尾
# =============================================================================

#\b 用来匹配边界
lst = re.findall(r".*d\b", "word pwd abc")  # d的前面匹配一次或者多次,贪婪算法匹配多次及时到符合的仍然继续匹配知道没有符合的获取最长的那个符合的
print(lst)

# 非贪婪匹配
lst = re.findall(r".*?d\b", "word pwd abc")  ##d的前面匹配一次或者多次,非贪婪算法匹配多次到最短符合就获取
print(lst)

# 优化版:舍掉空格  \S 匹配任意非空白符 ,下面就会将单词之间的空格去掉
lst = re.findall(r"\S*?d\b", "word pwd abc")
print(lst)

# 匹配单词的左边界
lst = re.findall(r"\bw.* ", "word abc")  # 在*后面有个空格,就是标识匹配到空格,所有这个匹配到'word ' 这边也存在贪婪算法
print(lst)


# ^ 必须以某个字符开头,后面的字符无所谓
# $ 必须以某个字符结尾,前面的字符无所谓

strvar = "大哥大嫂大爷"
print(re.findall('大.', strvar))
# ['大哥', '大嫂', '大爷']

print(re.findall('^大.', strvar))
# ['大哥']

print(re.findall('大.$', strvar))
# ['大爷']

print(re.findall('^大.$', strvar))  # 没有匹配到符合的,所有输出空列表
# []

print(re.findall('^大.*?$', strvar))  # 字符串是一个整体,所有要匹配到结尾的字符
# ['大哥大嫂大爷']


print(re.findall('^大.*?大$', strvar))
# []  #因为字符串中有以大开头,但是没有大结尾,所有匹配没有符合的,返回空列表

print(re.findall('^大.*?爷$', strvar))
# ['大哥大嫂大爷']

# 把字符串看成一个整体,只要一个结果
print(re.findall('^g.*? ', 'giveme 1gfive gay '))
# ['giveme ']

print(re.findall('five$', 'aassfive'))
# ['five']

print(re.findall('five$', 'aassfive00'))
# []   #没有以e结尾的

print(re.findall('^giveme$', 'giveme'))
# ['giveme']

print(re.findall('^giveme$', 'givemeq'))
# [] #没有符合以g开头以e结尾的

print(re.findall('^giv.me$', 'giveme'))
# ['giveme']  #中间那个.可以为任意字符,以g开头和以e结尾外加字符符合


print(re.findall('^giveme$', 'giveme giveme'))
# []  #没有符合的

print(re.findall('giveme', 'giveme giveme'))  # 符合两个
# ['giveme', 'giveme']  #没有以什么开头或以什么结尾,只要字符符合就可以符合

print(re.findall("^g.*e", 'giveme 1gfive gay'))
# ['giveme 1gfive']   #注意贪婪算法

print(re.findall("^g.*?e", 'giveme 1gfive gay'))
# ['give']    #非贪婪算法,遇到最短符合的字符串就获取


# =============================================================================
# 匹配多行
# =============================================================================
key ='''Created: 2019-07-03 15:46:34 by: qujing Number of alarms:  3026

Critical 28554515 SubNetwork=ONRM_ROOT_MO,SubNetwork=QuJing,ManagedElement=RBS6601_QJXWTT5146_WCTY_EFT
=====================================================================================================
AlarmId: 28554515
ObjectOfReference: SubNetwork=ONRM_ROOT_MO,SubNetwork=QuJing,ManagedElement=RBS6601_QJXWTT5146_WCTY_EFT
PerceivedSeverity: Critical
Acknowledger:
AckHistOp:
AckHistTime:
AckHistType:
AcknowledgeTime:
AlarmCategory:
AlarmClass:
AlarmNumber:
CeaseRecordType: Heartbeat Alarm
CeaseTime: 2019-06-24 08:29:40
CommentOp:
CommentText:
CommentTime:
CorrelatedId:
EventTime: 2019-06-24 06:00:46
EventType: Communications alarm
LoggingTime: 2019-06-24 06:00:52
ObjectClassOfReference:
ObjectType: 513241764
PreviousSeverity:
ProbableCause: LAN Error/Communication Error
ProblemData:
ProblemText: Heartbeat trap not received within the given heartbeat interval: 200
ProposedRepairAction:
ProposedRepairActionText: Unknown
RecordType: Heartbeat Alarm
SpecificProblem: Heartbeat Failure
FDN2:


Critical 28554288 SubNetwork=ONRM_ROOT_MO,SubNetwork=QuJing,ManagedElement=RBS6601_QJFYZY5100_WCTY_EFT
=====================================================================================================
AlarmId: 28554288
ObjectOfReference: SubNetwork=ONRM_ROOT_MO,SubNetwork=QuJing,ManagedElement=RBS6601_QJFYZY5100_WCTY_EFT
PerceivedSeverity: Critical
Acknowledger:
AckHistOp:
AckHistTime:
AckHistType:
AcknowledgeTime:
AlarmCategory:
AlarmClass:
AlarmNumber:
CeaseRecordType: Heartbeat Alarm
CeaseTime: 2019-06-24 05:57:50
CommentOp:
CommentText:
CommentTime:
CorrelatedId:
EventTime: 2019-06-24 05:53:43
EventType: Communications alarm
LoggingTime: 2019-06-24 05:53:49
ObjectClassOfReference:
ObjectType: 513241764
PreviousSeverity:
ProbableCause: LAN Error/Communication Error
ProblemData:
ProblemText: Heartbeat trap not received within the given heartbeat interval: 200
ProposedRepairAction:
ProposedRepairActionText: Unknown
RecordType: Heartbeat Alarm
SpecificProblem: Heartbeat Failure
FDN2:
'''

p1 = r'(Critical.*[\s\S]+?FDN2:)'  # 匹配以Critical开头，以FDN2:结尾的字符串
ls1 = re.findall(p1,key)

# =============================================================================
# 匹配所有的数字:整数、小数、负数 都可以
# =============================================================================
ls2 ='曲靖市人口78.43万,曲靖市共有8个县1个区！共有3500个自然村。去年GDP增长率是-1.5'
ls_new = re.sub(r'-?\d+\.?\d*','',ls2)
ls_new
