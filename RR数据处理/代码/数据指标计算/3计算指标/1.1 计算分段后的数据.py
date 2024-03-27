import pandas as pd
import numpy as np
import os
import nolds  # nolds库用于DFA计算

def calculate_sd1_sd2(rr_intervals):
    rr_diff = np.diff(rr_intervals)
    rr_diff_n = rr_diff[:-1]
    rr_diff_np1 = rr_diff[1:]

    SD1 = np.sqrt(np.std(rr_diff_n - rr_diff_np1, ddof=1) / 2)
    SD2 = np.sqrt(np.std(rr_diff_n + rr_diff_np1, ddof=1) / 2)

    return SD1, SD2

def calculate_dfa(rr_intervals):
    # 计算DFA
    alpha = nolds.dfa(rr_intervals)
    return alpha

# 读取文件夹中的所有文件
input_dir = '/12.14室内跑数据/setData_1min/'
output_dir = '/12.14室内跑数据/'
output_file = '1min_SD_results.csv'

results = []
dirs = os.listdir(input_dir)
for all_files in dirs:
    file_path = os.path.join(input_dir, all_files)
    data = pd.read_csv(file_path)

    if 'RRI' in data.columns:
        SD1, SD2 = calculate_sd1_sd2(data['RRI'].values)
        DFA = calculate_dfa(data['RRI'].values)
        results.append({'Filename': all_files[:-4], 'SD1': SD1, 'SD2': SD2, 'DFA': DFA})

# 将结果写入CSV文件
output_file_path = os.path.join(output_dir, output_file)
pd.DataFrame(results).to_csv(output_file_path, index=False)

print(f"Results saved to {output_file_path}")
