import pandas as pd
import os

data_path = r'D:\test\基站IP导出' + '\\'
files_list = os.listdir(data_path)
for file in files_list :
    if 'NEManagedElement' in file:
        zte_file.append(file)
    if 'NEManagedElement' in file:
        zte_file.append(file)