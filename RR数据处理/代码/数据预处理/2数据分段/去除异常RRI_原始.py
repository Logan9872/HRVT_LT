import pandas as pd
import numpy as np
import os
from scipy import interpolate

def remove_outliers_and_interpolate(data, window_size=60, z_threshold=3):
    if 'RRI' in data.columns:
        rr_intervals = data['RRI'].values.astype(float)
        # 设置异常值阈值
        outlier_threshold1 = 1000
        outlier_threshold2 = 200

        for i in range(len(rr_intervals)):
            window_start = max(0, i - window_size // 2)
            window_end = min(len(rr_intervals), i + window_size // 2 + 1)
            window_data = rr_intervals[window_start:window_end]

            local_median = np.median(window_data)
            local_mean = np.average(window_data)
            local_std = np.std(window_data)

            # 判断异常值的上下限
            if rr_intervals[i] <= outlier_threshold1 and rr_intervals[i] >= outlier_threshold2:

                if abs(rr_intervals[i] - local_median) > z_threshold * local_std:
                    rr_intervals[i] = np.nan

                elif abs(rr_intervals[i] - local_mean) > z_threshold * local_std:
                    rr_intervals[i] = np.nan
            else:
                rr_intervals[i] = np.nan

        not_nan = np.logical_not(np.isnan(rr_intervals))
        if np.any(not_nan):
            indices = np.arange(len(rr_intervals))
            interp = interpolate.interp1d(indices[not_nan], rr_intervals[not_nan], kind='4', bounds_error=False, fill_value="extrapolate")
            # rr_intervals = interp(indices)

            interpolated_values = interp(indices)
            rr_intervals = np.round(interpolated_values).astype(int)

        data['RRI'] = rr_intervals
        hr = np.round(60000 / rr_intervals)
        data['HR'] = hr

    return data

# Directory path for input and output
# input_directory_path = "E:/12.13乳酸阈数据处理/12.14室内跑数据/merageData/"
# output_directory_path = "E:/12.13乳酸阈数据处理/12.14室内跑数据/merageDataMM/"

input_directory_path = "E:/12.13乳酸阈数据处理/12.14户外跑数据/merageData/"
output_directory_path = "E:/12.13乳酸阈数据处理/12.14户外跑数据/merageDataMM/"

# Process each file in the directory
for filename in os.listdir(input_directory_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_directory_path, filename)
        data = pd.read_csv(file_path)
        processed_data = remove_outliers_and_interpolate(data)
        processed_file_path = os.path.join(output_directory_path, filename)
        processed_data.to_csv(processed_file_path, index=False)
        print(f"Processed and saved: {processed_file_path}")
