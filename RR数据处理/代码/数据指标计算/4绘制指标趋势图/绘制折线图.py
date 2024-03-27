import matplotlib.pyplot as plt
import os
import pandas as pd

# 设置中文字体和负号显示
plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签SimHei
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号
# 文件夹路径
# dir_path = "E:/12.13乳酸阈数据处理/12.14室内跑数据/1minSetDataSubject/"
# output_dir = 'E:/12.13乳酸阈数据处理/12.14室内跑数据/1PNG/'

dir_path = "E:/12.13乳酸阈数据处理/12.14户外跑数据/3minSetDataSubject/"
output_dir = 'E:/12.13乳酸阈数据处理/12.14户外跑数据/3PNG/'

# 遍历文件夹中的所有文件
dirs = os.listdir(dir_path)
for all_files in dirs:
    file_path = os.path.join(dir_path, all_files)
    data = pd.read_csv(file_path, encoding="unicode_escape")

    # 绘制折线图
    plt.figure(figsize=(10, 6))
    plt.plot(data['SD1'].index + 1, data['SD1'], label='SD1', marker='o', linestyle='-', color='blue')
    plt.plot(data['SD2'].index + 1, data['SD2'], label='SD2', marker='x', linestyle='--', color='red')
    plt.plot(data['DFA Alpha1'].index + 1, data['DFA Alpha1'], label='DFA Alpha1')
    plt.plot(data['DFA Alpha1'].index + 1, data['DFA Alpha2'], label='DFA Alpha2')
    plt.plot(data['DFA Alpha1'].index + 1, data['CV'], label='CV')


    file_name = all_files[:-4]

    plt.xlabel('时间')
    plt.ylabel('DFA值')
    plt.title(file_name)
    plt.legend()
    # plt.xticks(rotation=45)
    plt.tight_layout()

    # 保存图表
    output_file_name = os.path.join(output_dir, f"{file_name}.png")
    plt.savefig(output_file_name)

    plt.cla()
    plt.close("all")
