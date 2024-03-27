import pandas as pd
from scipy.interpolate import interp1d
from datetime import timedelta

# 修改后的将字符串转换为timedelta的函数
def convert_to_timedelta(timestamp_str):
    parts = timestamp_str.split(':')
    hours = int(parts[1])
    minutes = int(parts[2])
    seconds_milliseconds = parts[3].split('.')
    seconds = int(seconds_milliseconds[0])
    milliseconds = int(seconds_milliseconds[1])
    return timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)


dirs = os.listdir("E:\\develop\\12.13乳酸阈数据处理\\RR数据处理\训练日志提取\\")
for all_files in dirs:
    file_training = "E:\\develop\\12.13乳酸阈数据处理\\RR数据处理\训练日志提取\\" + all_files + ""
    file_rr = "E:\\develop\\12.13乳酸阈数据处理\\RR数据处理\\" + all_files + ""

    training_log_data = pd.read_csv(file_trainin, encoding="unicode_escape")
    rr_data = pd.read_csv(file_rr, encoding="unicode_escape")

    # 预处理训练日志数据
    # 假设时间列名为'Time'
    CSV_data = pd.DataFrame()
    CSV_data['Time'] = rr_data['Timestamp']

    training_log_data['Time'] = pd.to_datetime(training_log_data['Time'])
    training_log_data['Time_seconds'] = training_log_data['Time'].dt.second + training_log_data['Time'].dt.minute * 60 + training_log_data['Time'].dt.hour * 3600

    # 预处理RR数据
    rr_data['Timestamp'] = rr_data['Timestamp'].apply(convert_to_timedelta)
    rr_data['Time_seconds'] = rr_data['Timestamp'].dt.total_seconds()
    rr_data['HR'] = (60000 / rr_data['duration']).round(3)
    # 对齐时间戳
    # 插值
    columns_to_interpolate = ["Speed (km/h)"]  # 替换为需要插值的列名
    interpolated_data = pd.DataFrame()
    for col in columns_to_interpolate:
        training_log_data[col] = pd.to_numeric(training_log_data[col], errors='coerce')
        # 线性插值
        f = interp1d(training_log_data['Time_seconds'], training_log_data[col].round(3), kind='linear', fill_value='extrapolate')
        interpolated_data[col] = f(rr_data['Time_seconds'])


    # 合并数据
    aligned_data = pd.concat([rr_data, interpolated_data], axis=1)

    CSV_data['Time_seconds'] = aligned_data['Time_seconds']
    CSV_data['RRI'] = aligned_data['duration']
    CSV_data['HR'] = aligned_data['HR']
    CSV_data['Speed '] = aligned_data['Speed (km/h)']

    print(CSV_data)
    # 保存合并后的数据
    CSV_data.to_csv("E:/develop/12.13乳酸阈数据处理/RR数据处理/合并后的数据/" + title + ".csv",  index=False)
