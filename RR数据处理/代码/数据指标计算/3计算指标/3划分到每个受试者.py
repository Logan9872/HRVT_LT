import pandas as pd


import os

# 读取导出的数据文件
file_path = 'E:/12.13乳酸阈数据处理/12.14室内跑数据/2min_SD_results_sorted.csv'  # 请替换为您的文件路径
# file_path = 'E:/12.13乳酸阈数据处理/12.14户外跑数据/out_1min_SD_results_sorted.csv'  # 请替换为您的文件路径
results_df = pd.read_csv(file_path)

# 分割Filename来获取不同的分组
results_df['Group'] = results_df['Filename'].apply(lambda x: x.split('_')[0])

# 按照文件名前缀分组并保存
output_dir = 'E:/12.13乳酸阈数据处理/12.14室内跑数据/2minSetDataSubject/'  # 请替换为您的输出文件夹路径
# output_dir = 'E:/12.13乳酸阈数据处理/12.14户外跑数据/1minSetDataSubject/'  # 请替换为您的输出文件夹路径
for group_name, group_df in results_df.groupby('Group'):
    group_df = group_df.drop(['Group'], axis=1)  # 删除Group列
    output_file_path = os.path.join(output_dir, group_name + '.csv')
    group_df.to_csv(output_file_path, index=False)
    print(f"Saved: {output_file_path}")

# 提示完成
print("Files have been saved.")
