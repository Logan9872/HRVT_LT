import pandas as pd
import numpy as np
import os

def calculate_sd1_sd2(rr_intervals):
    rr_diff = np.diff(rr_intervals)
    rr_diff_n = rr_diff[:-1]
    rr_diff_np1 = rr_diff[1:]

    SD1 = np.sqrt(np.std(rr_diff_n - rr_diff_np1, ddof=1) / 2)
    SD2 = np.sqrt(np.std(rr_diff_n + rr_diff_np1, ddof=1) / 2)

    return SD1, SD2

def DFA(data, n, fittime):
    N = len(data)
    n_int = N // n
    nf = n_int * n
    mean_rr = np.mean(data[:nf])
    y = []
    y_hat = []
    for k in range(nf):
        y.append(np.sum(data[:k + 1]) - (k + 1) * mean_rr)
    for i in range(n_int):
        y_temp = y[i * n:(i + 1) * n]
        x = np.arange(i * n + 1, i * n + n + 1)
        coef = np.polyfit(x, y_temp, deg=fittime)
        y_hat.extend(np.polyval(coef, x))
    y_hat = np.array(y_hat)[:N]
    fn = np.sqrt(np.mean((np.asarray(y) - y_hat) ** 2))
    return fn

def calculate_dfa(rr_intervals):
    fittime = 1  # 线性拟合的次数
    n = 4  # 初始窗口大小
    while n <= len(rr_intervals) // 4:
        try:
            alpha = DFA(rr_intervals, n, fittime)
            return alpha
        except:
            n += 4
    return np.nan

# 读取文件夹中的所有文件
input_dir = 'E:/12.13乳酸阈数据处理/12.14室内跑数据/setData_2min/'
output_dir = 'E:/12.13乳酸阈数据处理/12.14室内跑数据/'
output_file = '2min_SD_results.csv'

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
