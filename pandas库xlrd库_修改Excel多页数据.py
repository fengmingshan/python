# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 16:54:34 2018
pandas/excel 获得sheet名 修改多个sheet数据 归一输出,创建excel 添加sheet 写入excel
@author: Administrator
"""

1 # -*- coding: utf-8 -*-
 2 
 3 import sys
 4 import glob
 5 import os
 6 from xlrd import open_workbook
 7 import xlwt
 8 import pandas as pd
 9 from xlutils.copy import copy
10 import numpy as np
11 
12 reload(sys)
13 sys.setdefaultencoding( "utf-8" )
14 
15 
16 def write_sheet(path,excel_name,name,index):
17     df = pd.read_excel(path,name)
18     list_sheet=[]
19     for number in range(0,len(df[0:])):
20         for i in df[0:].iloc[number]:
21             list_sheet.append(str(i))
22 
23     print list_sheet
24     rb=open_workbook(excel_name)
25     wb=copy(rb)
26     ws=wb.get_sheet(index)
27     number=0
28     for i in list_sheet:
29         ws.write(number,0,i)
30         number=number+1
31     wb.save(excel_name)
32 
33 def set_excel(excel_name,sheet_list):
34     i=0
35     for name in sheet_list:
36         if i==0:
37             book=xlwt.Workbook()
38             book.add_sheet(name)
39             book.save(excel_name)
40             i=i+1
41         else:
42             src = open_workbook(excel_name,formatting_info=True)
43             destination = copy(src)
44             destination.add_sheet(name)
45             destination.save(excel_name)
46 def main():
47     homdir=os.getcwd()
48     sour_dir=os.path.join(homdir,"qczsl")
49     path_dir=os.path.join(sour_dir,"*")
50     for path in glob.glob(path_dir):
51         excel_name=path.split("\\")[-1].strip("x")
52         sheet_list=open_workbook(path).sheet_names()
53         set_excel(excel_name,sheet_list)
54         for name in sheet_list:
55             index=sheet_list.index(name)
56             write_sheet(path,excel_name,name,index)
57             print "##########"
58 
59 if __name__ == "__main__":
60     main()