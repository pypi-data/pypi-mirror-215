from yplib.index import *
import pymysql


# 有关数据库操作的类
def get_connect(db, user, passwd, charset, port, host):
    return pymysql.connect(db='MoneyKing', user='moneyking_uer', passwd='3^qp3Xqt4bG7', charset="utf8mb4",
                           port=3307,
                           host='192.168.40.230')


# 执行 sql 语句
def exec_sql(db_conn, sql='', commit=True):
    local_cursor = db_conn.cursor()
    local_cursor.execute(sql)
    if commit:
        db_conn.commit()

# print('end')
