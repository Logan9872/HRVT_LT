import pandas as pd
import numpy as np
import os
import pyhrv.nonlinear as nl  # 导入pyHRV的非线性分析模块

def calculate_sd1_sd2(rr_intervals):
    rr_diff = np.diff(rr_intervals)
    rr_diff_n = rr_diff[:-1]
    rr_diff_np1 = rr_diff[1:]

    SD1 = np.sqrt(np.std(rr_diff_n - rr_diff_np1, ddof=1) / 2)
    SD2 = np.sqrt(np.std(rr_diff_n + rr_diff_np1, ddof=1) / 2)

    return SD1, SD2

def calculate_dfa(rr_intervals):
    # 使用pyHRV计算DFA
    dfa_result = nl.dfa(rr_intervals)
    alpha1 = dfa_result['dfa_alpha1']  # DFA的短期指数
    alpha2 = dfa_result['dfa_alpha2']  # DFA的长期指数
    return alpha1, alpha2

def calculate_cv(rr_intervals):
    mean_rr = np.mean(rr_intervals)
    std_rr = np.std(rr_intervals, ddof=1)
    cv = std_rr / mean_rr if mean_rr != 0 else 0
    mean_hr = 60000 / mean_rr
    return cv, mean_hr

def calculate_sdnn_rmssd(rr_intervals):
    SDNN = np.std(rr_intervals, ddof=1)  # SDNN的计算
    RMSSD = np.sqrt(np.mean(np.square(np.diff(rr_intervals))))  # RMSSD的计算
    return SDNN, RMSSD

input_dir = 'E:/12.13乳酸阈数据处理/12.14室内跑数据/setData_2min/'
output_dir = 'E:/12.13乳酸阈数据处理/12.14室内跑数据/'
output_file = '2min_SD_results.csv'  # 输出文件的名称

results = []
dirs = os.listdir(input_dir)
for all_files in dirs:
    file_path = os.path.join(input_dir, all_files)
    data = pd.read_csv(file_path)

    if 'RRI' in data.columns:
        SD1, SD2 = calculate_sd1_sd2(data['RRI'].values)
        alpha1, alpha2 = calculate_dfa(data['RRI'].values)
        cv, mean_hr = calculate_cv(data['RRI'].values)
        SDNN, RMSSD = calculate_sdnn_rmssd(data['RRI'].values)
        results.append({'Filename': all_files[:-4], 'SD1': SD1, 'SD2': SD2, 'DFA Alpha1': alpha1, 'DFA Alpha2': alpha2, 'CV': cv, 'mean HR': mean_hr, 'SDNN': SDNN, 'RMSSD': RMSSD})

# 将结果写入CSV文件
output_file_path = os.path.join(output_dir, output_file)
pd.DataFrame(results).to_csv(output_file_path, index=False)

print(f"Results saved to {output_file_path}")
