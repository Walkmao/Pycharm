import pymysql


class database_mysql(object):

    def __init__(self, host, username, password, db, charset='utf8', port=3306):
        self.host = host
        self.username = username
        self.password = password
        self.db = db
        self.charset = charset
        self.port = port
        self.conn = None
        self.cursor = None
        self.cur_dic = None

    # 数据库连接
    def connect(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.username, password=self.password,
                                    db=self.db,
                                    charset=self.charset)
        self.cursor = self.conn.cursor()
        self.cur_dic = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库断开
    def close(self):
        self.cursor.close()
        self.cur_dic.close()
        self.conn.close()

    def get_tuple(self, sql_str):
        try:
            self.cursor.execute(sql_str)
            tuple_data = self.cursor.fetchall()
        except Exception as e:
            print(e)
        return tuple_data

    # 查询，返回字典
    def get_dic(self, sql_str):
        try:
            self.cur_dic.execute(sql_str)
            dic = self.cur_dic.fetchall()
        except Exception as e:
            print(e)
        return dic

    # 以字典的形式插入
    def insert_dic(self,sql_str,data):
        '''
        传参示例：
        data = {'id': '20180606','name': 'Lily','age': 20}
        sql = 'INSERT INTO 'students'({keys}) VALUES ({values})'
        '''
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = sql_str.format(keys=keys, values=values)
        try:
            self.cursor.execute(sql, tuple(data.values()))
            print('Successful')
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    # 创建数据表,删除，更新
    def execute(self, sql_str):
        try:
            self.cursor.execute(sql_str)
        except Exception as e:
            print(e)

    # 按格式插入，查重，返回。
    def run(self, sql, params):

        '''
        1.批量插入数据,返回行数
        :param sql: 插入数据模版, 需要指定列和可替换字符串个数
        :param params: 插入所需数据，插入单条为元祖，多条记录为列表嵌套元组[(1, '张三', '男'),(2, '李四', '女'),]
        sql = "INSERT INTO USER VALUES (%s,%s,%s,%s)"
        params = [(2, 'fighter01', 'admin', 'sanpang'),
                (3, 'fighter02', 'admin', 'sanpang')]

        2.传入参数查重，返回0，1
        sql = 'select * from student where sno = %s'
        params = ('01')
        ret = mydb.run(sql,params)
        '''

        try:
            count = self.cursor.execute(sql, params)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return count

'''
if __name__ == "__main__":
    # 对象实例化
    mydb = database_mysql(host='localhost', username='root', password='12345', db='sql')
    mydb.connect()

    #--------方法调用-----------#

    # 01 run()方法查重
    sql = 'select * from student where sno = %s'
    params = ('01')
    ret = mydb.run(sql, params)
    print(ret)

    # 02 run()方法插入元组
    sql_str1 = 'INSERT INTO student(SNO,SSEX,SNAME,SAGE) VALUE(%s,%s,%s,%s)'
    params = ('100', '男', '墨尘', datetime.date(1996, 9, 20))
    mydb.run(sql_str1, params)

    # 03 insert_dic()插入字典
    data = {'sno': '110', 'ssex': 'boy', 'sname': 'mirco', 'sage': datetime.date(1996, 9, 20)}
    sql_str2 = 'INSERT INTO student({keys}) VALUES ({values})'
    mydb.insert_dic(sql_str2, data)

    # 04 get_tuple()/get_dic 获取元组和字段
    sql_str = 'select * from student'
    data1 = mydb.get_tuple(sql_str)
    data2 = mydb.get_dic(sql_str)
    print(data1, data2)

    mydb.close()
    
'''