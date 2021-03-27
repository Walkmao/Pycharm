
import os
import re
from sqlalchemy import create_engine
import pandas as pd


def deal_str(row):
    if '区' in str(row):
        return (row.split('区')[-1])
    return row

def deal_str2(row):
    str1 = re.findall('(.*?\d+).*',str(row))
    if len(str1):
        return str1[0]
    else:
        return row

def Output(row,df_):
    try:
        row = re.sub(r'[\(\)（）]','',str(row))
        x = pd.DataFrame(df_[df_['qhnxxdz'].str.contains(row)]['qhnxxdz'])
        if len(x):
            return x.iloc[0]
            print(x.iloc[0])
        else:
            return 0
    except:
        return 0

def main(data,df_):

    # df
    df_ = df_.drop_duplicates()

    # datas
    data['adress'] = data['adress'].str.replace(" ", "")
    data = data.dropna()

    data['adress2'] = data['adress'].apply(deal_str)
    data['middle'] = data['adress2'].apply(deal_str2)
    data['result'] = data.apply(lambda y: Output(y['middle'], df_), axis=1)
    return data

if __name__ == '__main__':

    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

    # oracle
    engine = create_engine('oracle+cx_oracle://cyptzb:cyptzb@2.40.9.42:1522/ORCL')
    df = pd.read_sql('select dzmc,qhnxxdz from CYPTZB.T_DZ_FWXXB', engine)
    print("df.shape:",df.shape)

    # excel
    datas = pd.read_excel(r'C:\Users\Mirco\Desktop\test.xlsx', usecols=['adress'], sheet_name='sheet1')
    print("datas.shape:", datas.shape)

    # 数据处理
    pd_datas = main(datas,df)

    # 数据导出
    pd_datas.to_excel(r'C:\Users\Mirco\Desktop\output_1.xlsx')