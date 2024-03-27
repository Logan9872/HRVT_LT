import pandas as pd
from datetime import timedelta
import os

# 创建目录
output_dir = 'E:/12.13乳酸阈数据处理/12.14户外跑数据/setData/'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def convert_to_timedelta(time_str):
    days, hours, minutes, sec_millisec = time_str.split(':')
    seconds, milliseconds = sec_millisec.split('.')
    return timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))

dirs = os.listdir("E:/12.13乳酸阈数据处理/12.14户外跑数据/Training/")
for all_files in dirs:
    file_path = "E:/12.13乳酸阈数据处理/12.14户外跑数据/merageData/" + all_files

    data = pd.read_csv(file_path, encoding="unicode_escape")
    # data['Time'] = data['Time'].apply(convert_to_timedelta)
    data_time = data['Time'].apply(convert_to_timedelta)
    data['Time_seconds'] =data_time.dt.total_seconds()

    stage_durations = [8*60, 5*60, 3*60+30, 3*60+30, 3*60, 3*60]
    stage_end_times = [sum(stage_durations[:i+1]) for i in range(len(stage_durations))]

    for i, end_time in enumerate(stage_end_times):
        if data['Time_seconds'].max() >= end_time:  # 检查数据是否达到这个阶段的结束时间
            stage_data = data[data['Time_seconds'] <= end_time]
            if i != 0:
                start_time = stage_end_times[i-1]
                stage_data = stage_data[stage_data['Time_seconds'] > start_time]

            output_file_name = os.path.join(output_dir, f"{os.path.splitext(all_files)[0]}_{i+1}.csv")
            stage_data.to_csv(output_file_name, index=False)
            print(f"Saved: {output_file_name}")

            data = data[data['Time_seconds'] > end_time]
