# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 09:00:14 2020

@author: Administrator
"""

import pandas as pd
import numpy as np
import os


def read_csv_partly(file,names):
    file_data = pd.read_csv(file, engine='python', encoding='utf-8', chunksize=100000)
    for df_tmp in file_data:
        yield df_tmp


def split_to_mutilines(df, col):
    df_tmp = df[col].str.split('$', expand=True).stack(
    ).reset_index(level=1, drop=True).rename(col)
    return df_tmp
