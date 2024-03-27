
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------数据读取和预处理----------------------------------------
# 遍历在文件夹中的文件并读取
dirs = os.listdir("E:\\develop\\12.13乳酸阈数据处理\\Polar实验数据\\Polar 室内训练日志\\")
for all_files in dirs:
    file = "E:\\develop\\12.13乳酸阈数据处理\\Polar实验数据\\Polar 室内训练日志\\" + all_files + ""
    CSV_data = pd.read_csv(
        file,
        skiprows=2,
        encoding="unicode_escape")
    CSV_data = CSV_data[['Time', 'HR (bpm)', 'Speed (km/h)', 'Pace (min/km)']]

    print(CSV_data)
    title = all_files[:-10]  # 读取文件名".csv"之前的名称

    CSV_data.to_csv("E:/develop/12.13乳酸阈数据处理/RR数据处理/室内训练日志提取/" + title + ".csv",  index=False)
    print(file)

