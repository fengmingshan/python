'''
爬取option tag里的内容里的内容
'''

import urllib2
import re      #导入正则库
url = 'xxx'
html = urllib2.urlopen(url).read()

patt = re.compile(r'<option.+?>(.+?)</option>')    #用正则表达式抓取option的内容
option = patt.findall(html)
f = open("out.txt", "w")
for value in option:
    print value
    f.writelines(value + '\n')
f.close()