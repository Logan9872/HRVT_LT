import pandas as pd
import os

dirs = os.listdir("C:/Users/Administrator/Desktop/merageData/")
for all_files in dirs:
    file_path = "C:/Users/Administrator/Desktop/merageData/" + all_files
    data = pd.read_csv(file_path, encoding="unicode_escape")
    # 设置暂停的最短持续时间（以秒为单位）
    min_pause_seconds = 30

    # 初始化变量
    start_index = 0
    stages = []
    last_time = data['Time_seconds'][0]

    # 遍历数据来识别跑步阶段
    for i in range(1, len(data)):
        current_time = data['Time_seconds'][i]
        time_diff = current_time - last_time

        # 如果速度为0且时间差超过设定的暂停时间，认为发生了暂停
        if data['Speed '][i] == 0 and time_diff > min_pause_seconds:
            # 如果当前阶段长度大于0，添加到阶段列表中
            if i - 1 > start_index:
                stages.append((start_index, i - 1))
            start_index = i + 1
        last_time = current_time

    # 添加最后一个阶段（如果存在）
    if start_index < len(data) - 1:
        stages.append((start_index, len(data) - 1))

    # 提取并保存每个阶段
    output_dir = 'C:/Users/Administrator/Desktop/setData/'  # 输出文件夹路径
    for j, (start, end) in enumerate(stages):
        stage_data = data.iloc[start:end + 1]
        output_file_name = os.path.join(output_dir, f"{os.path.splitext(all_files)[0]}_stage_{j + 1}.csv")
        stage_data.to_csv(output_file_name, index=False)
        print(f"Saved: {output_file_name}")
