import pandas as pd
import glob
import os

# 定义两个文件夹的路径
directory_path_2 = 'E:/12.13乳酸阈数据处理/12.14室内跑数据/室内结果/1minSetDataSubject/'
directory_path_1 = 'E:/12.13乳酸阈数据处理/12.14室内跑数据/室内结果/blood_lactate/'

# 查找两个文件夹中所有的CSV文件路径
csv_files_1 = glob.glob(os.path.join(directory_path_1, '*.csv'))
csv_files_2 = glob.glob(os.path.join(directory_path_2, '*.csv'))

# 假设文件名相同，但路径不同
for file_path_1, file_path_2 in zip(sorted(csv_files_1), sorted(csv_files_2)):
    # 读取两个文件
    df1 = pd.read_csv(file_path_1)
    df2 = pd.read_csv(file_path_2)

    # 获取两个文件的基础文件名（不包含路径）
    base_name_1 = os.path.basename(file_path_1)
    base_name_2 = os.path.basename(file_path_2)

    # 检查文件名是否相同
    if base_name_1 == base_name_2:
        # 横向合并两个DataFrame，不基于共同列，假设行是对应的
        merged_df = pd.concat([df1, df2], axis=1)

        # 保存合并后的DataFrame到新文件
        merged_df.to_csv(f'E:/12.13乳酸阈数据处理/12.14室内跑数据/室内结果/1min合并数据/{base_name_1}', index=False)
    else:
        print(f"文件名不匹配: {base_name_1} 和 {base_name_2}")
