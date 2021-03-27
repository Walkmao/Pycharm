import time
import pymssql
import pandas as pd

def Read_list(path):
    table_list = pd.read_excel(path)
    #print("datas.shape:", datas.shape)
    return table_list

def Build_sql(table_name,time):
    table_main = table_name
    table_log = table_name + "_LOG"
    table_backup = table_log + time

    # 自定义sql语句
    sql_bk = ("select * into {0} from {1} where 1=2".format(table_backup, table_log))  # 备份数据表

    sql_del = ("drop table {}".format(table_backup))

    # 查询主表
    sql_q1 = ("select a.name table_name, b.name column_name,"
              " case c.name when 'numeric' then 'numeric(' + convert(varchar,b.length) + '，' + convert(varchar,b.xscale) + ')'"
              " when 'char' then 'char(' + convert(varchar,b.length) + ')'"
              " when 'varchar' then 'varchar(' + convert(varchar,b.length) + ')'"
              " else c.name END AS data_type"
              " from sysobjects a,syscolumns b,systypes c where a.id=b.id"
              " and a.name= '{}' and a.xtype='U'"
              " and b.xtype=c.xtype".format(table_main))

    # 查询log表
    sql_q2 = ("select a.name table_name, b.name column_name,"
              " case c.name when 'numeric' then 'numeric(' + convert(varchar,b.length) + '，' + convert(varchar,b.xscale) + ')'"
              " when 'char' then 'char(' + convert(varchar,b.length) + ')'"
              " when 'varchar' then 'varchar(' + convert(varchar,b.length) + ')'"
              " else c.name END AS data_type"
              " from sysobjects a,syscolumns b,systypes c where a.id=b.id"
              " and a.name= '{}' and a.xtype='U'"
              " and b.xtype=c.xtype".format(table_log))

    return sql_bk,sql_del,sql_q1,sql_q2

if __name__ == '__main__':

    time_ = time.strftime('%m%d')

    # 连接数据库
    host_l = ['10.45.0.143','10.45.0.138','10.45.0.139']
    user_ = 'sa'
    password_1 = 'sql2k8@sg'
    password_2 = 'sql2k8@123'
    databases = ['ESB_pub_client1','ESB_medical_client1']

    for database in databases:
        nums_1 = 0            # 数据库修改表数
        nums_2 = 0            # 无须修改的表数
        print("连接到数据库：",database)
        conn = pymssql.connect(host=host_l[0], port=1433, user=user_, password=password_1, database=database)
        cursor = conn.cursor()

        # 读取Excel表
        path = r'C:\Users\Mirco\Desktop\table_list.xlsx'
        table_list = Read_list(path)

        # 读取和查询两张表的字段
        if database == 'ESB_pub_client1':
            table_list2 = table_list['table_name2']
            table_list2.dropna(axis=0, how='any', inplace=True)
        else:
            table_list2 = table_list['table_name1']
            table_list2.dropna(axis=0, how='any', inplace=True)

        # 循环表名修改表结构
        for table_name in table_list2:
            status = 1                # 状态标记
            sql_bk,sql_del,sql_q1,sql_q2 = Build_sql(table_name,time_)

            #备份log数据表（若log本身不存在，跳过）
            try:
                cursor.execute(sql_bk)
                # conn.commit()

                print("已经备份：",table_name)
            except:
                # print(table_name,"_log表不存在")
                # status = 0
                nums_2 += 1

            if status == 1:
                # 查询主表和log表
                df_main = pd.read_sql(sql_q1, con=conn)
                df_log = pd.read_sql(sql_q2, con=conn)
                # print(df_main.shape,df_log.shape)

                # 数据处理+清洗
                df_log['column_name'] = df_log['column_name'].str.upper()
                df_main['column_name'] = df_main['column_name'].str.upper()

                df_main['data'] = df_main['column_name'] + ' ' + df_main['data_type']
                df_main['data'] = df_main['data'].str.replace("，", ",")

                # 比较表结构并返回
                df_output = df_main[~df_main['column_name'].isin(df_log.column_name)]

                # 修改数据库表结构
                if df_output.shape[0] > 0:
                    nums_1 += 1
                    print("正在修改表：",table_name,":")
                    datas = df_output['data']
                    table_log = table_name + "_LOG"
                    for data in datas:
                        sql_add = "alter table {0} add {1}".format(table_log, data)
                        try:
                            print(sql_add)
                            cursor.execute(sql_add)
                            conn.commit()
                        except:
                            print("插入异常：",table_name,data)
                # else:
                #     print(database,table_name,"无须修改")
        print(database, "：修改{0}张表,未改{1}".format(nums_1, nums_2))
        print("----------next database----------")
    conn.close()



