import pandas as pd

# 读取导出的数据文件
file_path = 'E:/12.13乳酸阈数据处理/12.14室内跑数据/2min_SD_results.csv'
# file_path = 'E:/12.13乳酸阈数据处理/12.14户外跑数据/out_3min_SD_results.csv'
results_df = pd.read_csv(file_path)

# 分割Filename来获取排序依据
# 假设文件名格式为 "name_index.csv"
results_df['Name'] = results_df['Filename'].apply(lambda x: x.split('_')[0])
results_df['Index'] = results_df['Filename'].apply(lambda x: int(x.split('_')[1].split('.')[0]))

# 首先按照名字排序，然后按照数字排序
results_df.sort_values(by=['Name', 'Index'], inplace=True)

# 删除辅助列
results_df.drop(['Name', 'Index'], axis=1, inplace=True)

# 保存排序后的数据
sorted_output_path = 'E:/12.13乳酸阈数据处理/12.14室内跑数据/2min_SD_results_sorted.csv'
# sorted_output_path = 'E:/12.13乳酸阈数据处理/12.14户外跑数据/out_3min_SD_results_sorted.csv'
results_df.to_csv(sorted_output_path, index=False)



