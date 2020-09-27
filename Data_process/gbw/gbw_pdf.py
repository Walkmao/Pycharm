import os
import warnings

warnings.filterwarnings("ignore")
import pandas as pd

path = r"C:\Users\Mirco\Desktop\north\导出_csv"
filenames = os.listdir(path)
sum_df = pd.DataFrame()

for filename in filenames:
    data = pd.read_csv(path + "\\" + filename, names=['指标', '值'])  # usecols=[0,1]
    print(filename, len(data))
    # 数据清洗
    data['指标'] = data['指标'].str.replace(":", "")

    # 数据处理
    data_1 = data.copy()
    data_1['值'][:4] = data['指标'][:4]
    data_1['指标'][:4] = ['体检编号', '姓名', '收缩压', '舒张压']

    # 指标抽取
    if len(sum_df) == 0:
        data_T = data_1.T
        data_T.set_index([0], inplace=True)
        sum_df = sum_df.append(data_T)
    else:
        data_T = data_1.T
        data_T.set_index([0], inplace=True)
        sum_df = sum_df.append(data_T.iloc[1])

# print(sum_df)
sum_df.to_excel(r"C:\Users\Mirco\Desktop\north\sum_gbw.xlsx")