
import pandas as pd
import os
from datetime import timedelta

# -------------------------------------数据读取和预处理----------------------------------------
# 遍历在文件夹中的文件并读取
# dirs = os.listdir("E:\\develop\\12.13乳酸阈数据处理\\Polar实验数据\\Polar RR 户外\\")
dirs = os.listdir("E:\\develop\\12.13乳酸阈数据处理\\Polar实验数据\\Polar RR 室内\\")
for all_files in dirs:
    file = "E:\\develop\\12.13乳酸阈数据处理\\Polar实验数据\\Polar RR 室内\\" + all_files + ""
    rr_data = pd.read_csv(file, encoding="unicode_escape")

    rr_data = rr_data.iloc[1:]

    # Calculate cumulative duration
    rr_data['cumulative_duration'] = rr_data['duration'].cumsum()

    # Convert cumulative duration to timedelta (in milliseconds)
    rr_data['timestamp'] = rr_data['cumulative_duration'].apply(lambda x: timedelta(milliseconds=x))

    # Convert timedelta to formatted timestamp
    rr_data['Timestamp'] = rr_data['timestamp'].apply(lambda x: f"{int(x.days)}:{x.seconds//3600:02d}:{(x.seconds//60)%60:02d}:{x.seconds%60:02d}.{x.microseconds//1000:03d}")

    rr_data = rr_data[['Timestamp', 'duration']]

    print(rr_data)

    title = all_files[:-9]  # 读取文件名".csv"之前的名称

    rr_data.to_csv("E:/develop/12.13乳酸阈数据处理/RR数据处理/室内RR数据提取/" + title + ".csv",  index=False)


