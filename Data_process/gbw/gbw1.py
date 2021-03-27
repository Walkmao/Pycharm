import os
import pandas as pd

#path = r'E:\ToDoList\干保委\区政府个人报告2018'
path = r"C:\Users\Mirco\Desktop\2020年区政府31人报告"
filenames = os.listdir(path)

sum_data = []
for filename in filenames:
    print(filename)
    dic = {}
    datas = pd.read_excel(path + "\\" + filename)  # 数据读取

    dic["姓名"] = datas.iloc[0, 4]
    dic["体检编号"] = datas.iloc[0, 1]

    datas = datas.iloc[:, [0, 1]]  # 只取前两列作为数据处理内容
    datas.rename(columns={'Unnamed: 0': 'col_name', 'Unnamed: 1': 'values'}, inplace=True)  # 重命名两列列名
    datas.col_name.str.strip()  # 去掉names列左右的空格
    datas.set_index('col_name', inplace=True)  # 在本地修改并设置names列作为索引列

    # datas.loc['身高','values']
    indexes = ['身高', '体重', '血压（收缩压）', '血压（舒张压）', 'HDL胆固醇(HDL-CH)', 'LDL胆固醇(LDL-CH)',
               '谷草转氨酶(AST)', '谷丙转氨酶(ALT)', '尿酸(UA)', '甘油三脂(TRIG)', '血清总胆固醇(CHOL)',
               '空腹血糖(GLU)', '糖化血红蛋白(GHb)']
    da = datas.loc[indexes, 'values']
    dic['身高'] = da[0]
    dic['体重'] = da[1]
    dic['血压（收缩压）'] = da[2]
    dic['血压（舒张压）'] = da[3]
    dic['HDL胆固醇(HDL-CH)'] = da[4]
    dic['LDL胆固醇(LDL-CH)'] = da[5]
    dic['谷草转氨酶(AST)'] = da[6]
    dic['谷丙转氨酶(ALT)'] = da[7]
    dic['尿酸(UA)'] = da[8]
    dic['甘油三脂(TRIG)'] = da[9]
    dic['血清总胆固醇(CHOL)'] = da[10]
    dic['空腹血糖(GLU)'] = da[11]
    dic['糖化血红蛋白(GHb)'] = da[12]
    sum_data.append(dic)
pd_data = pd.DataFrame(sum_data)
pd_data.to_excel(r'C:\Users\Mirco\Desktop\gbw.xlsx')