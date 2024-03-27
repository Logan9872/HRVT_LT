import pandas as pd
import numpy as np
import os
from scipy import interpolate
def remove_outliers_and_calculate_hr(data):
    if 'RRI' in data.columns:
        rr_intervals = data['RRI'].values.astype(float)  # 转换为浮点数类型

        # 计算中位数和标准差，识别并替换异常值
        for i in range(len(rr_intervals)):
            start = max(0, i - 30)
            end = min(len(rr_intervals), i + 30)
            local_median = np.median(rr_intervals[start:end])
            local_std = np.std(rr_intervals[start:end])

            if abs(rr_intervals[i] - local_median) > 3 * local_std:
                rr_intervals[i] = np.nan

        # 使用样条插值替换NaN值
        not_nan = np.logical_not(np.isnan(rr_intervals))
        indices = np.arange(len(rr_intervals))
        interp = interpolate.interp1d(indices[not_nan], rr_intervals[not_nan], kind='cubic', fill_value="extrapolate")
        rr_intervals = interp(indices)

        # 计算心率
        hr = 60000 / rr_intervals
        data['HR'] = hr

    return data


def convert_time_to_seconds(time_str):
    d, h, m, s = time_str.split(':')
    days = int(d)
    hours = int(h)
    minutes = int(m)
    seconds = float(s)
    return days * 86400 + hours * 3600 + minutes * 60 + seconds

    # 读取数据
    dirs = os.listdir("E:/12.13乳酸阈数据处理/12.14室内跑数据/setData/")
    for all_files in dirs:
        file_path = "E:/12.13乳酸阈数据处理/12.14室内跑数据/setData/" + all_files
        data = pd.read_csv(file_path, encoding="unicode_escape")

        # 将Time列转换为秒
        data['Time_seconds'] = data['Time'].apply(convert_time_to_seconds)

        # 处理RRI数据，去除异常值并重新计算HR
        data = remove_outliers_and_calculate_hr(data)
        # output_file = os.path.join("E:/12.13乳酸阈数据处理/12.14室内跑数据/setDataMM/", f"{all_files}")
        # data.to_csv(output_file, index=False)

        # 查找最稳定的一分钟区间
        min_std = float('inf')
        stable_start_index = 0

        for i in range(len(data) - 1):
            current_time = data['Time_seconds'][i]
            for j in range(i + 1, len(data)):
                if data['Time_seconds'][j] - current_time >= 120:
                    std = data['Speed '][i:j].std()
                    if std < min_std:
                        min_std = std
                        stable_start_index = i
                    break  # 跳出内循环

        # 提取最稳定的60秒数据
        stable_end_index = stable_start_index
        while stable_end_index < len(data) and data['Time_seconds'][stable_end_index] - data['Time_seconds'][stable_start_index] < 60:
            stable_end_index += 1

        stable_data = data.iloc[stable_start_index:stable_end_index]

        # 保存提取的数据
        output_dir = 'E:/12.13乳酸阈数据处理/12.14室内跑数据/setData_1min/'  # 输出文件夹路径
        output_file_name = os.path.join(output_dir, f"{all_files}")
        stable_data.to_csv(output_file_name, index=False)
