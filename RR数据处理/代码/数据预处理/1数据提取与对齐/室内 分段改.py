import pandas as pd
import os

# 加载数据
dirs = os.listdir("C:/Users/Administrator/Desktop/merageData/")
for all_files in dirs:
    file_path = "C:/Users/Administrator/Desktop/merageData/" + all_files
    data = pd.read_csv(file_path, encoding="unicode_escape")


    # 假设 'Speed' 列是速度数据
    # 设置阶段的最短持续时间（以秒为单位）
    min_duration_seconds = 3 * 60
    # 设置暂停的最短持续时间（以秒为单位）
    min_pause_seconds = 25

    # 遍历数据来识别跑步阶段
    start_index = None
    stages = []
    running_time = 0
    pause_time = 0

    for i in range(len(data)):
        # 如果速度不为0，开始或继续跑步阶段
        if data['Speed '][i] != 0:
            if start_index is None:
                start_index = i
            running_time += data['RRI'][i]*0.001  # 假设数据以1秒间隔采集，否则需要调整
            pause_time = 0
        # 如果速度为0，开始或继续暂停
        else:
            pause_time += 1
            # 如果暂停时间超过阈值且跑步时间达到最小阶段持续时间，则结束当前跑步阶段
            if pause_time > min_pause_seconds and running_time >= min_duration_seconds:
                stages.append((start_index, i - pause_time))
                start_index = None
                running_time = 0

    # 处理最后一个阶段（如果存在）
    if start_index is not None and running_time >= min_duration_seconds:
        stages.append((start_index, len(data)))

    # 提取并保存每个阶段
    output_dir = 'C:/Users/Administrator/Desktop/setData/'  # 输出文件夹路径
    for j, (start, end) in enumerate(stages):
        stage_data = data.iloc[start:end]
        output_file_name = os.path.join(output_dir, f"{os.path.splitext(all_files)[0]}_stage_{j + 1}.csv")
        stage_data.to_csv(output_file_name, index=False)
        print(f"Saved: {output_file_name}")