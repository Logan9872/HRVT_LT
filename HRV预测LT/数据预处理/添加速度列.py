
import pandas as pd
import glob
import os

# 指定包含CSV文件的文件夹路径
directory_path = '/12.14室内跑数据/室内结果/1minSetDataSubject/'  # 替换为你的文件夹路径



# 匹配文件夹中所有CSV文件的模式
pattern = os.path.join(directory_path, '*.csv')

# 遍历文件夹中的所有CSV文件
for file_path in glob.glob(pattern):
    # 读取CSV文件
    df = pd.read_csv(file_path)

    # 确保'Filename'列是字符串类型，以避免前面用户遇到的错误
    df['Filename'] = df['Filename'].astype(str)

    # 提取'Filename'列中的数字部分
    df['Filename'] = df['Filename'].str.extract('(\d+)$').astype(int)

    # 计算'Velocity'列
    df['Velocity'] = (df['Filename'] - 1) * 1.2 + 4

    # 将修改后的DataFrame保存回CSV文件，不包含索引
    df.to_csv(file_path, index=False)

    # 可选：打印出已处理文件的路径
    print(f"已处理文件 {file_path}")
