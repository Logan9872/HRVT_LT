import pandas as pd
import os

# 加载数据
dirs = os.listdir("E:/12.13乳酸阈数据处理/12.14室内跑数据/merageDataMM/")
for all_files in dirs:
    file_path = "E:/12.13乳酸阈数据处理/12.14室内跑数据/merageDataMM/" + all_files
    data = pd.read_csv(file_path, encoding="unicode_escape")

    # 设置阶段的最短持续时间和暂停的最短持续时间（以秒为单位）
    min_duration_seconds = 3 * 60
    min_pause_seconds = 20

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
            running_time += 1
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

    # 提取并保存每个阶段，去除前后30秒的数据
    output_dir = 'E:/12.13乳酸阈数据处理/12.14室内跑数据/setData/'  # 输出文件夹路径
    for j, (start, end) in enumerate(stages):
        # 调整开始和结束索引以去除前后30秒的数据
        adjusted_start = min(start + 30, end)  # 确保不超过阶段的结束
        adjusted_end = max(end - 30, adjusted_start)  # 确保不低于调整后的开始
        stage_data = data.iloc[adjusted_start:adjusted_end]
        output_file_name = os.path.join(output_dir, f"{os.path.splitext(all_files)[0]}_{j + 1}.csv")
        stage_data.to_csv(output_file_name, index=False)
        print(f"Saved: {output_file_name}")
